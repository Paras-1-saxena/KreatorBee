from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    specific_commission = fields.Float(string='Specific Partner Commission')


class Partner(models.Model):
    _inherit = 'res.partner'

    my_commission_count = fields.Integer(compute="_compute_commission_count")


    def _compute_commission_count(self):
        order_lines = self.env['sale.order.line'].search([
            ('partner_commission_partner_id', '=', self.id)
        ])
        # Extract unique Sale Orders
        sale_orders = order_lines.mapped('order_id')
        self.my_commission_count = len(sale_orders)

    commission_line_ids = fields.One2many(
        'sale.order.line',
        'partner_commission_partner_id',
        string="Commission Lines"
    )

    commission_count = fields.Integer(
        string="Commission Count",
        compute="_compute_commission_order_count",
        store=True
    )

    @api.depends('commission_line_ids.order_id')
    def _compute_commission_order_count(self):
        for partner in self:
            # count unique sale orders linked to partner's commission lines
            order_ids = partner.commission_line_ids.mapped('order_id')
            partner.commission_count = len(set(order_ids.ids))


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