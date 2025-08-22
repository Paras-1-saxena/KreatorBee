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
from odoo import models, fields, api


class ResPartner(models.Model):
    """Inherited res partner model"""
    _inherit = 'res.partner'

    is_active_subscription = fields.Boolean(string="Active Subscription",
                                            default=False,
                                            help='Is Subscription is active')
    subscription_product_line_ids = fields.One2many(
        'subscription.package.product.line', 'res_partner_id',
        ondelete='restrict', string='Products Line',
        help='Subscription product')

    def _valid_field_parameter(self, field, name):
        """
        Validate field parameters, allowing custom handling for 'ondelete'
        """
        if name == 'ondelete':
            return True
        return super(ResPartner,
                     self)._valid_field_parameter(field, name)


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def create(self, vals):
        user = super(ResUsers, self).create(vals)

        # Check if user is in portal group
        portal_group = self.env.ref('base.group_portal')
        if portal_group in user.groups_id:
            # Find product with name "[Free] 28 Days Subscription"
            product = self.env['product.product'].search([('name', '=', '[Free] 28 Days Subscription')], limit=1)

            if product:
                # Create subscription
                subscription = self.env['subscription.package'].create({
                    'reference_code': self.env['ir.sequence'].next_by_code('sequence.reference.code'),
                    'start_date': fields.Date.today(),
                    'stage_id': self.env.ref('subscription_package.draft_stage').id,
                    'partner_id': user.partner_id.id,
                    'plan_id': product.subscription_plan_id.id if product.subscription_plan_id else False,
                    'product_line_ids': [(6, 0, [product.id])],  # Many2many or One2many handling
                })
                subscription.button_start_date()
        return user