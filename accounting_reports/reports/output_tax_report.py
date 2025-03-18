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



class WizardOutputTaxReport(models.TransientModel):
    _name = 'wizard.output.tax.report'
    _description = "Output Tax Report"

    end_date = fields.Date('End Date')
    company_id = fields.Many2one(
        'res.company', string='Company')  # , default=lambda self: self.env.user.company_id)
    start_date = fields.Date(string='Start Date', required=True)


    # Usage

    def print_output_tax_report(self):

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

        filename = 'Output Tax Reports.xls'

        year = date.today().year
        row = 0
        worksheet.write(row, 0, 'Customer TIN', style1_left)
        worksheet.write(row, 1, 'Customer Name', style1_left)
        worksheet.write(row, 2, 'Invoice No.', style1_left)
        worksheet.write(row, 3, "Invoice Date", style1_left)
        worksheet.write(row, 4, 'Invoice Total (excluding GST)', style1_left)
        worksheet.write(row, 5, 'GST Charged at 8%', style1_left)
        worksheet.write(row, 6, 'GST Charged at 16%', style1_left)
        worksheet.write(row, 7, 'Value of Zero-Rated Supplies', style1_left)
        worksheet.write(row, 8, 'Value of Exempt Supplies', style1_left)
        worksheet.write(row, 9, 'Value of Out-of-Scope Supplies', style1_left)
        worksheet.write(row, 10, 'Your Taxable Activity No.', style1_left)

        invoice = self.env['account.move'].search([('move_type', 'in', ['out_invoice', 'out_refund']),
                                                   ('journal_id.name', '!=', 'Sales MSC'),
                                                   ('state', '=', 'posted'),
                                                   ('invoice_date', '>=', self.start_date),  # Start date filter
                                                   ('invoice_date', '<=', self.end_date),
                                                   ])
        row = 1

        sorted_invoices = sorted(invoice, key=lambda rec: rec.invoice_date)

        for rec in sorted_invoices:

            if rec.move_type == 'out_invoice':  # Use rec.move_type here
                print(rec.amount_untaxed_signed)
                worksheet.write(row, 0, rec.partner_id.vat or '', style1_left1)
                worksheet.write(row, 1, rec.partner_id.name or '', style1_left1)
                worksheet.write(row, 2, rec.name or '', style1_left1)
                worksheet.write(row, 3, rec.invoice_date.strftime('%Y-%m-%d'), style1_left1)
                worksheet.write(row, 4, format_indian_number(rec.amount_untaxed), style1_left1)
                total_gst_8_value = 0
                total_gst_16_value = 0

                # Iterate through all invoice lines and sum up tax values
                for record in rec.invoice_line_ids:
                    for tax in record.tax_ids:
                        if tax.tax_group_id.name == 'GST 8%':
                            new = record.price_total - record.price_subtotal
                            print('total_gst_8_value', record.price_subtotal)# Check if it's 'GST 8%'
                            print('total_gst_8_value', new)# Check if it's 'GST 8%'
                            total_gst_8_value += abs(new)
                        elif tax.tax_group_id.name == 'GST 16%':  # Check if it's 'GST 16%'
                            new = record.price_total - record.price_subtotal
                            total_gst_16_value += abs(new)
                # print('total_gst_8_value', record.new)
                # Write the summed values for GST tax groups
                worksheet.write(row, 5, format_indian_number(total_gst_8_value) if total_gst_8_value else '',
                                style1_left1)  # Column for GST 8%
                worksheet.write(row, 6, format_indian_number(total_gst_16_value) if total_gst_16_value else '',
                                style1_left1)  # Column for GST 16%
            # err
                # if tax_group_names
                # Now `tax_group_names` contains all the names.
                # print(tax_group_names)

            else:  # Handle other cases (e.g., refunds)

                worksheet.write(row, 1, rec.partner_id.name or '', style1_left1)

                worksheet.write(row, 2, rec.name or '', style1_left1)

                worksheet.write(row, 3, rec.invoice_date.strftime('%Y-%m-%d'), style1_left1)

                worksheet.write(row, 4, '-' + format_indian_number((round(rec.amount_untaxed, 2))), style1_left1)

                total_gst_8_value = 0

                total_gst_16_value = 0

                # Iterate through all invoice lines and sum up tax values

                for record in rec.invoice_line_ids:

                    for tax in record.tax_ids:

                        if tax.tax_group_id.name == 'GST 8%':

                            new = record.price_total - record.price_subtotal

                            print('GST 8% Subtotal:', record.price_subtotal)

                            print('GST 8% Tax Amount:', new)

                            total_gst_8_value += abs(new)

                        elif tax.tax_group_id.name == 'GST 16%':

                            new = record.price_total - record.price_subtotal

                            print('GST 16% Subtotal:', record.price_subtotal)

                            print('GST 16% Tax Amount:', new)

                            total_gst_16_value += abs(new)

                # Write the summed values for GST tax groups

                worksheet.write(row, 5, format_indian_number(total_gst_8_value) if total_gst_8_value else '',
                                style1_left1)  # Column for GST 8%
                worksheet.write(row, 6, format_indian_number(total_gst_16_value) if total_gst_16_value else '',
                                style1_left1)  # Column for GST 16%

            row += 1  # Move to the next row for the next invoice

        fp = BytesIO()
        workbook.save(fp)
        export_id = self.env['output.tax.report.excel'].create(
            {
                'excel_file': base64.b64encode(fp.getvalue()),
                'file_name': filename,
            }
        )
        fp.close()

        return {
            'view_mode': 'form',
            'res_id': export_id.id,
            'res_model': 'output.tax.report.excel',
            'view_type': 'form',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
    #
    def action_print_report(self):
        # Call the actual method that generates the report
        return self.env['wizard.output.tax.report'].print_output_tax_report()


class OutputReport(models.TransientModel):
    _name = "output.tax.report.excel"

    excel_file = fields.Binary('output Tax Report Sheet')
    file_name = fields.Char('Excel File', size=64)