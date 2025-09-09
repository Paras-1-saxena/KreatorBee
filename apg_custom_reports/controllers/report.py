from odoo import models, fields, api,http
import io
import xlsxwriter
import base64
from io import BytesIO
import xlwt
from datetime import date
from datetime import datetime, time
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.http import request
from odoo.exceptions import UserError, ValidationError
import pytz


class CommissionReportWizard(models.TransientModel):
    _name = 'commission.report.wizard'
    _description = 'Commission Report Wizard'

    from_date = fields.Date(string='From Date', required=True)
    to_date = fields.Date(string='To Date', required=True)

    def action_download_report(self):
        # Create an in-memory binary stream
        output = io.BytesIO()

        # Create an Excel workbook and worksheet
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Detailed- info about affiliate')

        # Adding headers for the first sheet
        headers = ['Order Name', 'Customer Name', 'Affiliate ID(Sponsor)', 'Affiliate User ID(Sponsor)',
                   'Affiliate Email(Sponsor)', 'Affiliate Plan', 'Commission', 'Phone', 'Email',
                   'Revenue', 'Product', 'Remarks', 'Tag']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)

        worksheet1 = workbook.add_worksheet('Sponsor Commission Detail')

        # Adding headers for the second sheet
        headers1 = ['From Date - To Date', 'Sponsor ID', 'Sponsor Name', 'Sponsor Email id', 'Commission',
                    'TDS', 'After TDS', 'Account no.', 'Holder Name', 'IFSCCode', 'Status',
                    'Reason For Failed']
        for col, header in enumerate(headers1):
            worksheet1.write(0, col, header)

        # Fetch sale.order data based on date range
        sale_orders = self.env['sale.order'].search([
            ('date_order', '>=', self.from_date),
            ('date_order', '<=', self.to_date)
        ])

        # Group order lines by partner and calculate commission totals
        partner_commission = {}
        for order in sale_orders:
            for line in order.order_line:
                # Handle `direct_commission_partner_id`
                direct_partner = line.direct_commission_partner_id
                if direct_partner:
                    if direct_partner.id not in partner_commission:
                        partner_commission[direct_partner.id] = {
                            'partner': direct_partner,
                            'commission_total': 0.0
                        }
                    partner_commission[direct_partner.id]['commission_total'] += line.direct_commission_amount or 0.0

                # Handle `partner_commission_partner_id`
                commission_partner = line.partner_commission_partner_id
                if commission_partner:
                    if commission_partner.id not in partner_commission:
                        partner_commission[commission_partner.id] = {
                            'partner': commission_partner,
                            'commission_total': 0.0
                        }
                    partner_commission[commission_partner.id][
                        'commission_total'] += line.partner_commission_amount or 0.0

        # Write the aggregated data into the first worksheet (no duplicate partner names)
        row = 1  # Start writing data from row 1 (header row is 0)
        for partner_data in partner_commission.values():
            partner = partner_data['partner']
            commission_total = partner_data['commission_total']

            # Write partner-specific details (aggregated commission for the partner)
            worksheet.write(row, 0, '')  # Leave the Order Name empty
            worksheet.write(row, 1, partner.name or '')  # Customer Name (Partner Name)
            worksheet.write(row, 2, partner.code or '')  # Affiliate ID
            worksheet.write(row, 3, '')  # Affiliate User ID
            worksheet.write(row, 4, partner.email or '')  # Affiliate Email
            worksheet.write(row, 5, 'Influence Mastery')  # Affiliate Plan
            worksheet.write(row, 6, commission_total or 0.0)  # Commission (Total for the partner)
            worksheet.write(row, 7, partner.phone)  # Phone
            worksheet.write(row, 8, partner.email)
            worksheet.write(row, 9, '')
            worksheet.write(row, 10, '')
            worksheet.write(row, 11, 'Ok Case')
            worksheet.write(row, 12, 'Payu')

            row += 1  # Increment row for the next partner

        # Write grouped data for the second sheet
        date_range = f"{self.from_date} to {self.to_date}"
        row = 1  # Start writing data from row 1 in the second worksheet
        for partner_data in partner_commission.values():
            partner = partner_data['partner']
            commission_total = partner_data['commission_total']
            tds = commission_total * 0.02  # 2% TDS
            after_tds = commission_total - tds

            worksheet1.write(row, 0, date_range)  # Static Week
            worksheet1.write(row, 1, partner.code)  # Sponsor ID
            worksheet1.write(row, 2, partner.name)  # Sponsor Name
            worksheet1.write(row, 3, partner.email)  # Sponsor Email
            worksheet1.write(row, 4, commission_total)  # Total Commission
            worksheet1.write(row, 5, tds)  # TDS
            worksheet1.write(row, 6, after_tds)  # After TDS
            worksheet1.write(row, 7, partner.Account_holder_number or '')  # Account Number
            worksheet1.write(row, 8, partner.Account_holder_name or '')  # Holder Name
            worksheet1.write(row, 9, partner.ifsc_code or '')  # IFSC Code
            worksheet1.write(row, 10, '')  # Status
            worksheet1.write(row, 11, '')  # Reason For Failed

            row += 1

        # Close workbook
        workbook.close()

        # Prepare the file for download
        output.seek(0)
        attachment = self.env['ir.attachment'].create({
            'name': 'Commission_Report.xlsx',
            'datas': base64.b64encode(output.read()),
            'type': 'binary',
            'store_fname': 'Commission_Report.xlsx',
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })

        output.close()

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % attachment.id,
            'target': 'self',
        }

