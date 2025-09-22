# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2025-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: SREERAG PM (<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import api, fields, models, _
from odoo.tools.safe_eval import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
				""" This class is used to inherit sale order"""
				_inherit = 'sale.order'
				
				subscription_count = fields.Integer(string='Subscriptions',
								compute='_compute_subscription_count',
								help='Subscriptions count')
				is_subscription = fields.Boolean(string='Is Subscription', default=False,
								help='Is subscription')
				subscription_id = fields.Many2one('subscription.package',
								string='Subscription',
								help='Choose the subscription')
				sub_reference = fields.Char(string="Sub Reference Code", store=True,
								compute="_compute_reference_code",
								help='Subscription Reference Code')
				
				def check_payment_status(self):
								import requests
								
								# API credentials (Replace these with your actual credentials)
								client_id="Coke62IvL4I4KV14X8BEH1DTg8dzXVPiAgfpaRZb"
								client_secret="GIiFXhQnDuxpzgaQDYi9FrQBi8VxXiyGoALu9pXajYvpga0GCQxf6jtyGDqHN5wErtPrtC1FuUUSGvKPpCimmsy4sDEmJgwt8vwzLJIO7s61QIcu1vLe2A2UTYElfhCc"
								
								# OAuth endpoint to get the access token
								auth_url="https://api.instamojo.com/oauth2/token/"
								
								# Prepare the data for the request
								data={
												'client_id':client_id,'client_secret':client_secret,'grant_type':'client_credentials'}
								
								# Send POST request to get the access token
								response=requests.post(auth_url,data=data)
								
								# Check if the request was successful
								if response.status_code==200:
												access_token=response.json()['access_token']
												
												headers={
																'Authorization':f'Bearer {access_token}'}
												
												# Make GET request to fetch payment status
												url="https://api.instamojo.com/v2/payments/"
												params={"page":1,"limit":9000}
												
												res=requests.get(url,headers=headers,params=params)
												res.raise_for_status()
												payments=res.json()
												so_no=self.name
												filtered=[p for p in payments.get("payments",[]) if p.get("title")==so_no]
												
												if filtered and filtered[0]['status']:
																_logger.info("Statusssssssssssssssssssssss: %s",filtered)
																
																if self.state=='draft':
																				self.action_confirm()
																tx=self.env['payment.transaction'].sudo().search([('reference','=',so_no)],limit=1)
																if tx and tx.state != 'done':
																				tx.provider_reference=filtered[0]['id']
																				tx._set_done()
																print("narshhhhhhhhhhhhh", filtered)
												else:
																_logger.info("NO payment status: %s",filtered)
																raise ValidationError(_('There is not Payment status received from Instamojo.'))
				
				
				
				@api.model_create_multi
				def create(self, vals_list):
								""" It displays subscription in sale order """
								for vals in vals_list:
												if vals.get('is_subscription'):
																vals.update({
																				'is_subscription': True,
																				'subscription_id': vals.get('subscription_id'),
																})
												return super().create(vals)
				
				@api.depends('subscription_id')
				def _compute_reference_code(self):
								""" It displays subscription reference code """
								for sub in self:
												sub.sub_reference = self.env['subscription.package'].search(
																[('id', '=', int(sub.subscription_id.id))]).reference_code
				
				def action_confirm(self):
								""" It Changed the stage, to renew, start date for subscription
								package based on sale order confirm """
								
								res = super().action_confirm()
								sale_order = self.subscription_id.sale_order_id
								so_state = self.search([('id', '=', sale_order.id)]).state
								partner = self.partner_id
								in_progress_subs = partner.subscription_product_line_ids.subscription_id.filtered(
												lambda sub: sub.stage_id.name == 'In Progress')
								draft_subs = partner.subscription_product_line_ids.subscription_id.filtered(
												lambda sub: sub.stage_id.name == 'Draft')[:1]
								
								if draft_subs and len(in_progress_subs) < 1:
												draft_subs.button_start_date()
								if so_state in ['sale', 'done']:
												stage = self.env['subscription.package.stage'].search(
																[('category', '=', 'progress')], limit=1).id
												values = {'stage_id': stage, 'is_to_renew': False,
																'start_date': datetime.datetime.today()}
												self.subscription_id.write(values)
								return res
				
				@api.depends('subscription_count')
				def _compute_subscription_count(self):
								"""the compute function the count of
								subscriptions associated with the sale order."""
								subscription_count = self.env[
												'subscription.package'].sudo().search_count(
												[('sale_order_id', '=', self.id)])
								if subscription_count > 0:
												self.subscription_count = subscription_count
								else:
												self.subscription_count = 0
				
				def button_subscription(self):
								"""Open the subscription packages associated with the sale order."""
								return {
												'name': 'Subscription',
												'sale_order_id': False,
												'domain': [('sale_order_id', '=', self.id)],
												'view_type': 'form',
												'res_model': 'subscription.package',
												'view_mode': 'list,form',
												'type': 'ir.actions.act_window',
												'context': {
																"create": False
												}
								}
				
				def _action_confirm(self):
								"""the function used to Confrim the sale order and
								create subscriptions for subscription products"""
								combo_product = self.order_line.filtered(lambda p: p.product_id.bom_ids)
								if combo_product:
												new_order =  self.env['sale.order'].create({
																'name': f'Course Access {self.name}',
																'partner_id': self.partner_id.id,
																'date_order': self.date_order,
																'company_id': self.company_id.id,
																'order_line': [(0, 0, {
																				'product_id': line.product_id.id,
																				'product_uom_qty': 1,
																				'price_unit': 0,
																}) for line in combo_product.product_id.bom_ids[0].bom_line_ids]
												})
												new_order.action_confirm()
								if self.subscription_count != 1:
												if self.order_line:
																for line in self.order_line:
																				if line.product_id.is_subscription:
																								existing_subscription = self.env['subscription.package'].search([('partner_id', '=', self.partner_id.id)])
																								existing_subscription = existing_subscription.filtered(lambda es: es.stage_id.name == 'In Progress')
																								existing_subscription = self.env['subscription.package'].search([('partner_id', '=', self.partner_id.id),
																												('stage_id.name', '=', 'In Progress')
																								], order="start_date desc", limit=1)
																								close_state = self.env['subscription.package.stage'].search([('name', '=', 'Closed')], limit=1)
																								# if existing_subscription:
																								#     existing_subscription.write({'stage_id': close_state.id})
																								#     invoices = self.env['account.move'].search([('subscription_id', '=', existing_subscription.id), ('state', '=', 'posted'), ('payment_state', '!=', 'paid')])
																								#     invoices.button_draft()
																								#     invoices.button_cancel()
																								this_products_line = []
																								rec_list = [0, 0, {'product_id': line.product_id.id,
																												'product_qty': line.product_uom_qty,
																												'unit_price': line.product_id.list_price}]
																								this_products_line.append(rec_list)
																								subscription = self.env['subscription.package'].create(
																												{
																																'sale_order_id': self.id,
																																'reference_code': self.env[
																																				                 'ir.sequence'].next_by_code(
																																				'sequence.reference.code'),
																																'start_date': existing_subscription.next_invoice_date + relativedelta(days=1) if existing_subscription else fields.Date.today(),
																																'stage_id': self.env.ref('subscription_package.draft_stage').id,
																																'partner_id': self.partner_id.id,
																																'plan_id': line.product_id.subscription_plan_id.id,
																																'product_line_ids': this_products_line
																												})
																								# subscription.button_start_date()
								return super()._action_confirm()
