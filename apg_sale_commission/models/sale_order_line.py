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
    partner_commission_partner_id = fields.Many2one('res.partner', string='Partner Commission', readonly=False, store=True)
    direct_commission_amount = fields.Float(string='Direct Commission Amount', compute='_compute_commission',store=True)
    partner_commission_amount = fields.Float(string='Partner Commission Amount', compute='_compute_commission',store=True)
    referral_partner_id = fields.Many2one('res.partner', string='Referral Partner', readonly=False, store=True)
    referral_partner_subs_status = fields.Selection([
        ('inprogress', 'In Progress'),
        ('closed', 'Closed')
        ], string='Referral Partner Subscription Status')
    is_commission = fields.Boolean(string="Is Commission", compute='_compute_commission',store=True)
    user_id = fields.Many2one(
        'res.users',
        string="Salesperson",
        related="order_id.user_id",
        store=True
    )
    @api.depends('product_id','price_subtotal','partner_commission_partner_id')
    def _compute_commission(self):
        for line in self:
            line.partner_commission_amount = line.price_subtotal if line.partner_commission_partner_id else False
            line.direct_commission_amount = False
            line.direct_commission_partner_id = False
            line.is_commission = True
        # elearning_id = False
        # partner_commission_id = self.env['partner.commission'].search([],order='create_date desc',  # Order by creation date, latest first
        #     limit=1
        # )
        # direct_commission_id = self.env['direct.commission'].search([],order='create_date desc',  # Order by creation date, latest first
        #     limit=1
        # )
        # if not partner_commission_id:
        #     raise exceptions.ValidationError(_("Please configure Partner Commission"))
        # if not direct_commission_id:
        #     raise exceptions.ValidationError(_("Please configure Direct Commission"))
        # # discounted_line = self.filtered(lambda ol: ol.discount > 0.0)
        # for line in self:
        #     if line.partner_commission_amount > 0.0:
        #         line.partner_commission_amount = line.partner_commission_amount
        #         line.direct_commission_amount = line.direct_commission_amount
        #         line.direct_commission_partner_id = line.direct_commission_partner_id
        #         line.is_commission = line.is_commission
        #         continue
        #     if line.product_id:
        #         elearning_id = self.env['slide.channel'].search([
        #             ('state', '=', 'published'),
        #             ('product_id', '=', line.product_id.id)
        #             ], limit=1)
        #     specific_partner_commission = line.product_id.product_tmpl_id.specific_commission if line.product_id.product_tmpl_id.specific_commission > 0.0 else 70.0 if line.price_unit < 0.0 else 0.0
        #     if elearning_id or line.price_unit < 0.0:
        #         coupon_type = line.order_id.coupon_type
        #         if coupon_type == 'partner':
        #             total_discount = (line.price_unit / 100) * line.discount
        #             if line.partner_commission_partner_id:
        #                 line.partner_commission_amount = (((line.price_subtotal + total_discount) * (specific_partner_commission if specific_partner_commission else partner_commission_id.rate)) / 100) - (total_discount*0.6)
        #             else:
        #                 line.partner_commission_amount = 0.0
        #             line.direct_commission_amount = ((line.price_subtotal + total_discount) * (direct_commission_id.rate - ((specific_partner_commission if specific_partner_commission else partner_commission_id.rate) if line.partner_commission_partner_id else 0.0))) / 100
        #             line.direct_commission_partner_id = elearning_id.create_uid.partner_id.id
        #             # line.partner_commission_partner_id = elearning_id.create_uid.partner_id.id
        #             line.is_commission = True
        #         elif coupon_type == 'creator':
        #             total_discount = (line.price_unit / 100) * line.discount
        #             if line.partner_commission_partner_id:
        #                 line.partner_commission_amount = ((line.price_subtotal + total_discount) * (
        #                     specific_partner_commission if specific_partner_commission else partner_commission_id.rate)) / 100
        #             else:
        #                 line.partner_commission_amount = 0.0
        #             line.direct_commission_amount = (((line.price_subtotal + total_discount) * (direct_commission_id.rate - ((specific_partner_commission if specific_partner_commission else partner_commission_id.rate) if line.partner_commission_partner_id else 0.0))) / 100) - (total_discount * 0.6)
        #             line.direct_commission_partner_id = elearning_id.create_uid.partner_id.id
        #             # line.partner_commission_partner_id = elearning_id.create_uid.partner_id.id
        #             line.is_commission = True
        #         else:
        #             total_discount = (line.price_unit / 100) * line.discount
        #             if line.partner_commission_partner_id:
        #                 line.partner_commission_amount = ((line.price_subtotal+total_discount) * (specific_partner_commission if specific_partner_commission else partner_commission_id.rate))/100
        #             else:
        #                 line.partner_commission_amount = 0.0
        #             line.direct_commission_amount = ((line.price_subtotal+total_discount) * (direct_commission_id.rate - ((specific_partner_commission if specific_partner_commission else partner_commission_id.rate) if line.partner_commission_partner_id else 0.0)))/100
        #             line.direct_commission_partner_id = elearning_id.create_uid.partner_id.id
        #             # line.partner_commission_partner_id = elearning_id.create_uid.partner_id.id
        #             line.is_commission = True
        #     else:
        #         line.partner_commission_amount = False
        #         line.direct_commission_amount = False
        #         line.direct_commission_partner_id = False
        #         line.is_commission = False


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
    update_amount = fields.Boolean('Amount Update', default=False, compute='_amount_calculate')

    def _amount_calculate(self):
        self.update_amount = True

        order_lines = self.env['sale.order.line'].sudo().search([
            ('state', '=', 'sale'),
            ('partner_commission_partner_id', 'in', self.achievement_ids.mapped('partner_id').ids)
        ])
        partner_commission_id = self.env['partner.commission'].sudo().search([],order='create_date desc',  # Order by creation date, latest first
            limit=1
        )

        if self.achievement_ids:
            for achievement_partner in self.achievement_ids:
                amount = False
                for line in order_lines.filtered(lambda l: l.partner_commission_partner_id.id == achievement_partner.partner_id.id):
                    if partner_commission_id:
                        amount += (line.price_subtotal * partner_commission_id.rate)/100
                achievement_partner.amount = amount

class SaleTargetAchievement(models.Model):
    _name = 'sale.target.achievement'
    _description = 'Sale Target Achievement'

    partner_id = fields.Many2one('res.partner', string='Partner')
    amount = fields.Float(string='Amount')
    sale_target_id = fields.Many2one('sale.target', string='Sale Target', ondelete='cascade')

class Partner(models.Model):
    _inherit = 'res.partner'

    user_type = fields.Selection(
        [('creator', 'Creator'),('partner', 'Partner'), ('customer', 'Customer'),('internal_user', 'Internal')],
        string='User Type',
        required=True,
    )

    @api.model
    def create(self, values_list):
        partner = super(Partner, self).create(values_list)
        if partner.user_type == 'partner':
            # Fetch all sales target records
            sale_targets = self.env['sale.target'].sudo().search([])
            for target in sale_targets:
                # Check if the partner is already in the achievement_ids
                existing_achievement = target.achievement_ids.filtered(lambda a: a.partner_id == partner)
                if not existing_achievement:
                    # Create a new achievement record
                    self.env['sale.target.achievement'].sudo().create({
                        'partner_id': partner.id,
                        'amount': target.target_amount,  # Default amount can be set as needed
                        'sale_target_id': target.id,
                    })
        return partner