class RBLBankReportController(http.Controller):

    @http.route('/rbl_bank_report/download', type='http', auth="user")
    def download_rbl_bank_report(self):
        # Create an in-memory binary stream
        output = io.BytesIO()

        # Create an Excel workbook and worksheet
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('sample')

        # Adding headers
        headers = ['Payment Type', 'Cust Ref Number', 'Source Account Number', 'Source Narration',
                   'Destination Account Number', 'Currency', 'Amount', 'Destination Narration', 'Destination bank',
                   'Destination Bank IFS Code',
                   'Beneficiary Name', 'Beneficiary Account Type', 'Email ']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)

        # Initialize the row counter
        row = 1

        # Query account.payments in the "paid" state
        payments = request.env['account.payment'].search([('state', '=', 'paid')])

        for payment in payments:
            # Fetch partner information
            partner = payment.partner_id
            partner_bank = partner.bank_id.bank_id.name if partner.bank_id else None
            if partner_bank == 'RBL':
                # Static fields
                payment_type = 'NFT'
                source_narration = 'Cash Back'
                currency = 'INR'
                amount = payment.amount
                beneficiary_name = partner.name
                beneficiary_account_type = 'Savings'

                # Write data to Excel sheet
                worksheet.write(row, 0, payment_type)
                worksheet.write(row, 1, partner.code)
                worksheet.write(row, 2,'6898764534654')
                worksheet.write(row, 3, source_narration)
                worksheet.write(row, 4, partner.Account_holder_number)
                worksheet.write(row, 5, currency)
                worksheet.write(row, 6, amount)
                worksheet.write(row, 7, 'My Company')
                worksheet.write(row, 8, 'Indian Bank')
                worksheet.write(row, 9, '454654')
                worksheet.write(row, 10, beneficiary_name)
                worksheet.write(row, 11, beneficiary_account_type)
                worksheet.write(row, 12, partner.email)

                # Move to the next row for the next payment
                row += 1

        # Close the workbook
        workbook.close()

        # Prepare the response as a downloadable Excel file
        response = request.make_response(
            output.getvalue(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', 'attachment; filename=RBL_Bank_Report.xlsx;')
            ]
        )
        output.close()
        return response

