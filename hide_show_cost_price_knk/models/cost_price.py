from odoo import models, api, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_sales_user = fields.Boolean(
        compute="_compute_is_sales_user",
        string="Is Sales User",
        store=False,
    )

    @api.depends('create_uid')
    def _compute_is_sales_user(self):
        # List of groups for which the cost price should be invisible
        groups_to_check = [
            'sales_team.group_sale_salesman',
            'sales_team.group_sale_salesman_all_leads',
            'sales_team.group_sale_manager',
            'point_of_sale.group_pos_user',
            'point_of_sale.group_pos_manager',
            'stock.group_stock_user',
            'stock.group_stock_manager',
        ]

        # Groups to exclude
        excluded_groups = [
            'purchase.group_purchase_user',
            'base.group_system',  # Administrator group
            'account.group_account_user',
        ]

        for product in self:
            # Get the group objects for the current user
            user_groups = self.env.user.groups_id

            # Check if the user belongs to any of the specified groups
            is_included = any(
                self.env.ref(group, raise_if_not_found=False) in user_groups for group in groups_to_check
            )

            # Check if the user belongs to any of the excluded groups
            is_excluded = any(
                self.env.ref(group, raise_if_not_found=False) in user_groups for group in excluded_groups
            )

            # Set is_sales_user to True only if included and not excluded
            product.is_sales_user = is_included and not is_excluded