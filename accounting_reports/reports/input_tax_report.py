from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, tools
import xlwt
from xlwt import easyxf
from io import StringIO
from io import BytesIO
from babel import numbers


def format_indian_number(value):
    """Format numbers into Indian currency style (1,00,000)."""

    """Format numbers into Indian currency style using Babel library."""
    # Format the value using the Indian locale (in this case, India locale)
    formatted_value = numbers.format_decimal(value, locale='en_IN')

    return formatted_value




class WizardInputTaxReport(models.TransientModel):
    _name = 'wizard.input.tax.report'
    _description = "Input Tax Report"

    end_date = fields.Date('End Date')
    company_id = fields.Many2one(
        'res.company', string='Company')  # , default=lambda self: self.env.user.company_id)


    start_date = fields.Date(string='Start Date', required=True)
    # end_date = fields.Date(string='End Date', required=True)

    # Usage

    def print_input_tax_report(self):

        import base64
        workbook = xlwt.Workbook()
        style = xlwt.XFStyle()
        tall_style = xlwt.easyxf('font:height 820;')
        font = xlwt.Font()
        font.name = 'Times New Roman'
        font.bold = True
        font.height = 250
        style.font = font
        xlwt.add_palette_colour("ice_blue", 0x1F)
        xlwt.add_palette_colour("gray25", 0x16)
        header_style = easyxf(
            'pattern: pattern solid, fore_colour gray25;'
            'font: name Arial;'
            'alignment: horizontal  center;'
            'font:bold True,height 400'
        )
        header_style1 = easyxf(
            'pattern: pattern solid, fore_colour gray25;'
            'font: name Arial;'
            'alignment: horizontal  center;'
            'font:bold True,height 220'
        )
        style1_left = easyxf(
            'pattern: pattern solid, fore_colour gray25;'
            'font: name Arial;'
            'alignment: horizontal center;'
            'font:bold True,height 220'
        )
        style1_left1 = easyxf(
            'font: name Arial;'
            'alignment: horizontal  left;'
        )
        style1_left2 = easyxf(
            'font: name Arial;'
            'alignment: horizontal  left;'
            'pattern: pattern solid, fore_colour gray25;'
        )
        style1_center = easyxf(
            'font: name Arial;'
            'alignment: horizontal  center;'
        )
        bold_style = easyxf(
            'font: name Arial;'
            'alignment: horizontal  left;'
            'font:bold True'
        )

        table_footer = easyxf(
            'pattern: pattern solid, fore_colour gray25;'
            'font: name Arial;'
            'alignment: horizontal  right;'
            'font:bold True,height 220'
        )
        footer = easyxf(
            'pattern: pattern solid, fore_colour gray25;'
            'font: name Arial;'
            'alignment: horizontal  left;'
            'font:bold True,height 220'
        )
        table_footer_value = easyxf(
            'pattern: pattern solid, fore_colour gray25;'
            'font: name Arial;'
            'alignment: horizontal  center;'
            'font:bold True,height 220'
        )

        worksheet = workbook.add_sheet('Sheet 1')
        col_0 = worksheet.col(0)
        col_1 = worksheet.col(1)
        col_2 = worksheet.col(2)
        col_3 = worksheet.col(3)
        col_4 = worksheet.col(4)
        col_5 = worksheet.col(5)
        col_6 = worksheet.col(6)
        col_7 = worksheet.col(7)
        col_8 = worksheet.col(8)
        col_9 = worksheet.col(9)
        col_10 = worksheet.col(10)
        col_11 = worksheet.col(11)
        col_12 = worksheet.col(12)
        col_13 = worksheet.col(13)
        col_14 = worksheet.col(14)
        col_15 = worksheet.col(15)
        col_16 = worksheet.col(16)

        col_0.width = 250 * 12
        col_1.width = 250 * 20
        col_2.width = 250 * 20
        col_3.width = 250 * 18
        col_4.width = 250 * 15
        col_5.width = 250 * 20
        col_6.width = 250 * 12
        col_7.width = 250 * 18
        col_8.width = 250 * 18
        col_9.width = 250 * 18
        col_10.width = 250 * 18
        col_11.width = 250 * 20
        col_12.width = 250 * 12
        col_13.width = 250 * 18
        col_14.width = 250 * 18
        col_15.width = 250 * 18
        col_16.width = 250 * 18

        filename = 'Input Tax Reports.xls'

        year = date.today().year
        row = 0
        worksheet.write(row, 0, '#', style1_left)
        worksheet.write(row, 1, 'Supplier TIN', style1_left)
        worksheet.write(row, 2, 'Supplier Invoice Number', style1_left)
        # worksheet.write(row, 3, "Supplier Invoice Number ", style1_left)
        worksheet.write(row, 3, 'Invoice Date', style1_left)
        worksheet.write(row, 4, 'Invoice Total (excluding GST)', style1_left)
        worksheet.write(row, 5, 'GST Charged at 6% ', style1_left)
        worksheet.write(row, 6, 'GST Charged at 8%', style1_left)
        # worksheet.write(row, 7, 'GST Charged at 8%', style1_left)
        worksheet.write(row, 7, 'GST Charged at 12%', style1_left)
        worksheet.write(row, 8, 'GST Charged at 16%', style1_left)
        worksheet.write(row, 9, 'Your Taxable Activity Number', style1_left)
        worksheet.write(row, 10, 'Revenue / Capital', style1_left)
        invoice = self.env['account.move'].search([('move_type', 'in', ['in_invoice', 'in_refund']),
                                                   # Filter for purchase invoices and refunds
                                                   ('state', '=', 'posted'),
                                                   ('invoice_date', '>=', self.start_date),  # Start date filter
                                                   ('invoice_date', '<=', self.end_date)
                                                   ])
        items = self.env['account.move.line'].search([
                                                   ('account_id.name', 'ilike', "input"),
                                                   ('date', '>=', self.start_date),  # Start date filter
                                                    ('date', '<=', self.end_date),
                                                    ('parent_state', '=', 'posted'),
                                                  ])
        # print("items", items.mapped('move_name'))
        name = items.mapped('move_name')

        invoice_journals = self.env['account.move'].search([('name', 'in', name)])

        print("items", invoice_journals.mapped('name'))
        # errrr
        row = 1

        sorted_invoices = sorted(invoice_journals, key=lambda rec: rec.invoice_date)
        for rec in sorted_invoices:
            i = 1
            # if rec.move_type == 'in_invoice':  # Use rec.move_type here
            print(rec.amount_untaxed_signed)
            worksheet.write(row, 0, i or '', style1_left1)
            worksheet.write(row, 1, rec.partner_id.vat or '', style1_left1)
            # worksheet.write(row, 1, rec.partner_id.name or '', style1_left1)
            worksheet.write(row, 2, rec.name or '', style1_left1)
            worksheet.write(row, 3, rec.invoice_date and rec.invoice_date.strftime('%Y-%m-%d') or '', style1_left1)
            worksheet.write(row, 4, format_indian_number(rec.amount_untaxed) or '',style1_left1)
            total_gst_6_value = 0
            total_gst_8_value = 0
            total_gst_12_value = 0
            total_gst_16_value = 0
            print(rec.invoice_line_ids)
            # Convert to string to avoid errors
            for record in rec.invoice_line_ids:
                print('record', record)
                for tax in record.tax_ids:
                    if tax.tax_group_id.name == 'GST 6%':  # Check if the tax group name matches 'Gst 8%'
                        new = record.price_total - record.price_subtotal
                        total_gst_6_value += abs(new)
                    if tax.tax_group_id.name == 'GST 8%':
                        new = record.price_total - record.price_subtotal
                        print('new', tax.tax_group_id.name)
                        total_gst_8_value += abs(new)
                    if tax.tax_group_id.name == 'GST 12%':
                        new = record.price_total - record.price_subtotal
                        total_gst_12_value += abs(new)
                    if tax.tax_group_id.name == 'GST 16%':
                        new = record.price_total - record.price_subtotal
                        total_gst_16_value += abs(new)
                    print('tax.tax_group_id.name', tax.tax_group_id.name)
            worksheet.write(row, 5, format_indian_number(abs(total_gst_6_value)) if total_gst_6_value else '', style1_left1)
            worksheet.write(row, 6, format_indian_number(abs(total_gst_8_value)) if total_gst_8_value else '', style1_left1)
            worksheet.write(row, 7, format_indian_number(abs(total_gst_12_value)) if total_gst_12_value else '', style1_left1)
            worksheet.write(row, 8, format_indian_number(abs(total_gst_16_value)) if total_gst_16_value else '', style1_left1)

            # else:  # Use rec.move_type here
            #     print(rec.amount_untaxed_signed)
            #     worksheet.write(row, 0, i or '', style1_left1)
            #     worksheet.write(row, 1, rec.partner_id.vat or '', style1_left1)
            #     # worksheet.write(row, 1, rec.partner_id.name or '', style1_left1)
            #     worksheet.write(row, 2, rec.name or '', style1_left1)
            #     worksheet.write(row, 3, rec.invoice_date and rec.invoice_date.strftime('%Y-%m-%d') or '', style1_left1)
            #     worksheet.write(row, 4, '-' + format_indian_number(str(rec.amount_untaxed)) or '', style1_left1)
            #     total_gst_6_value = 0
            #     total_gst_8_value = 0
            #     total_gst_12_value = 0
            #     total_gst_16_value = 0
            #     print(rec.invoice_line_ids)
            #     # Convert to string to avoid errors
            #     for record in rec.invoice_line_ids:
            #         print('record', record)
            #         for tax in record.tax_ids:
            #             if tax.tax_group_id.name == 'GST 6%':  # Check if the tax group name matches 'Gst 8%'
            #                 new = record.price_total - record.price_subtotal
            #                 total_gst_6_value += abs(new)
            #             if tax.tax_group_id.name == 'GST 8%':
            #                 new = record.price_total - record.price_subtotal
            #                 print('new', tax.tax_group_id.name)
            #                 total_gst_8_value += abs(new)
            #             if tax.tax_group_id.name == 'GST 12%':
            #                 new = record.price_total - record.price_subtotal
            #                 total_gst_12_value += abs(new)
            #             if tax.tax_group_id.name == 'GST 16%':
            #                 new = record.price_total - record.price_subtotal
            #                 total_gst_16_value += abs(new)
            #             print('tax.tax_group_id.name', tax.tax_group_id.name)
            #     worksheet.write(row, 5, format_indian_number(abs(total_gst_6_value)) if total_gst_6_value else '', style1_left1)
            #     worksheet.write(row, 6, format_indian_number(abs(total_gst_8_value)) if total_gst_8_value else '', style1_left1)
            #     worksheet.write(row, 7, format_indian_number(abs(total_gst_12_value)) if total_gst_12_value else '', style1_left1)
            #     worksheet.write(row, 8, format_indian_number(abs(total_gst_16_value)) if total_gst_16_value else '', style1_left1)
            row +=1
            i +=1



        # error

        fp = BytesIO()
        workbook.save(fp)
        export_id = self.env['input.tax.report.excel'].create(
            {
                'excel_file': base64.b64encode(fp.getvalue()),
                'file_name': filename,
            }
        )
        fp.close()

        return {
            'view_mode': 'form',
            'res_id': export_id.id,
            'res_model': 'input.tax.report.excel',
            'view_type': 'form',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
    #
    def action_print_report(self):
        # Call the actual method that generates the report
        return self.env['wizard.input.tax.report'].print_input_tax_report()


class InputReport(models.TransientModel):
    _name = "input.tax.report.excel"

    excel_file = fields.Binary('Input Tax Report Sheet')
    file_name = fields.Char('Excel File', size=64)