class ICICIBankReportController(http.Controller):
    @http.route('/icici_bank_report/download', type='http', auth="user")
    def download_icici_bank_report(self):
        # Create an in-memory binary stream
        output = io.BytesIO()

        # Create an Excel workbook and worksheet
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('sheet1')

        # Adding headers (same as before)
        headers = [
            'PYMT_PROD_TYPE_CODE', 'PYMT_MODE', 'DEBIT_ACC_NO', 'BNF_NAME',
            'BENE_ACC_NO', 'BENE_IFSC', 'AMOUNT', 'DEBIT_NARR', 'CREDIT_NARR',
            'MOBILE_NUM', 'EMAIL_ID', 'REMARK', 'PYMT_DATE', 'REF_NO',
            'ADDL_INFO1', 'ADDL_INFO2', 'ADDL_INFO3', 'ADDL_INFO4', 'ADDL_INFO5'
        ]
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)  # Writing headers to the first row

        # Initialize the row counter
        row = 1

        # Query account.payments in the "paid" state and partner's bank name as "ICICI"
        payments = request.env['account.payment'].search([
            ('state', '=', 'paid')
        ])

        for payment in payments:
            partner = payment.partner_id
            print("partner",partner)
            partner_bank = partner.bank_id.bank_id.name if partner.bank_id else None
            print("partner_bank",partner_bank)
            if partner_bank == 'ICICI':
                payment_type = 'BULK'
                payment_mode = 'NEFT'
                debit_account_no = '6898764534654'
                beneficiary_name = partner.name
                beneficiary_account_no = partner.Account_holder_number
                beneficiary_ifsc = partner.ifsc_code
                amount = payment.amount
                debit_narration = 'Payment Initiated'
                credit_narration = 'Funds Received'
                mobile_num = partner.phone
                email = partner.email
                remark = 'Transaction Approved'
                payment_date = payment.date.strftime('%Y-%m-%d')  # Format the payment date
                ref_no = payment.name
                add_info1 = 'Info1'
                add_info2 = 'Info2'
                add_info3 = 'Info3'
                add_info4 = 'Info4'
                add_info5 = 'Info5'

                # Write data to Excel sheet
                worksheet.write(row, 0, payment_type)
                worksheet.write(row, 1, payment_mode)
                worksheet.write(row, 2, debit_account_no)
                worksheet.write(row, 3, beneficiary_name)
                worksheet.write(row, 4, beneficiary_account_no)
                worksheet.write(row, 5, beneficiary_ifsc)
                worksheet.write(row, 6, amount)
                worksheet.write(row, 7, debit_narration)
                worksheet.write(row, 8, credit_narration)
                worksheet.write(row, 9, mobile_num)
                worksheet.write(row, 10, email)
                worksheet.write(row, 11, remark)
                worksheet.write(row, 12, payment_date)
                worksheet.write(row, 13, ref_no)
                worksheet.write(row, 14, add_info1)
                worksheet.write(row, 15, add_info2)
                worksheet.write(row, 16, add_info3)
                worksheet.write(row, 17, add_info4)
                worksheet.write(row, 18, add_info5)

                # Move to the next row for the next payment
                row += 1

        # Close the workbook
        workbook.close()

        # Prepare the response as a downloadable Excel file
        response = request.make_response(
            output.getvalue(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', 'attachment; filename=ICICI_Bank_Report.xlsx;')
            ]
        )
        output.close()
        return response

