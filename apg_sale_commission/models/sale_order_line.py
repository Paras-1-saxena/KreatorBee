# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
from datetime import timedelta

from markupsafe import Markup

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.fields import Command
from odoo.osv import expression
from odoo.tools import float_compare, float_is_zero, format_date, groupby
from odoo.tools.translate import _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    _description = "Sales Order Line"


    direct_commission_partner_id = fields.Many2one('res.partner', string='Direct Commission', compute='_compute_commission')
    partner_commission_partner_id = fields.Many2one('res.partner', string='Partner Commission',readonly=False,store=True)
    direct_commission_amount = fields.Float(string='Direct Commission Amount', compute='_compute_commission',store=True)
    partner_commission_amount = fields.Float(string='Partner Commission Amount', compute='_compute_commission',store=True)
    is_commission = fields.Boolean(string="Is Commission", compute='_compute_commission',store=True)
    user_id = fields.Many2one(
        'res.users',
        string="Salesperson",
        related="order_id.user_id",
        store=True
    )
    @api.depends('product_id','price_subtotal','partner_commission_partner_id')
    def _compute_commission(self):
        elearning_id = False
        self.partner_commission_amount = False
        self.direct_commission_amount = False
        self.direct_commission_partner_id = False
        # self.partner_commission_partner_id = False
        self.is_commission = False
        partner_commission_id = self.env['partner.commission'].search([],order='create_date desc',  # Order by creation date, latest first
            limit=1
        )
        direct_commission_id = self.env['direct.commission'].search([],order='create_date desc',  # Order by creation date, latest first
            limit=1
        )
        if not partner_commission_id:
            raise exceptions.ValidationError(_("Please configure Partner Commission"))
        if not direct_commission_id:
            raise exceptions.ValidationError(_("Please configure Direct Commission"))
        for line in self:
            if line.product_id:
                elearning_id = self.env['slide.channel'].search([
                    ('state', '=', 'published'),
                    ('product_id', '=', line.product_id.id)
                    ], limit=1)
            if elearning_id:
                if line.partner_commission_partner_id:
                    line.partner_commission_amount = (line.price_subtotal * partner_commission_id.rate)/100
                
                line.direct_commission_amount = (line.price_subtotal * direct_commission_id.rate)/100
                line.direct_commission_partner_id = elearning_id.create_uid.partner_id.id
                # line.partner_commission_partner_id = elearning_id.create_uid.partner_id.id
                line.is_commission = True


class SaleTarget(models.Model):
    _name = 'sale.target'
    _description = "Sales Target"

    name = fields.Char(string='name')
    target_amount = fields.Float(string='Target Amount')
    date_from = fields.Date(string='Start Date')
    date_to = fields.Date(string='End Date')
    achievement_ids = fields.One2many(
        'sale.target.achievement',
        'sale_target_id',
        string='Achievements'
    )

    # @api.depends('date_from', 'date_to')
    # def _compute_achievements(self):
    #     for record in self:
    #         if record.date_from and record.date_to:
    #             # Fetch sale orders in the date range
    #             sale_orders = self.env['sale.order'].search([
    #                 ('date_order', '>=', record.date_from),
    #                 ('date_order', '<=', record.date_to)
    #             ])
    #
    #             # Aggregate partner-wise amounts
    #             partner_amounts = {}
    #             for order in sale_orders:
    #                 partner_user = self.env['res.users'].search([
    #                     ('partner_id', '=', order.partner_id.id),
    #                     ('user_type', '=', 'partner')
    #                 ], limit=1)
    #
    #                 if partner_user:
    #                     total_amount = sum(order.order_line.mapped('price_subtotal'))
    #                     partner_id = order.partner_id.id
    #                     if partner_id in partner_amounts:
    #                         partner_amounts[partner_id] += total_amount
    #                     else:
    #                         partner_amounts[partner_id] = total_amount
    #
    #             # Create achievements
    #             new_achievements = [
    #                 (0, 0, {
    #                     'partner_id': partner_id,
    #                     'amount': amount,
    #                     'sale_target_id': record.id,
    #                 })
    #                 for partner_id, amount in partner_amounts.items()
    #             ]
    #
    #             # Update the achievement_ids field with the new values
    #             record.achievement_ids = [(5, 0, 0)] + new_achievements  # Clear old achievements, then add new ones
    #         else:
    #             record.achievement_ids = [(5, 0, 0)]  # Clear achievements if no date range
    class SaleTargetAchievement(models.Model):
        _name = 'sale.target.achievement'
        _description = 'Sale Target Achievement'

        partner_id = fields.Many2one('res.partner', string='Partner')
        amount = fields.Float(string='Amount')
        sale_target_id = fields.Many2one('sale.target', string='Sale Target', ondelete='cascade')



