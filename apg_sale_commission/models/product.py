from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    specific_commission = fields.Float(string='Specific Partner Commission')


class Partner(models.Model):
    _inherit = 'res.partner'

    my_commission_count = fields.Integer(compute="_compute_commission_count")
    commission_count = fields.Integer(
        string="My Commission Orders",
        compute="_compute_commission_order_count",
        store=True
    )

    @api.depends('sale_order_line_ids.partner_commission_partner_id')
    def _compute_commission_order_count(self):
        # use read_group for efficiency
        counts = self.env['sale.order.line'].read_group(
            [('partner_commission_partner_id', 'in', self.ids)],
            ['order_id'],
            ['partner_commission_partner_id']
        )
        # build mapping partner -> unique order count
        mapping = {}
        for rec in counts:
            partner_id = rec['partner_commission_partner_id'][0]
            mapping.setdefault(partner_id, set()).add(rec['order_id'][0])

        for partner in self:
            partner.commission_count = len(mapping.get(partner.id, set()))


    def _compute_commission_count(self):
        order_lines = self.env['sale.order.line'].search([
            ('partner_commission_partner_id', '=', self.id)
        ])
        # Extract unique Sale Orders
        sale_orders = order_lines.mapped('order_id')
        self.my_commission_count = len(sale_orders)

    # def _compute_like_count(self):
    #     for line in self:
    #         line.like_count = len(line.like_ids)


    def action_view_my_commission_sale_order(self):
        self.ensure_one()
        # Find all sale order lines with this commission partner
        order_lines = self.env['sale.order.line'].search([
            ('partner_commission_partner_id', '=', self.id)
        ])
        # Extract unique Sale Orders
        sale_orders = order_lines.mapped('order_id')

        # Load the standard Sale Order action
        action = self.env['ir.actions.actions']._for_xml_id('sale.action_orders')
        action['domain'] = [('id', 'in', sale_orders.ids)]
        return action