class SalesCustomReportWizard(models.TransientModel):
    _name = 'sale.custom.report.wizard'
    _description = 'Sales Report Wizard'

    from_date = fields.Date(string='Order Date From')
    to_date = fields.Date(string='Order Date To')
    joined_from = fields.Date(string='Joined From Date')
    joined_to = fields.Date(string='Joined TO Date')
    customer_partner_id = fields.Many2one('res.partner', string="Customer")


    def check_filters(self):
        sale_orders = self.env['sale.order']
        for rec in self:
            # Validation checks
            if rec.joined_from > rec.joined_to:
                raise exceptions.ValidationError(_("Joined From Date should not be greater than Joined To Date."))

            if rec.from_date > rec.to_date:
                raise exceptions.ValidationError(_("From Date should not be greater than To Date."))

            # Build user domain
            domain = []
            if rec.joined_from and rec.joined_to:
                domain += [
                    ('create_date', '>=', rec.joined_from),
                    ('create_date', '<=', rec.joined_to)
                ]
            if rec.customer_partner_id:
                domain.append(('partner_id', '=', rec.customer_partner_id.id))

            # Fetch users and their partners
            partner_ids = self.env['res.users'].sudo().search(domain).mapped('partner_id')
            # Build sale order domain
            so_domain = []
            if rec.from_date and rec.to_date:
                so_domain += [
                    ('date_order', '>=', rec.from_date),
                    ('date_order', '<=', rec.to_date)
                ]

            if partner_ids:
                so_domain.append(('partner_id', 'in', partner_ids.ids))
            so_domain.append(('state', '=', 'sale'))

            # Fetch sale orders
            sale_orders = self.env['sale.order'].sudo().search(so_domain, order="name asc") if so_domain else self.env['sale.order']

        return sale_orders


    def action_download_report(self):

        sale_orders = self.check_filters()

        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Sheet 1')

        # Column widths
        worksheet.col(0).width = 250 * 12
        worksheet.col(1).width = 250 * 20
        worksheet.col(2).width = 250 * 20
        worksheet.col(3).width = 250 * 18
        worksheet.col(4).width = 250 * 15
        worksheet.col(5).width = 250 * 20
        worksheet.col(6).width = 250 * 12

        # Headers
        row = 0
        worksheet.write(row, 0, 'Customer Name')
        worksheet.write(row, 1, 'Email')
        worksheet.write(row, 2, 'Phone number')
        worksheet.write(row, 3, 'Sponsor')
        worksheet.write(row, 4, 'Purchase amount')
        worksheet.write(row, 5, 'Joined on')
        worksheet.write(row, 6, 'Products')

        row = 1
        total_sale = 0.0
        if sale_orders:
            for rec in sale_orders:
                if rec.amount_total > 0:
                    total_sale += rec.amount_total

                    # products for each SO ( fixed loop – before it was fetching all products for all orders every time)
                    products = ", ".join(
                        line.product_id.name
                        for line in rec.order_line
                        if line.product_id.bom_ids
                    )
                    sponsor_name = (
                        rec.order_line.filtered(lambda l: l.partner_commission_partner_id)
                        [:1].partner_commission_partner_id.name
                    )

                    worksheet.write(row, 0, rec.partner_id.name or '')
                    worksheet.write(row, 1, rec.partner_id.email or '')
                    worksheet.write(row, 2, rec.partner_id.mobile or '')
                    worksheet.write(row, 3, sponsor_name or '')
                    worksheet.write(row, 4, rec.amount_total or 0.0)
                    worksheet.write(row, 5, str(rec.partner_id.create_date.date()) if rec.partner_id.create_date else '')
                    worksheet.write(row, 6, products or '')
                    row += 1
            # Total row
            worksheet.write(row, 3, 'Total')
            worksheet.write(row, 4, total_sale or 0.0)

        # Save to memory
        fp = BytesIO()
        workbook.save(fp)
        fp.seek(0)

        # Create attachment for direct download
        attachment = self.env['ir.attachment'].create({
            'name': 'Sales Report.xls',
            'datas': base64.b64encode(fp.getvalue()),
            'type': 'binary',
            'store_fname': 'sales_report.xls',
            'mimetype': 'application/vnd.ms-excel',
        })

        fp.close()

        # Direct download
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % attachment.id,
            'target': 'self',
        }

