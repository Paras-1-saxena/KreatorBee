# -*- coding: utf-8 -*-
from odoo import api, fields, models , _
from odoo.exceptions import ValidationError


class Partner(models.Model):
    _inherit = 'res.partner'

    code = fields.Char(size=64, index=True, tracking=True)

    @api.constrains('code')
    def _check_barcode_unicity(self):
        if self.env['res.partner'].search_count([('code', '=', self.code)]) > 1:
            raise ValidationError('An other user already has this code')

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if name:
            args = ['|', '|', '|', ('name', operator, name), ('code', operator, name),
                    ('mobile', operator, name), ('email', operator, name)] + args
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)

    @api.model_create_multi
    def create(self, values_list):
        for values in values_list:
            # Ensure that 'code' field is set for each record in the values list
            if not values.get('code'):
                values['code'] = self.env['ir.sequence'].with_company(values.get('company_id')).next_by_code('res.partner') or 'New'

        # Call the super method to actually create the records
        return super(Partner, self).create(values_list)
