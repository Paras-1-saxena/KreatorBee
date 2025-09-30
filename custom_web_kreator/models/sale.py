from odoo import models, fields, api
from datetime import date, datetime, timedelta, time


class SaleOrder(models.Model):
				_inherit = 'sale.order'
				
				referral_partner_id = fields.Many2one('res.partner', string='Referral Partner')
				
				def _update_partner_onlines(self):
								if self.referral_partner_id:
												commission_partner=self.referral_partner_id
												
												commission_partner_courses=commission_partner.sale_order_ids.filtered(
																lambda so:so.state in ['sale','done']).order_line.filtered(
																lambda line:line.product_id.bom_ids).product_id
												commission_partner_count=len(commission_partner_courses)
												
												# Count courses current user owns (before this order)
												user_courses=self.partner_id.sale_order_ids.filtered(
																lambda so:so.state in ['sale','done']).order_line.filtered(
																lambda line:line.product_id.bom_ids).product_id
												user_course_count=len(user_courses)
												
												# Find difference
												diff_count=max(0,commission_partner_count-user_course_count)
												
												subscription=commission_partner.subscription_product_line_ids.subscription_id.filtered(
																lambda sub:sub.stage_id.name=='In Progress')
												
												end_days=-1
												if subscription:
																end_days=(subscription.next_invoice_date-datetime.today().date()).days
												
												if diff_count>0:
																# Filter only course lines (products with BoM)
																course_lines=self.sudo().order_line.filtered(lambda l:l.product_id.bom_ids)
																
																# Take only up to diff_count lines
																lines_to_update=course_lines[:diff_count]
																
																if lines_to_update:
																				lines_to_update.write({
																								'partner_commission_partner_id':commission_partner.id if end_days>=0 else False,
																								'referral_partner_id':          commission_partner.id,
																								'referral_partner_subs_status': 'inprogress' if end_days>=0 else 'closed',})
				
								else:
												previous_commission_lines=self.env['sale.order.line'].sudo().search(
																[('order_id.partner_id','=',self.partner_id.id),('partner_commission_partner_id','!=',False),
																				('order_id.state','in',['sale','done']),],limit=1)
												
												if previous_commission_lines:
																commission_partner=previous_commission_lines.partner_commission_partner_id
																
																# Count courses commission partner owns
																commission_partner_courses=commission_partner.sale_order_ids.filtered(
																				lambda so:so.state in ['sale','done']).order_line.filtered(
																				lambda line:line.product_id.bom_ids).product_id
																commission_partner_count=len(commission_partner_courses)
																
																# Count courses current user owns (before this order)
																user_courses=self.partner_id.sale_order_ids.filtered(
																				lambda so:so.state in ['sale','done']).order_line.filtered(
																				lambda line:line.product_id.bom_ids).product_id
																user_course_count=len(user_courses)
																
																# Find difference
																diff_count=max(0,commission_partner_count-user_course_count)
																
																subscription=commission_partner.subscription_product_line_ids.subscription_id.filtered(
																				lambda sub:sub.stage_id.name=='In Progress')
																end_days=-1
																if subscription:
																				end_days=(subscription.next_invoice_date-datetime.today().date()).days
																
																if diff_count>0:
																				# Filter only course lines (products with BoM)
																				course_lines=self.sudo().order_line.filtered(lambda l:l.product_id.bom_ids)
																				
																				# Take only up to diff_count lines
																				lines_to_update=course_lines[:diff_count]
																				
																				if lines_to_update:
																								lines_to_update.write({
																												'partner_commission_partner_id':commission_partner.id if end_days>=0 else False,
																												'referral_partner_id':          commission_partner.id,
																												'referral_partner_subs_status': 'inprogress' if end_days>=0 else 'closed',})


				def _action_confirm(self):
								user = self.env.user
								sale_cart = self.env['kb.sale.cart'].sudo().search([('name', '=', user.id)], limit=1)
								sale_cart.sudo().write({'course_ids': False})
								return super()._action_confirm()