class SalesCommissionReportWizard(models.TransientModel):
    _name = 'sales.commission.report.wizard'
    _description = 'Sales Commission Report Wizard'

    
    from_date = fields.Date(string='Date From')
    to_date = fields.Date(string='Date To')
    partner_ids = fields.Many2many('res.partner', string="Sponsor Name")
   


    def check_filters(self):
        SaleOrderLine = self.env['sale.order.line']
        result = {}

        for rec in self:
            if rec.from_date and rec.to_date and rec.from_date > rec.to_date:
                raise exceptions.ValidationError(_("From Date should not be greater than To Date."))

            domain = [('order_id.state', '=', 'sale')]
            if rec.from_date and rec.to_date:
                # Get user timezone
                user_tz = self.env.user.tz or 'UTC'
                tz = pytz.timezone(user_tz)

                # Localize dates in user timezone
                from_dt_local = datetime.combine(rec.from_date, time.min)
                to_dt_local = datetime.combine(rec.to_date, time.max)

                # Convert to UTC for DB comparison
                from_dt_utc = tz.localize(from_dt_local).astimezone(pytz.UTC)
                to_dt_utc = tz.localize(to_dt_local).astimezone(pytz.UTC)

                domain += [
                    ('order_id.date_order', '>=', from_dt_utc.strftime(DEFAULT_SERVER_DATETIME_FORMAT)),
                    ('order_id.date_order', '<=', to_dt_utc.strftime(DEFAULT_SERVER_DATETIME_FORMAT)),
                ]
            if rec.partner_ids:
                domain.append(('partner_commission_partner_id', 'in', rec.partner_ids.ids))

            order_lines = SaleOrderLine.sudo().search(domain)

            for line in order_lines:
                partner = line.partner_commission_partner_id
                if not partner:
                    continue

                if partner.id not in result:
                    result[partner.id] = {
                        'partner_commission_partner_id': partner.name,
                        'partner_commission_email': partner.email or '',
                        'partner_commission_phone': partner.phone or '',
                        'partner_commission_amount': 0.0,
                        'order_ids': []
                    }

                result[partner.id]['partner_commission_amount'] += line.partner_commission_amount

                if line.order_id.id not in result[partner.id]['order_ids']:
                    result[partner.id]['order_ids'].append(line.order_id.id)

        return result


    def action_download_report(self):
        commissionData = self.check_filters()

        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Sales Commission Report')

        # Define styles
        header_style = xlwt.easyxf("font: bold on; align: horiz center;")
        subheader_style = xlwt.easyxf("font: bold on; align: horiz center;")
        normal_style = xlwt.easyxf("align: horiz center;")
        normal_style1 = xlwt.easyxf("align: horiz left;")
        sponsor_style = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_color gray25; align: horiz center;")


        # Column widths
        for i, w in enumerate([25, 30, 25, 30, 15, 20, 40]):
            worksheet.col(i).width = 250 * w

        # Headers
        row = 0
        worksheet.write(row, 0, 'Sponsor Name', header_style)
        worksheet.write(row, 1, 'Email', header_style)
        worksheet.write(row, 2, 'Phone number', header_style)
        worksheet.write(row, 3, 'Commission Amount', header_style)
        # worksheet.write(row+1, 1, 'Customer Name', subheader_style)
        # worksheet.write(row+1, 2, 'Customer Email', subheader_style)
        # worksheet.write(row+1, 3, 'Customer Phone', subheader_style)
        # worksheet.write(row+1, 4, 'Purchase Amount', subheader_style)
        # worksheet.write(row+1, 5, 'Order Date', subheader_style)
        # worksheet.write(row+1, 6, 'Products', subheader_style)

        row = 1
        if commissionData:
            for partner_id, data in commissionData.items():
                # Sponsor info
                worksheet.write(row, 0, data['partner_commission_partner_id'], sponsor_style)
                worksheet.write(row, 1, data['partner_commission_email'], sponsor_style)
                worksheet.write(row, 2, data['partner_commission_phone'], sponsor_style)
                worksheet.write(row, 3, data['partner_commission_amount'], sponsor_style)
                row += 1

                # Get full SO records
                orders = self.env['sale.order'].browse(data['order_ids'])
                for order in orders:
                    products = ", ".join(order.order_line.mapped('product_id.display_name'))
                    worksheet.write(row, 1, order.partner_id.name or '', normal_style)
                    worksheet.write(row, 2, order.partner_id.email or '', normal_style)
                    worksheet.write(row, 3, order.partner_id.phone or '', normal_style)
                    worksheet.write(row, 4, order.amount_total or 0.0, normal_style)
                    worksheet.write(row, 5, str(order.date_order.date()) if order.date_order else '', normal_style)
                    worksheet.write(row, 6, products or '', normal_style)
                    row += 1

        # Save file in memory
        fp = BytesIO()
        workbook.save(fp)
        fp.seek(0)

        attachment = self.env['ir.attachment'].create({
            'name': 'Sales Commission Report.xls',
            'datas': base64.b64encode(fp.getvalue()),
            'type': 'binary',
            'store_fname': 'sales_report.xls',
            'mimetype': 'application/vnd.ms-excel',
        })

        fp.close()

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % attachment.id,
            'target': 'self',
        }