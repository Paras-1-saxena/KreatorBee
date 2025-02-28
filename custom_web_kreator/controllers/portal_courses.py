# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import base64
from itertools import groupby
from operator import attrgetter
from datetime import date, datetime, timedelta
import json
from werkzeug.exceptions import NotFound
from odoo.addons.website.controllers.main import QueryURL
from odoo.http import content_disposition



class PortalMyCourses(http.Controller):

    # Not in Use Bharat/Roystan
    # @http.route(['/get-started'], type='http', auth='user', website=True)
    # def get_started(self, **kwargs):
    #     return request.render('custom_web_kreator.get_started')

    # @http.route('/get_started_home', type='http', auth='public', website=True)
    # def getstarted_home(self, **kwargs):
    #     return http.request.render('custom_web_kreator.get_started_home')

    # @http.route('/1get_started_home', type='http', auth='public', website=True)
    # def getstarted_homen(self, **kwargs):
    #     return http.request.render('custom_web_kreator.1get_started')

    # @http.route('/course-details', type='http', auth='public', website=True)
    # def course_details(self, **kwargs):
    #     return http.request.render('custom_web_kreator.course_detail')

    # @http.route('/course_standard', type='http', auth='public', website=True)
    # def course_standard(self, **kwargs):
    #     return http.request.render('custom_web_kreator.course_standard')

    # @http.route('/1course_standard', type='http', auth='public', website=True, methods=['POST'])
    # def Ncourse_standard(self, **kwargs):
    #     # Extract data from the form
    #     course_data = {
    #         'course_name': kwargs.get('course_name'),
    #         'course_description': kwargs.get('course_description'),
    #         'regular_price': kwargs.get('regular_price'),
    #         'sales_price': kwargs.get('sales_price'),
    #     }

    #     # Save the data in the session
    #     http.request.session['course_data'] = course_data

    #     # Debugging
    #     print("Course Data:", course_data)

    #     # Render the next page
    #     return http.request.render('custom_web_kreator.Ncourse_standard', {'course_data': course_data})

    # @http.route('/term_condition', type='http', auth='public', website=True)
    # def term_condition(self, **kwargs):
    #     return http.request.render('custom_web_kreator.term_condition')

    # @http.route('/1term_condition', type='http', auth='public', website=True, methods=['POST'])
    # def Nterm_condition(self, **kwargs):
    #     # Retrieve existing data from the session
    #     course_data = http.request.session.get('course_data', {})

    #     # Extract Google Drive link from the POST data
    #     google_drive_link = kwargs.get('google_drive_link')

    #     # Update the dictionary with the new data
    #     course_data['google_drive_link'] = google_drive_link

    #     # Save the updated dictionary back to the session
    #     http.request.session['course_data'] = course_data

    #     # Debugging
    #     print("Updated Course Data:", course_data)

    #     # Render the next page template
    #     return http.request.render('custom_web_kreator.Nterm', {'course_data': course_data})

    # @http.route('/submit', type='http', auth='public', website=True)
    # def submit_page(self, **kwargs):
    #     return http.request.render('custom_web_kreator.submit_page')

    # @http.route('/welcome', type='http', auth='public', website=True, methods=['GET', 'POST'])
    # def welcome_page(self, **kwargs):
    #     # Retrieve existing data from the session
    #     course_data = http.request.session.get('course_data', {})

    #     # Extract the "agreement" value
    #     agreement = kwargs.get('agreement')

    #     # Update the dictionary with the new data
    #     course_data['agreement'] = agreement

    #     # Save the final data back to the session
    #     http.request.session['course_data'] = course_data

    #     # Debugging
    #     print("Final Course Data:", course_data)

    #     # Check the agreement value
    #     if agreement != 'agree':
    #         print("User did not agree. Skipping course creation.")
    #         # Render the final page without creating a course
    #         return http.request.render('custom_web_kreator.welcome', {'course_data': course_data})

    #     # Validate required fields
    #     if all(key in course_data for key in ['course_name', 'course_description', 'regular_price', 'sales_price']):
    #         # Get sales price
    #         sales_price = float(course_data['sales_price'])

    #         # Fetch the rate values from partner.commission and direct.commission models
    #         partner_commission_rate = http.request.env['partner.commission'].sudo().search([], limit=1).rate
    #         direct_commission_rate = http.request.env['direct.commission'].sudo().search([], limit=1).rate

    #         # Calculate the commission values
    #         partner_commission_value = (sales_price * partner_commission_rate) / 100
    #         direct_commission_value = (sales_price * direct_commission_rate) / 100

    #         # Create a record in the slide.channel model
    #         http.request.env['slide.channel'].sudo().create({
    #             'name': course_data['course_name'],
    #             'description': course_data['course_description'],
    #             'regular_price': float(course_data['regular_price']),  # Convert to float if necessary
    #             'sales_price': sales_price,  # Convert to float if necessary
    #             'partner_commission': partner_commission_value,
    #             'direct_commission': direct_commission_value,
    #         })

    #         print("Slide Channel record created successfully.")
    #     else:
    #         print("Missing required data to create slide.channel record.")

    #     # Render the final page
    #     return http.request.render('custom_web_kreator.welcome', {'course_data': course_data})

    # @http.route('/leaderboard', type='http', auth='public', website=True)
    # def leaderboard(self, **kwargs):
    #     return http.request.render('custom_web_kreator.leaderboard_page')

    @http.route('/nleaderboard', type='http', auth='public', website=True)
    def nleaderboard(self, **kwargs):
        orders_lines = request.env['sale.order.line'].sudo().search([('is_commission','=', True),('state', '=', 'sale'),('partner_commission_partner_id', '!=', False)])
        order_lines = sorted(orders_lines, key=attrgetter('partner_commission_partner_id'))
        # Group by commission partner ID
        grouped_data = {}
        leaderboard = []
        for partner, lines in groupby(order_lines, key=attrgetter('partner_commission_partner_id')):
            grouped_data[partner] = {
                'total_commission': sum(line.partner_commission_amount for line in lines),
            }
        for data in grouped_data:
            lines = orders_lines.search([('partner_commission_partner_id','=',data.id)])
            leaderboard.append({
                'partner_name':data.name,
                'total_commission': sum(line.partner_commission_amount for line in lines),
            })
        leaderboard = sorted(leaderboard, key=lambda x: x['total_commission'], reverse=True)
        values = {
            'leaderboard':leaderboard,
            'currency_id': request.env.company.currency_id
        }
        

        return http.request.render('custom_web_kreator.nleaderboard_page',values)
    
    # Not in Use Bharat/Roystan
    # @http.route('/sales', type='http', auth='public', website=True)
    # def sales_page(self, **kwargs):
    #     return http.request.render('custom_web_kreator.sales_page_template')

    # Not in Use Bharat/Roystan
    # @http.route('/data', type='http', auth='public', website=True)
    # def data_page(self, **kwargs):
    #     # Render the data page template
    #     return http.request.render('custom_web_kreator.data_page_template')

    # @http.route('/ndata', type='http', auth='public', website=True)
    # def ndata_page(self, **kwargs):
    #     # Render the data page template
    #     return http.request.render('custom_web_kreator.ndata_page_template')

    # @http.route('/kyc', type='http', auth='public', website=True)
    # def kyc_page(self, **kwargs):
    #     # Render the data page template
    #     return http.request.render('custom_web_kreator.kyc_page_template')

    @http.route('/nkyc', type='http', auth='public', website=True, methods=['GET', 'POST'])
    def nkyc_page(self, **kwargs):
        # Fetch the current user and their partner record
        user = request.env.user
        partner = user.partner_id
        bank_id = False

        # Check if the user_type of the partner is 'creator'
        if partner.user_type != 'creator':
            print("You do not have permission to update this information. Only 'creator' users can update.")
            # return request.render('custom_web_kreator.error_page_template', {
            #     'error': "You do not have permission to update this information. Only 'creator' users can update."
            # })
        # Basic Details and document
        bank_id = request.env['res.partner.bank'].sudo().search([])
        if request.httprequest.method == 'POST':
            user = request.env.user
            partner = user.partner_id

            # Fetch the form data from the POST request
            full_name = kwargs.get('full_name')
            email = kwargs.get('email')
            mobile = kwargs.get('phone')
            document = kwargs.get('document') if kwargs.get('document') != '- Select -' else False
            state_selection = kwargs.get('state_selection', 'under_review')
            partner.write({'state_selection': state_selection})
            # Initialize a dictionary to update partner details
            partner_values = {}

            if full_name:
                partner_values['name'] = full_name
            if email:
                partner_values['email'] = email
            if mobile:
                partner_values['phone'] = mobile
            if document:
                partner_values['select_document'] = document

            # Common fields for document-specific details
            document_number = kwargs.get('document_number')
            document_name = kwargs.get('document_name')  # Dynamic field for document name
            document_front = kwargs.get('file_upload_front')  # Front side upload
            document_back = kwargs.get('file_upload_back')  # Back side upload

            # Map document types to field names
            document_mapping = {
                'passport': {
                    'number_field': 'passport_number',
                    'name_field': 'passport_name',
                    'front_file_field': 'passport_front',
                    'back_file_field': 'passport_back',
                },
                'aadhaar': {
                    'number_field': 'aadhaar_number',
                    'name_field': 'aadhaar_name',
                    'front_file_field': 'aadhaar_front',
                    'back_file_field': 'aadhaar_back',
                },
                'driving_license': {
                    'number_field': 'driving_license_number',
                    'name_field': 'driving_license_name',
                    'front_file_field': 'driving_license_front',
                    'back_file_field': 'driving_license_back',
                },
                'voter_identity_card': {
                    'number_field': 'voter_identity_number',
                    'name_field': 'voter_identity_name',
                    'front_file_field': 'voter_identity_front',
                    'back_file_field': 'voter_identity_back',
                },
            }

            # Handle document-specific updates dynamically
            if document and document in document_mapping:
                doc_fields = document_mapping[document]
                # Update document number and name
                if document_number:
                    partner_values[doc_fields['number_field']] = document_number
                if document_name:
                    partner_values[doc_fields['name_field']] = document_name

                # Upload front side of the document
                if document_front:
                    try:
                        front_data = document_front.read()
                        partner_values[doc_fields['front_file_field']] = base64.b64encode(front_data).decode('utf-8')
                    except Exception as e:
                        print("Front file upload failed",e)
                        # return request.render('custom_web_kreator.error_page_template', {
                        #     'error': f"Front file upload failed: {e}"
                        # })

                # Upload back side of the document
                if document_back:
                    try:
                        back_data = document_back.read()
                        partner_values[doc_fields['back_file_field']] = base64.b64encode(back_data).decode('utf-8')
                    except Exception as e:
                        print("Back file upload failed",e)
                        # return request.render('custom_web_kreator.error_page_template', {
                        #     'error': f"Back file upload failed: {e}"
                        # })

                # Reset other document-related fields
                for doc_type, fields in document_mapping.items():
                    if doc_type != document:  # Reset other document fields
                        partner_values[fields['number_field']] = False
                        partner_values[fields['name_field']] = False
                        partner_values[fields['front_file_field']] = False
                        partner_values[fields['back_file_field']] = False

            # Update pan details
            pan_card_number = kwargs.get('pan_number')
            pan_card_name = kwargs.get('pan_name')
            if pan_card_number:
                partner_values['pan_card_number'] = pan_card_number
            if pan_card_name:
                partner_values['pan_card_name'] = pan_card_name

            pan_card_file = kwargs.get('pan_file')
            if pan_card_file:
                try:
                    file_data = pan_card_file.read()
                    file_content = base64.b64encode(file_data).decode('utf-8')
                    partner_values['pan_card_file'] = file_content
                except Exception as e:
                    print("PAN card file upload failed",e)
                    # return request.render('custom_web_kreator.error_page_template', {
                    #     'error': f"PAN card file upload failed: {e}"
                    # })

            # Update bank details
            account_holder_name = kwargs.get('account_holder_name')
            account_holder_number = kwargs.get('account_number')
            ifsc_code = kwargs.get('ifsc_code')
            bank_id = kwargs.get('bank_id')
            print("bank_id",bank_id)

            # Search for the bank record using the bank_name
            if bank_id:
                bank = request.env['res.partner.bank'].sudo().search([('id', '=', bank_id)], limit=1)
                if bank:
                    partner_values['bank_id'] = bank.id  # Assign the bank_id to the partner record
                else:
                    # Handle case where bank with the provided name is not found
                    print("Bank with name not found.")
                    # return request.render('custom_web_kreator.error_page_template', {
                    #     'error': f"Bank with name {bank_name} not found."
                    # })
            upi_mobile_number = kwargs.get('upi_mobile_number')
            if account_holder_name:
                partner_values['Account_holder_name'] = account_holder_name
            if account_holder_number:
                partner_values['Account_holder_number'] = account_holder_number
            if ifsc_code:
                partner_values['ifsc_code'] = ifsc_code
            if upi_mobile_number:
                partner_values['upi_mobile_number'] = upi_mobile_number

            upload_file = kwargs.get('upload_file')
            if upload_file:
                try:
                    file_data = upload_file.read()
                    file_content = base64.b64encode(file_data).decode('utf-8')
                    partner_values['upload_file'] = file_content
                except Exception as e:
                    print("File upload failed",e)
                    # return request.render('custom_web_kreator.error_page_template', {
                    #     'error': f"File upload failed: {e}"
                    # })

            # Write all updates to the partner record
            if partner_values:
                partner.write(partner_values)

            return request.redirect('/nkyc')

        # If the request is a GET request (loading the form), fetch partner details to pre-populate
        selected_document = partner.select_document

        document_number = ''
        document_name = ''
        file_upload_front = ''
        file_upload_back = ''
        bank_file = ''
        pan_file = ''
        if selected_document:
            # Dynamically fetch the number and name fields
            if selected_document == 'voter_identity_card':
                document_number = getattr(partner, f"voter_identity_number", '')
                document_name = getattr(partner, f"voter_identity_name", '')
                file_upload_front = getattr(partner, f"voter_identity_front", '')
                file_upload_back = getattr(partner, f"voter_identity_back", '')
            else:
                document_number = getattr(partner, f"{selected_document}_number", '')
                document_name = getattr(partner, f"{selected_document}_name", '')
                file_upload_front = getattr(partner, f"{selected_document}_front", '')
                file_upload_back = getattr(partner, f"{selected_document}_back", '')

            # Convert binary fields to base64 strings for use in templates
            if file_upload_front:
                file_upload_front = base64.b64encode(file_upload_front).decode('utf-8')
            if file_upload_back:
                file_upload_back = base64.b64encode(file_upload_back).decode('utf-8')

        if partner.upload_file:
            bank_file = base64.b64encode(partner.upload_file).decode('utf-8')
        if partner.pan_card_file:
            pan_file = base64.b64encode(partner.pan_card_file).decode('utf-8')

        values = {
            'partner_id': partner,
            'partner_name': partner.name,
            'partner_email': partner.email,
            'partner_phone': partner.phone,
            'document': partner.select_document,
            'document_number': document_number,
            'document_name': document_name,
            'file_upload_front': file_upload_front,
            'file_upload_back': file_upload_back,
            'account_holder_name': partner.Account_holder_name,
            'account_number': partner.Account_holder_number,
            'bank_id': bank_id if bank_id else '',# This will render the bank's name in the template
            'ifsc_code': partner.ifsc_code,
            'upi_mobile_number': partner.upi_mobile_number,
            'bank_file': bank_file,
            'pan_number': partner.pan_card_number,
            'pan_name': partner.pan_card_name,
            'pan_file': pan_file,
            'state_selection' : partner.state_selection,

        }
        return request.render('custom_web_kreator.nkyc_page_template', values)

    # @http.route('/referral', type='http', auth='public', website=True)
    # def referral_page(self, **kwargs):
    #     # Render the data page template
    #     return http.request.render('custom_web_kreator.referral_link_page')

    @http.route('/nreferral', type='http', auth='public', website=True)
    def nreferral_page(self, **kwargs):
        # Render the data page template
        return http.request.render('custom_web_kreator.nreferral_link_page')

    # @http.route('/partner-home', type='http', auth='public', website=True)
    # def partner_page(self, **kwargs):
    #     # Render the data page template
    #     return http.request.render('custom_web_kreator.get_started_partner')

    @http.route('/partner', type='http', auth='public', website=True)
    def partner(self, **kwargs):
        current_user = request.env.user
        partner = current_user.partner_id
        # Define date ranges
        today = datetime.today().date()
        last_7_days = today - timedelta(days=7)
        last_30_days = today - timedelta(days=30)
        orders_obj = request.env['sale.order.line']
        # Initialize commission data
        partner_total_commission = 0.0
        partner_commission_today = 0.0
        partner_commission_last_7_days = 0.0
        partner_commission_last_30_days = 0.0
        order_lines = orders_obj.sudo().search([
            ('is_commission', '=', True),
            ('state', '=', 'sale'),
            ('partner_commission_partner_id', '=', partner.id)
        ])
        for line in order_lines:
            order_date = line.create_date.date()
            partner_total_commission += line.partner_commission_amount
            if order_date == today:
                partner_commission_today += line.partner_commission_amount
            if last_7_days <= order_date <= today:
                partner_commission_last_7_days += line.partner_commission_amount
            if last_30_days <= order_date <= today:
                partner_commission_last_30_days += line.partner_commission_amount

        # Prepare data for rendering or JSON response
        commission_data = {
            'commission': {
                'total': partner_total_commission,
                'today': partner_commission_today,
                'last_7_days': partner_commission_last_7_days,
                'last_30_days': partner_commission_last_30_days
            }
        }
        # Render the data page template
        return http.request.render('custom_web_kreator.Npartner', commission_data)

    # @http.route('/my-courses', type='http', auth='public', website=True)
    # def mycourses_page(self, **kwargs):
    #     # Render the data page template
    #     return http.request.render('custom_web_kreator.my_courses_template')

    @http.route('/nmy-courses', type='http', auth='user', website=True)
    def nmycourses_page(self, **kwargs):
        # Get the logged-in user
        current_user = request.env.user
        # Get the partner record associated with the current user
        partner = current_user.partner_id

        print("-------------currnt user",current_user)

        # Initialize course lists
        published_courses = []
        draft_review_courses = []

        # Check if the user is of type 'creator'
        if partner.user_type in ['creator','internal_user']:
            # Fetch published courses created by the user
            approved_courses = request.env['slide.channel'].sudo().search([
                ('create_uid', '=', current_user.id),
                ('state', '=', 'course_preview')
            ])
            
            # Fetch draft and under review courses created by the user
            published_courses = request.env['slide.channel'].sudo().search([
                ('create_uid', '=', current_user.id),
                ('state', '=', 'published')  # Filter for draft and under review
            ])
            
            under_review_courses = request.env['slide.channel'].sudo().search([
                ('create_uid', '=', current_user.id),
                ('state', '=', 'draft')  # Filter for draft and under review
            ])
            
            all_courses = request.env['slide.channel'].sudo().search([
                ('create_uid', '=', current_user.id),
            ])
            

        course_count = request.env['slide.channel'].sudo().search([
                ('create_uid', '=', current_user.id),
                ('state', 'in', ['draft', 'course_preview','published'])  # Filter for draft and under review
            ])
        approve_course_count = True if published_courses else False
        course_count = True if course_count else False

        

        # Render the template and pass the course lists
        return request.render('custom_web_kreator.nmy_courses_template', {
            'approved_courses': approved_courses,
            'published_courses': published_courses,
            'under_review_courses': under_review_courses,
            'approve_course_count':approve_course_count,
            'course_count':course_count,
            'all_courses':all_courses,
        })

    @http.route('/nmy-courses-partner', type='http', auth='public', website=True)
    def nmycourses_partner(self, **kwargs):
        # Get the logged-in user
        current_user = request.env.user
        partner = current_user.partner_id

        courses = []

        # Check if the user is of type 'customer'
        if partner.user_type in ['partner','internal_user']:
            # Fetch sale orders linked to the customer
            sale_orders = request.env['sale.order'].sudo().search(
                [('partner_id', '=', partner.id), ('state', 'in', ['sale'])])
            print("Sale Orders:", sale_orders)

            # Extract product template IDs from sale order lines
            product_template_ids = sale_orders.mapped('order_line.product_template_id')
            product_names = product_template_ids.mapped('name')
            print("Product Template IDs:", product_template_ids)

            if product_template_ids:
                # Fetch courses where the product_template_ids match
                courses = request.env['slide.channel'].sudo().search(
                    [('name', 'in', product_names)]
                )
                print("Courses:", courses)

        # Render the data page template
        return request.render('custom_web_kreator.nmy_courses_partner', {
            'courses': courses
        })

    # Consume course
    @http.route(['/consume/course/<int:course_id>'], type='http', auth="public", website=True)
    def consume_to_course(self, course_id, **kwargs):
        # You can add custom logic here before redirecting
        course = request.env['slide.channel'].sudo().search([('id', '=', course_id)],limit=1)
        if not course.exists():
            return request.redirect('/404')  # Redirect if the course does not exist
        # Redirect to the target URL
        website_url = course.open_website_url()
        url = website_url['context']['params']['path']
        return request.redirect(url)

    @http.route('/target', type='http', auth='public', website=True)
    def target(self, **kwargs):
        # Get the current logged-in user (res.partner)
        partner = request.env.user.partner_id

        # Fetch all sales targets
        targets = request.env['sale.target'].sudo().search([])

        # Prepare data to pass to the template
        target_data = []
        for target in targets:
            # Filter achievements for the logged-in partner only
            achievement_amount = sum(
                target.achievement_ids.filtered(lambda a: a.partner_id == partner).mapped('amount')
            )

            # Append data to the list
            target_data.append({
                'name': target.name,  # Target name
                'achievement_amount': achievement_amount,  # Achieved amount for this partner
                'target_amount': target.target_amount,  # Total target amount
            })

        values = {
            'targets': target_data,
            'currency_id': request.env.company.currency_id
        }

        # Render the template with prepared data
        return request.render('custom_web_kreator.target_page_template', values)

    @http.route('/npromote', type='http', auth='public', website=True)
    def promote(self, **kwargs):
        print("coming here")
        # Fetch courses where is_training_course is True and sort them alphabetically by name
        promotional_courses = request.env['slide.channel'].sudo().search(
            [('state', '=', 'published')],
            order='name asc'
        )

        # Fetch only courses that have at least one record in promotional_material_ids
        promotional_courses = request.env['slide.channel'].sudo().search([
            ('state', '=', 'published'),
            ('promotional_material_ids', '!=', False)  # Filters only those courses with promotional materials
        ], order='name asc')

        # Render the template and pass the filtered courses
        return request.render('custom_web_kreator.npromote', {
            'promotional_courses': promotional_courses
        })

    # @http.route('/forumsection', type='http', auth='public', website=True)
    # def forumpost(self, **kwargs):
    #     # Render the data page template
    #     return http.request.render('custom_web_kreator.fbpostforum')

    # @http.route('/offers', type='http', auth='public', website=True)
    # def offers(self, **kwargs):
    #     # Render the data page template
    #     return http.request.render('custom_web_kreator.offers_page')

    @http.route('/offers', type='http', auth='public', website=True, methods=['GET', 'POST'])
    def offers(self, **kwargs):

        user_id = request.env.user  # Get the current logged-in user

        # Fetch only courses created by the current user
        product_ids = request.env['slide.channel'].sudo().search([
            ('product_id', '!=', False),
            ('create_uid', '=', user_id.id)  # Filter courses by the logged-in user
        ]).product_id
        discount_ids = request.env['discount.discount'].sudo().search([])
        loyalty_ids = request.env['loyalty.program'].sudo().search([], order='create_date desc')
        values = {
            'loyalty_ids': loyalty_ids,
            'product_ids': product_ids,
            'discount_ids': discount_ids,
            'currency_id': request.env.company.currency_id
        }

        return request.render('custom_web_kreator.offers_page',values)

    @http.route('/offers-create', type='http', auth='public', website=True, methods=['GET', 'POST'])
    def offers_create(self, **kwargs):
        coupon_name = kwargs.get('coupon_name', '')
        discount = kwargs.get('discount', '')
        duration_value = kwargs.get('duration', '')  # e.g., "1_days"
        description = kwargs.get('description', '')
        date_from = kwargs.get('from_date', '')
        date_to = kwargs.get('to_date', '')
        # Step 1: Handle discount field
        discount_record = request.env['discount.discount'].sudo().search([('id', '=', discount)], limit=1)

        # Step 2: Handle duration field
        if '_' in duration_value:
            duration_number, duration_unit = duration_value.split('_', 1)
        else:
            duration_number, duration_unit = duration_value, 'days'  # Default to 'days'

        # Validate and map the duration unit
        duration_unit_mapping = {
            'minute': 'minutes',
            'minutes': 'minutes',
            'hour': 'hours',
            'hours': 'hours',
            'day': 'days',
            'days': 'days',
        }
        duration_unit = duration_unit_mapping.get(duration_unit.lower(), 'days')  # Default to 'days'

        # Search for the duration record
        duration_record = request.env['duration.duration'].sudo().search([
            ('name', '=', duration_number),  # name should be the number (e.g., 1, 2, 7)
            ('duration', '=', duration_unit)  # duration should be the unit (e.g., minutes, hours, days)
        ], limit=1)

        if not duration_record:
            # Create a new duration record if it doesn't exist
            duration_record = request.env['duration.duration'].sudo().create({
                'name': duration_number,  # Store the number as the name (e.g., 1, 2, 7)
                'duration': duration_unit,  # Store the unit as the duration (e.g., minutes, hours, days)
            })

        # Step 3: Create a record in loyalty.program
        loyalty_id = request.env['loyalty.program'].sudo().create({
            'name': coupon_name,
            'program_type': 'promo_code',  # Use the key for "Discount Code"
            'discount_id': discount_record.id,
            'duration_id': duration_record.id,
            'date_from': date_from,
            'date_to': date_to,
        })
        return request.redirect('/offers')


    @http.route('/partner-lead', type='http', auth="user", website=True)
    def partner_lead(self, **kwargs):
        # Get the current logged-in user
        user = request.env.user

        # Get the start and end date from the URL parameters, if provided
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')

        # Convert date strings into datetime objects (if they exist)
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Prepare the domain for filtering sales orders
        domain = [('state', '!=', 'sale')]  # Only fetch orders that are not confirmed (state != 'sale')

        if start_date and end_date:
            domain.extend([
                ('date_order', '>=', start_date),
                ('date_order', '<=', end_date)
            ])

        # Fetch the sale orders based on the domain
        sale_orders = request.env['sale.order'].sudo().search(domain)

        # Fetch visitor data, no date filters for visitors
        visitors = request.env['website.visitor'].sudo().search([])

        # Prepare the context to pass to the template
        context = {
            'user_name': user.name,  # Pass the current user's name
            'sale_orders': sale_orders,  # Pass the filtered sale orders
            'start_date': start_date,  # Pass the start date
            'end_date': end_date,  # Pass the end date
            # 'visitors': visitors,  # Pass the visitor data
        }

        return request.render('custom_web_kreator.partner_lead', context)

    # @http.route('/maintemp', type='http', auth='public', website=True)
    # def maintemp(self, **kwargs):
    #     # Render the data page template
    #     return http.request.render('custom_web_kreator.main_template')

    @http.route('/master', type='http', auth='public', website=True)
    def master(self, **kwargs):
        # Render the data page template
        user = request.env.user
        
        # Count the number of courses created by the user
        course_count = request.env['slide.channel'].sudo().search_count([('create_uid', '=', user.id)])
        approve_course_count = request.env['slide.channel'].sudo().search_count([('create_uid', '=', user.id),('state', '=', 'published')]) > 0
        
    
       
        if course_count:
            return http.request.redirect('/nmy-courses')
        else:
            return http.request.render('custom_web_kreator.master',{'course_count': course_count})

    @http.route('/master_course_detail', type='http', auth='public', website=True)
    def master_course_detail(self, **kwargs):
        partner_commission_rate = (request.env['partner.commission'].sudo().search([],order='create_date desc',  # Order by creation date, latest first
                    limit=1).rate)/100
        direct_commission_rate = (request.env['direct.commission'].sudo().search([],order='create_date desc',  # Order by creation date, latest first
                    limit=1).rate)/100
        values = {
            'partner_commission_rate':partner_commission_rate,
            'direct_commission_rate':direct_commission_rate,
            'currency_id': request.env.company.currency_id
        }
        user = request.env.user
        course_count = request.env['slide.channel'].sudo().search_count([('create_uid', '=', user.id)]) > 0
        approve_course_count = request.env['slide.channel'].sudo().search_count([('create_uid', '=', user.id),('state', '=', 'published')]) > 0
        values['course_count'] = course_count
        values['approve_course_count'] = approve_course_count
        # Render the data page template
        return http.request.render('custom_web_kreator.master_course_detail', values)
 
    @http.route('/master_course_standard', type='http', auth='public', website=True)
    def master_course_standard(self, **kwargs):
        course_data = {
            'course_name': kwargs.get('course_name'),
            'course_description': kwargs.get('course_description'),
            'regular_price': kwargs.get('regular_price'),
            'sales_price': kwargs.get('sales_price'),
        }
        http.request.session['course_data'] = course_data

        user = request.env.user
        course_count = request.env['slide.channel'].sudo().search_count([('create_uid', '=', user.id)]) > 0
        approve_course_count = request.env['slide.channel'].sudo().search_count([('create_uid', '=', user.id),('state', '=', 'published')]) > 0
        # Render the data page template
        return http.request.render('custom_web_kreator.master_course_standard', {'course_data': course_data,
            'course_count':course_count,'approve_course_count':approve_course_count})

    @http.route('/master_term', type='http', auth='public', website=True, methods=['POST'])
    def master_term(self, **kwargs):
        import json

        # Retrieve existing course_data from the session and ensure it's a dictionary
        course_data = http.request.session.get('course_data', '{}')
        print("course_data before update:", course_data)

        if isinstance(course_data, str):
            try:
                course_data = json.loads(course_data)  # Convert string to dictionary
            except json.JSONDecodeError:
                course_data = {}

        # Extract Google Drive links from the form
        google_drive_links = request.httprequest.form.getlist('google_drive_link[]')
        print("google_drive_links",google_drive_links)
        if isinstance(google_drive_links, str):  # If only one link is provided, convert to list
            google_drive_links = [google_drive_links]

        # Update course_data with the new links
        course_data['new_google_drive_links'] = google_drive_links

        # Store updated course_data back in the session
        http.request.session['course_data'] = json.dumps(course_data)  # Store as JSON string

        # Debugging
        print("Updated Course Data:", course_data)

        user = request.env.user
        course_count = request.env['slide.channel'].sudo().search_count([('create_uid', '=', user.id)]) > 0
        approve_course_count = request.env['slide.channel'].sudo().search_count([('create_uid', '=', user.id),('state', '=', 'published')]) > 0
        print('-----------apporve',approve_course_count)
        print('-----------course_count',course_count)
        # Render the data page template
        return http.request.render('custom_web_kreator.master_term', {'course_data': course_data,'course_count':course_count,'approve_course_count':approve_course_count})

    @http.route('/master_welcome', type='http', auth='public', website=True)
    def master_welcome(self, **kwargs):
        # Fetch course_data from session
        course_data = request.session.get('course_data', '{}')
        # If it's a string, try to fix single quotes to double quotes to make it valid JSON
        if isinstance(course_data, str):
            course_data = course_data.replace("'", '"')

        # Now try to load the data as JSON
        try:
            course_data = json.loads(course_data)
        except json.JSONDecodeError:
            course_data = {}

        # Check the agreement value
        agreement = kwargs.get('agreement')

        if agreement == 'agree':
            # Create a record in slide.channel
            SlideChannel = request.env['slide.channel']
            slide_channel = SlideChannel.sudo().create({
                'name': course_data.get('course_name'),
                'description': course_data.get('course_description'),
                'regular_price': course_data.get('regular_price'),
                'sales_price': course_data.get('sales_price'), 
                # Add other fields as required from course_data
            })
            # ✅ Add Google Drive links to google_drive_links1
            google_drive_links = course_data.get('new_google_drive_links', [])  # Extract links from session data
            if google_drive_links:
                google_drive_link_records = [(0, 0, {'link': link}) for link in google_drive_links]
                slide_channel.sudo().write({'google_drive_links1': google_drive_link_records})
            return request.render('custom_web_kreator.master_welcome', {'course_data': course_data,'agreement':agreement})
        elif agreement == 'disagree':
            print(course_data.get('course_name'))
            # Create a record in crm.lead
            CrmLead = request.env['crm.lead']
            crm_lead = CrmLead.sudo().create({
                'name': course_data.get('course_name'),
                'type' : 'lead',
                # Add other fields as required from course_data
            })

            return request.render('custom_web_kreator.master_welcome', {'course_data': course_data, 'agreement': agreement})


        # Get the logged-in user
        current_user = request.env.user
        # Get the partner record associated with the current user
        partner = current_user.partner_id

        
        published_courses = request.env['slide.channel'].sudo().search([
                ('create_uid', '=', current_user.id),
                ('state', '=', 'published')
            ])
        course_count = request.env['slide.channel'].sudo().search([
                ('create_uid', '=', current_user.id),
                ('state', 'in', ['draft', 'course_preview','published'])  # Filter for draft and under review
            ])
        approve_course_count = True if published_courses else False
        course_count = True if course_count else False

        print("||||approve_course_count||||||",approve_course_count)
        print("||||course_count||||||",course_count)
        
        # If the user disagrees, just return the page without creating anything
        return request.render('custom_web_kreator.master_welcome', {'course_data': course_data,'agreement':agreement,'approve_course_count':approve_course_count,
            'course_count':course_count,})
    
    @http.route('/master_income_data', type='http', auth='public', website=True)
    def master_income(self, **kwargs):
        current_user = request.env.user
        partner = current_user.partner_id
        
        # Define date ranges
        today = datetime.today().date()
        # today = fields.Date.today()
        last_7_days = today - timedelta(days=7)
        last_30_days = today - timedelta(days=30)
        
        # Fetch product IDs linked to the user's courses
        courses_obj = request.env['slide.channel']
        orders_obj = request.env['sale.order.line']
        product_ids = courses_obj.sudo().search([('create_uid', '=', current_user.id)]).product_id.ids
        
        # Initialize commission data
        direct_total_commission = partner_total_commission = total_commission = 0.0
        direct_commission_today = partner_commission_today = commission_today = 0.0
        direct_commission_last_7_days = partner_commission_last_7_days = commission_last_7_days = 0.0
        direct_commission_last_30_days = partner_commission_last_30_days = commission_last_30_days = 0.0
        
        if product_ids:
            # Fetch order lines with commissions
            order_lines = orders_obj.sudo().search([
                ('is_commission', '=', True),
                ('state', '=', 'sale'),
                ('product_id', 'in', product_ids)
            ])

            # Separate and calculate commissions by date range
            for line in order_lines:
                order_date = line.create_date.date()
                total_commission += line.direct_commission_amount + line.partner_commission_amount
                direct_total_commission += line.direct_commission_amount 
                partner_total_commission += line.partner_commission_amount
                if order_date == today:
                    commission_today += line.direct_commission_amount + line.partner_commission_amount
                    direct_commission_today += line.direct_commission_amount
                    partner_commission_today += line.partner_commission_amount
                if last_7_days <= order_date <= today:
                    commission_last_7_days += line.direct_commission_amount + line.partner_commission_amount
                    direct_commission_last_7_days += line.direct_commission_amount
                    partner_commission_last_7_days += line.partner_commission_amount
                if last_30_days <= order_date <= today:
                    commission_last_30_days += line.direct_commission_amount + line.partner_commission_amount
                    direct_commission_last_30_days += line.direct_commission_amount
                    partner_commission_last_30_days += line.partner_commission_amount

        # Prepare data for rendering or JSON response
        commission_data = {
            'commission': {
                'total': total_commission,
                'today': commission_today,
                'last_7_days': commission_last_7_days,
                'last_30_days': commission_last_30_days
            },
            'direct_commission': {
                'total': direct_total_commission,
                'today': direct_commission_today,
                'last_7_days': direct_commission_last_7_days,
                'last_30_days': direct_commission_last_30_days
            },
            'partner_commission': {
                'total': partner_total_commission,
                'today': partner_commission_today,
                'last_7_days': partner_commission_last_7_days,
                'last_30_days': partner_commission_last_30_days
            }
        }
        # Render the data page template
        return http.request.render('custom_web_kreator.master_income_data', commission_data)

    # @http.route('/customer', type='http', auth='public', website=True)
    # def customer_courses(self, **kwargs):
    #     print("coming")
    #     # Render the data page template
    #     return http.request.render('custom_web_kreator.customer_courses')

    @http.route('/customer', type='http', auth='public', website=True)
    def customer_courses(self, **kwargs):
        # Get the logged-in user
        current_user = request.env.user
        partner = current_user.partner_id

        courses = []

        # Check if the user is of type 'customer'
        if partner.user_type == 'customer':
            # Fetch sale orders linked to the customer
            sale_orders = request.env['sale.order'].sudo().search([('partner_id', '=', partner.id),('state', 'in', ['sale'])])

            # Extract product template IDs from sale order lines
            product_template_ids = sale_orders.mapped('order_line.product_template_id')
            product_names = product_template_ids.mapped('name')

            if product_template_ids:
                # Fetch courses where the product_template_ids match
                courses = request.env['slide.channel'].sudo().search(
                    [('name', 'in', product_names)]
                )

        # Render the data page template
        return request.render('custom_web_kreator.customer_courses', {
            'courses': courses
        })

    @http.route('/customer_courses_recommend', type='http', auth='public', website=True)
    def customer_courses_recommend(self, **kwargs):
        # Fetch courses where is_training_course is True and sort them alphabetically by name
        recommended_courses = request.env['slide.channel'].sudo().search(
            [('state', '=', 'published')],
            order='name asc'
        )

        # Render the template and pass the courses
        return request.render('custom_web_kreator.customer_courses_recommend', {
            'recommended_courses': recommended_courses
        })

    # @http.route('/custom-page222', type='http', auth="public", website=True)
    # def custom_page(self, **kwargs):
    #     return http.request.render('custom_web_kreator.webtemp', {})

    # @http.route('/creator-dashboard', type='http', auth="public", website=True)
    # def creator_layout(self, **kwargs):
        # return http.request.render('custom_web_kreator.creator_dashboard', {})

    # @http.route('/partner-dashboard', type='http', auth="public", website=True)
    # def partner_layout(self, **kwargs):
    #     return http.request.render('custom_web_kreator.partner_dashboard', {})

    # @http.route('/customer-dashboard', type='http', auth="public", website=True)
    # def customer_layout(self, **kwargs):
    #     return http.request.render('custom_web_kreator.customer_dashboard', {})

    @http.route('/course/search', type='json', auth='public', methods=['POST'])
    def search_courses(self, query=False):
        courses = request.env['slide.channel'].sudo().search([
            ('name', 'ilike', query),
            ('state', '=', 'published')
        ], limit=10)
        result = [{'id': course.id, 'name': course.name} for course in courses]
        return result

    @http.route('/choose-product', type='http', auth="public", website=True)
    def choose_product(self, **kwargs):
        current_user = request.env.user
        partner = current_user.partner_id
        search_query = kwargs.get('name', '').strip()  # Get search query from URL
        selected_course_id = kwargs.get('course_id')  # Get selected course ID from reques

        added_course_ids = request.env['my.product.cart'].sudo().search([
            ('partner_id', '=', partner.id)
        ]).course_id.ids
        domain = [('state', '=', 'published')]  # Base domain to filter published courses
        
        # If a specific course is selected, show only that course
        if selected_course_id:
            domain.append(('id', '=', int(selected_course_id)))
        
        elif search_query:
            domain.append(('name', 'ilike', search_query))  # Filter by course name
        
        # if course_ids:
        #     domain.append(('id', 'not in', course_ids))
        # domain = '[('state', ' = ', 'published'),('course_id', ' in ', course_ids)]'
        courses = request.env['slide.channel'].sudo().search(domain)
        total_courses = len(courses)  # Get total count after filtering
        # for course in courses:

        return request.render('custom_web_kreator.choose_product', {
            'courses': courses,
            'total_courses': total_courses,
            'search_query': search_query,  # Pass search query to maintain input value
            'added_course_ids': added_course_ids,
        })

    @http.route('/choose-product/autocomplete', type='json', auth='public', website=True)
    def choose_product_autocomplete(self, **kwargs):
        # Parse the JSON payload from the raw HTTP request body
        try:
            data = json.loads(request.httprequest.data or '{}')
        except Exception as e:
            data = {}
        search = data.get('search', '')
        print("Search query:", search)

        if not search:
            return []

        current_user = request.env.user
        partner = current_user.partner_id
        course_ids = request.env['my.product.cart'].sudo().search([
            ('partner_id', '=', partner.id)
        ]).course_id.ids

        domain = [
            ('state', '=', 'published'),
            ('id', 'not in', course_ids),
            ('name', 'ilike', search)
        ]
        courses = request.env['slide.channel'].sudo().search(domain, limit=5)
        return [{'id': c.id, 'name': c.name} for c in courses]

    @http.route('/add-to-cart', type='http', auth="user", methods=['POST'], csrf=False)
    def add_to_cart(self, **kwargs):
        current_user = request.env.user
        partner = current_user.partner_id
        course_id = kwargs.get("courseId")
        my_cart_id = request.env['my.product.cart'].sudo().create({
            'course_id': course_id,
            'partner_id': partner.id,
            })
        return request.redirect('/choose-product')


    @http.route('/partner-product', type='http', auth="public", website=True)
    def partner_product(self, **kwargs):
        user = request.env.user
        partner = user.partner_id
        product_cart_ids = request.env['my.product.cart'].sudo().search([('partner_id', '=', partner.id)], order='create_date desc')
        values = {
            'product_cart': product_cart_ids,
            'currency_id': request.env.company.currency_id
        }
        return http.request.render('custom_web_kreator.partner_product', values)

    @http.route('/remove/partner-product', type='http', auth="public", website=True)
    def remove_partner_product(self, **kwargs):
        course_id = kwargs.get('cartCourseID')
        partner_id = kwargs.get('cartPartnerID')
        product_cart_id = request.env['my.product.cart'].sudo().search([
            ('course_id', '=', int(course_id)),
            ('partner_id', '=', int(partner_id))],limit=1)
        if product_cart_id:
            product_cart_id.sudo().unlink()
            print("Product Removed Successfully")
        return request.redirect('/partner-product')



    @http.route('/my-product', type='http', auth="public", website=True)
    def myproduct_new(self, **kwargs):
        return http.request.render('custom_web_kreator.myproduct_new', {})

    @http.route('/promotional', type='http', auth="public", website=True)
    def promotional(self, **kwargs):
        return http.request.render('custom_web_kreator.promotional', {})

    @http.route('/partner-kyc', type='http', auth="public", website=True)
    def partner_kyc(self, **kwargs):
        user = request.env.user
        partner = user.partner_id
        bank_id = request.env['res.partner.bank'].sudo().search([])
        # Check if the user_type of the partner is 'creator'
        if partner.user_type != 'partner':
            print("You do not have permission to update this information. Only 'Partner' users can update.")
            # return request.render('custom_web_kreator.nkyc_partner_template', {
            #     'error': "You do not have permission to update this information. Only 'partner' users can update."
            # })

        if request.httprequest.method == 'POST':
            # Fetch the form data from the POST request
            full_name = kwargs.get('full_name')
            email = kwargs.get('email')
            mobile = kwargs.get('phone')
            document = kwargs.get('document') if kwargs.get('document') != '- Select -' else False
            state_selection = kwargs.get('state_selection', 'under_review')
            partner.write({'state_selection': state_selection})
            # Initialize a dictionary to update partner details
            partner_values = {}

            if full_name:
                partner_values['name'] = full_name
            if email:
                partner_values['email'] = email
            if mobile:
                partner_values['phone'] = mobile
            if document:
                partner_values['select_document'] = document

            # Common fields for document-specific details
            document_number = kwargs.get('document_number')
            document_name = kwargs.get('document_name')  # Dynamic field for document name
            document_front = kwargs.get('file_upload_front')  # Front side upload
            document_back = kwargs.get('file_upload_back')  # Back side upload

            # Map document types to field names
            document_mapping = {
                'passport': {
                    'number_field': 'passport_number',
                    'name_field': 'passport_name',
                    'front_file_field': 'passport_front',
                    'back_file_field': 'passport_back',
                },
                'aadhaar': {
                    'number_field': 'aadhaar_number',
                    'name_field': 'aadhaar_name',
                    'front_file_field': 'aadhaar_front',
                    'back_file_field': 'aadhaar_back',
                },
                'driving_license': {
                    'number_field': 'driving_license_number',
                    'name_field': 'driving_license_name',
                    'front_file_field': 'driving_license_front',
                    'back_file_field': 'driving_license_back',
                },
                'voter_identity_card': {
                    'number_field': 'voter_identity_number',
                    'name_field': 'voter_identity_name',
                    'front_file_field': 'voter_identity_front',
                    'back_file_field': 'voter_identity_back',
                },
            }

            # Handle document-specific updates dynamically
            if document and document in document_mapping:
                doc_fields = document_mapping[document]
                # Update document number and name
                if document_number:
                    partner_values[doc_fields['number_field']] = document_number
                if document_name:
                    partner_values[doc_fields['name_field']] = document_name

                # Upload front side of the document
                if document_front:
                    try:
                        front_data = document_front.read()
                        partner_values[doc_fields['front_file_field']] = base64.b64encode(front_data).decode('utf-8')
                    except Exception as e:
                        print("Front file upload failed",e)
                        # return request.render('custom_web_kreator.error_page_template', {
                        #     'error': f"Front file upload failed: {e}"
                        # })

                # Upload back side of the document
                if document_back:
                    try:
                        back_data = document_back.read()
                        partner_values[doc_fields['back_file_field']] = base64.b64encode(back_data).decode('utf-8')
                    except Exception as e:
                        print("Back file upload failed",e)
                        # return request.render('custom_web_kreator.error_page_template', {
                        #     'error': f"Back file upload failed: {e}"
                        # })

                # Reset other document-related fields
                for doc_type, fields in document_mapping.items():
                    if doc_type != document:  # Reset other document fields
                        partner_values[fields['number_field']] = False
                        partner_values[fields['name_field']] = False
                        partner_values[fields['front_file_field']] = False
                        partner_values[fields['back_file_field']] = False

            # Update pan details
            pan_card_number = kwargs.get('pan_number')
            pan_card_name = kwargs.get('pan_name')
            if pan_card_number:
                partner_values['pan_card_number'] = pan_card_number
            if pan_card_name:
                partner_values['pan_card_name'] = pan_card_name

            pan_card_file = kwargs.get('pan_file')
            if pan_card_file:
                try:
                    file_data = pan_card_file.read()
                    file_content = base64.b64encode(file_data).decode('utf-8')
                    partner_values['pan_card_file'] = file_content
                except Exception as e:
                    print("PAN card file upload failed",e)
                    # return request.render('custom_web_kreator.error_page_template', {
                    #     'error': f"PAN card file upload failed: {e}"
                    # })

            # Update bank details
            account_holder_name = kwargs.get('account_holder_name')
            account_holder_number = kwargs.get('account_number')
            ifsc_code = kwargs.get('ifsc_code')
            upi_mobile_number = kwargs.get('upi_mobile_number')
            bank_id = kwargs.get('bank_id')
            print("bank_name",bank_id)
            if bank_id:
                bank = request.env['res.partner.bank'].sudo().search([('id', '=', bank_id)], limit=1)
                if bank:
                    partner_values['bank_id'] = bank.id  # Assign the bank_id to the partner record
                else:
                    # Handle case where bank with the provided name is not found
                    print("Bank with name not found.")
                    # return request.render('custom_web_kreator.error_page_template', {
                    #     'error': f"Bank with name {bank_name} not found."
                    # })
            if account_holder_name:
                partner_values['Account_holder_name'] = account_holder_name
            if account_holder_number:
                partner_values['Account_holder_number'] = account_holder_number
            if ifsc_code:
                partner_values['ifsc_code'] = ifsc_code
            if upi_mobile_number:
                partner_values['upi_mobile_number'] = upi_mobile_number

            upload_file = kwargs.get('upload_file')
            if upload_file:
                try:
                    file_data = upload_file.read()
                    file_content = base64.b64encode(file_data).decode('utf-8')
                    partner_values['upload_file'] = file_content
                except Exception as e:
                    print("File upload failed",e)
                    # return request.render('custom_web_kreator.error_page_template', {
                    #     'error': f"File upload failed: {e}"
                    # })

            # Write all updates to the partner record
            if partner_values:
                partner.write(partner_values)

            return request.redirect('/partner-kyc')

        # If the request is a GET request (loading the form), fetch partner details to pre-populate
        selected_document = partner.select_document

        document_number = ''
        document_name = ''
        file_upload_front = ''
        file_upload_back = ''
        bank_file = ''
        pan_file = ''
        if selected_document:
            # Dynamically fetch the number and name fields
            document_number = getattr(partner, f"{selected_document}_number", '')
            document_name = getattr(partner, f"{selected_document}_name", '')
            file_upload_front = getattr(partner, f"{selected_document}_front", None)
            file_upload_back = getattr(partner, f"{selected_document}_back", None)

            if file_upload_front:
                file_upload_front = base64.b64encode(file_upload_front).decode('utf-8')
            else:
                print("No data for file_upload_front")
                file_upload_front = ''

            if file_upload_back:
                file_upload_back = base64.b64encode(file_upload_back).decode('utf-8')
            else:
                print("No data for file_upload_back")
                file_upload_back = ''

        if partner.upload_file:
            bank_file = base64.b64encode(partner.upload_file).decode('utf-8')
        if partner.pan_card_file:
            pan_file = base64.b64encode(partner.pan_card_file).decode('utf-8')

        values = {
            'partner_id': partner,
            'partner_name': partner.name,
            'partner_email': partner.email,
            'partner_phone': partner.phone,
            'document': partner.select_document,
            'document_number': document_number,
            'document_name': document_name,
            "file_upload_front": file_upload_front,
            "file_upload_back": file_upload_back,
            'account_holder_name': partner.Account_holder_name,
            'account_number': partner.Account_holder_number,
            'bank_id': bank_id if bank_id else '',# This will render the bank's name in the template
            'ifsc_code': partner.ifsc_code,
            'upi_mobile_number': partner.upi_mobile_number,
            'bank_file': bank_file,
            'pan_number': partner.pan_card_number,
            'pan_name': partner.pan_card_name,
            'pan_file': pan_file,
            'state_selection' : partner.state_selection,
        }
        return http.request.render('custom_web_kreator.nkyc_partner_template', values)

    # @http.route('/boot5', type='http', auth="public", website=True)
    # def boot5(self, **kwargs):
    #     return http.request.render('custom_web_kreator.bootnav', {})

    # @http.route('/partner-lead', type='http', auth="public", website=True)
    # def partner_lead(self, **kwargs):
    #     return http.request.render('custom_web_kreator.partner_lead', {})

    # Search Coupons
    @http.route('/coupons/search', type='json', auth='public', methods=['POST'])
    def search_coupons(self, query=False):
        coupons = request.env['loyalty.program'].sudo().search([
            ('name', 'ilike', query),
            ('program_type', '=', 'promo_code')
        ], limit=10)
        result = [{'id': coupon.id, 'name': coupon.name} for coupon in coupons]
        return result

    @http.route('/offers-coupon', type='http', auth="public", website=True)
    def offers_coupon(self, **kwargs):
        search_query = kwargs.get('name', '').strip()  # Get search query from URL
        domain = [('program_type', '=', 'promo_code')]  # Base domain to filter Discount coupons
        selected_coupon_id = kwargs.get('coupon_id')  # Get selected coupon ID from reques
        # If a specific course is selected, show only that course
        
        if selected_coupon_id:
            domain.append(('id', '=', int(selected_coupon_id)))
        
        elif search_query:
            domain.append(('name', 'ilike', search_query))  # Filter by course name

        loyalty_ids = request.env['loyalty.program'].sudo().search(domain, order='create_date desc')
        values = {
            'loyalty_ids': loyalty_ids,
            'currency_id': request.env.company.currency_id,
            'search_query': search_query  # Pass search query to maintain input value
        }
        return http.request.render('custom_web_kreator.coupon_offers_page', values)

    @http.route('/choose-product-detail', type='http', auth="public", website=True)
    def choose_product_detail(self, **kwargs):
        course_id = kwargs.get('course_id')  # Get course ID from URL
        if course_id:
            course = request.env['slide.channel'].sudo().browse(int(course_id))  # Fetch course details

            current_user = request.env.user
            partner = current_user.partner_id

            added_course_ids = request.env['my.product.cart'].sudo().search([
                ('partner_id', '=', partner.id)
            ]).course_id.ids

        currency = course.currency_id
        return request.render('custom_web_kreator.choose_product_detail', {
            'course': course,  # Pass course details to template
            'currency_name': currency.name if currency else 'INR',
            'added_course_ids': added_course_ids,
        })

    @http.route('/creator-lead', type='http', auth="public", website=True)
    def creator_lead(self, **kwargs):
        # Get the current logged-in user
        user = request.env.user

        # Get the start and end date from the URL parameters, if provided
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')

        # Convert date strings into datetime objects (if they exist)
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Prepare the domain for filtering sales orders
        domain = [('state', '!=', 'sale')]  # Only fetch orders that are not confirmed (state != 'sale')

        if start_date:
            domain.append(('date_order', '>=', start_date))  # Filter based on start date
        if end_date:
            domain.append(('date_order', '<=', end_date))  # Filter based on end date

        # Fetch the sale orders based on the domain
        sale_orders = request.env['sale.order'].sudo().search(domain)

        # Fetch visitor data, no date filters for visitors
        visitors = request.env['website.visitor'].sudo().search([])

        # Prepare the context to pass to the template
        context = {
            'user_name': user.name,  # Pass the current user's name
            'sale_orders': sale_orders,  # Pass the filtered sale orders
            'start_date': start_date,  # Pass the start date
            'end_date': end_date,  # Pass the end date
            # 'visitors': visitors,  # Pass the visitor data
        }

        return request.render('custom_web_kreator.creator_lead', context)


    # @http.route('/partner_income_data', type='http', auth='public', website=True)
    # def partner_income(self, **kwargs):
    #     # Render the data page template
    #     return http.request.render('custom_web_kreator.partner_income_data')

    # @http.route('/creator-landing-page', type='http', auth='public', website=True)
    # def creator_landing_page(self, **kwargs):
    #     # Render the data page template
    #     return http.request.render('custom_web_kreator.creator_landing_page')


    #Pass Data through JS
    @http.route('/creator-landing-page-js', type='http', auth='public', methods=['POST'], csrf=False)
    def handle_form_data(self, **kwargs):
        # Get the list from the form_data field
        # Banner Information
        if kwargs.get('form_data'):
            try:
                print("\n\n\n=========1==============",kwargs.get('form_data'))
                form_data_json = kwargs.get('form_data')
                form_data_list = json.loads(form_data_json) if form_data_json else []
                # Unpack the list values
                course_id = request.env['slide.channel'].sudo().search([('id', '=', form_data_list[1])],limit=1)
                upload_file = kwargs.get('upload_file')
                file_content = False
                if upload_file:
                    file_content = upload_file.read()
                    file_name = upload_file.filename
                if course_id:
                    course_id.sudo().write({
                        'creator_name':form_data_list[0],
                        'main_heading':course_id.name,
                        'p2':form_data_list[2],
                        'combination_id':int(form_data_list[3]),
                        'image_icon': base64.b64encode(file_content),
                    })
                    return request.make_response(
                        json.dumps({'result': {'success': True, 'message': 'Data received successfully!'}}),
                        headers=[('Content-Type', 'application/json')]
                    )
                else:
                    return request.make_response(
                        json.dumps({'result': {'success': False, 'message': 'Course not found!'}}),
                        headers=[('Content-Type', 'application/json')]
                    )
            except Exception as e:
                return request.make_response(
                    json.dumps({'result': {'success': False, 'message': f'An unexpected error occurred: {str(e)}'}}),
                    headers=[('Content-Type', 'application/json')]
                )
        # USP Data Updating
        elif kwargs.get('usp_data'):
            try:
                print("\n\n\n=========2==============", kwargs.get('usp_data'))
                # Parse JSON data
                form_data_json = kwargs.get('usp_data')
                form_data_list = json.loads(form_data_json) if form_data_json else []

                # Search for the course
                course_id = request.env['slide.channel'].sudo().search([('id', '=', form_data_list[0])], limit=1)

                if course_id:
                    # Update fields c1 and c2
                    course_id.sudo().write({
                        'c1': form_data_list[1] if len(form_data_list) > 1 else '',
                        'c2': form_data_list[2] if len(form_data_list) > 2 else '',
                    })

                    return request.make_response(
                        json.dumps({'result': {'success': True, 'message': 'Data received successfully!'}}),
                        headers=[('Content-Type', 'application/json')]
                    )
                else:
                    return request.make_response(
                        json.dumps({'result': {'success': False, 'message': 'Course not found!'}}),
                        headers=[('Content-Type', 'application/json')]
                    )
            except Exception as e:
                return request.make_response(
                    json.dumps({'result': {'success': False, 'message': f'An unexpected error occurred: {str(e)}'}}),
                    headers=[('Content-Type', 'application/json')]
                )
        
        # About Course Data Updating
        elif kwargs.get('aboutCourse_data'):
            try:
                print("\n\n\n=========3==============", kwargs.get('aboutCourse_data'))
                # Parse JSON data
                form_data_json = kwargs.get('aboutCourse_data')
                form_data_list = json.loads(form_data_json) if form_data_json else []

                # Search for the course
                course_id = request.env['slide.channel'].sudo().search([('id', '=', form_data_list[0])], limit=1)
                para_lines = []
                for para in form_data_list[1:]:
                    vals = {
                        'p1':para,
                    }
                    para_lines.append((0, 0, vals))
                if course_id:
                    course_id.sudo().write({'course_line_ids': para_lines})
                    return request.make_response(
                        json.dumps({'result': {'success': True, 'message': 'Data received successfully!'}}),
                        headers=[('Content-Type', 'application/json')]
                    )
                else:
                    return request.make_response(
                        json.dumps({'result': {'success': False, 'message': 'Course not found!'}}),
                        headers=[('Content-Type', 'application/json')]
                    )
            except Exception as e:
                return request.make_response(
                    json.dumps({'result': {'success': False, 'message': f'An unexpected error occurred: {str(e)}'}}),
                    headers=[('Content-Type', 'application/json')]
                )

        # What Can I Learn From This Data Updating
        elif kwargs.get('learnFromThisParas_data'):
            try:
                print("\n\n\n=========4==============", kwargs.get('learnFromThisParas_data'))
                # Parse JSON data
                form_data_json = kwargs.get('learnFromThisParas_data')
                form_data_list = json.loads(form_data_json) if form_data_json else []

                # Search for the course
                course_id = request.env['slide.channel'].sudo().search([('id', '=', form_data_list[0])], limit=1)
                para_lines = []
                for para in form_data_list[1:]:
                    vals = {
                        'c1':para,
                    }
                    para_lines.append((0, 0, vals))
                if course_id:
                    course_id.sudo().write({'individual_line_ids': para_lines})
                    return request.make_response(
                        json.dumps({'result': {'success': True, 'message': 'Data received successfully!'}}),
                        headers=[('Content-Type', 'application/json')]
                    )
                else:
                    return request.make_response(
                        json.dumps({'result': {'success': False, 'message': 'Course not found!'}}),
                        headers=[('Content-Type', 'application/json')]
                    )
            except Exception as e:
                return request.make_response(
                    json.dumps({'result': {'success': False, 'message': f'An unexpected error occurred: {str(e)}'}}),
                    headers=[('Content-Type', 'application/json')]
                )
        
        # Course Curriculum Data Updating
        elif kwargs.get('curriculum_data'):
            try:
                print("\n\n\n=========5==============", kwargs.get('curriculum_data'))
                # Parse JSON data
                form_data_json = kwargs.get('curriculum_data')
                form_data_list = json.loads(form_data_json) if form_data_json else []
                # Search for the course
                course_id = request.env['slide.channel'].sudo().search([('id', '=', form_data_list[0]['courseID'])], limit=1)
                para_lines = []
                for para in form_data_list[1:]:
                    vals = {
                        'h1':para['title'],
                        'c1':para['content'],
                    }
                    para_lines.append((0, 0, vals))
                if course_id:
                    course_id.sudo().write({'line_ids': para_lines})
                    return request.make_response(
                        json.dumps({'result': {'success': True, 'message': 'Data received successfully!'}}),
                        headers=[('Content-Type', 'application/json')]
                    )
                else:
                    return request.make_response(
                        json.dumps({'result': {'success': False, 'message': 'Course not found!'}}),
                        headers=[('Content-Type', 'application/json')]
                    )
            except Exception as e:
                return request.make_response(
                    json.dumps({'result': {'success': False, 'message': f'An unexpected error occurred: {str(e)}'}}),
                    headers=[('Content-Type', 'application/json')]
                )
        
        # About Me Data Updating
        elif kwargs.get('aboutMe_data'):
            try:
                print("\n\n\n=========6==============", kwargs.get('aboutMe_data'))
                # Parse JSON data
                form_data_json = kwargs.get('aboutMe_data')
                form_data_list = json.loads(form_data_json) if form_data_json else []

                # Search for the course
                course_id = request.env['slide.channel'].sudo().search([('id', '=', form_data_list[0]['courseID'])], limit=1)
                para_lines = []
                upload_file = kwargs.get('aboutme_upload_file')
                file_content = False
                if upload_file:
                    file_content = upload_file.read()
                for para in form_data_list[1:]:
                    vals = {
                        'p1':para['content'],
                    }
                    para_lines.append((0, 0, vals))
                if course_id:
                    course_id.sudo().write({
                        'about_me_line_ids': para_lines,
                        'm1': form_data_list[0]['facebook'],
                        'm2': form_data_list[0]['mediaX'],
                        'm3': form_data_list[0]['linkedIn'],
                        'm4': form_data_list[0]['youtube'],
                        'm5': form_data_list[0]['instagram'],
                        'm6': form_data_list[0]['pininterest'],
                        'my_image_icon': base64.b64encode(file_content),
                    })
                    return request.make_response(
                        json.dumps({'result': {'success': True, 'message': 'Data received successfully!'}}),
                        headers=[('Content-Type', 'application/json')]
                    )
                else:
                    return request.make_response(
                        json.dumps({'result': {'success': False, 'message': 'Course not found!'}}),
                        headers=[('Content-Type', 'application/json')]
                    )
            except Exception as e:
                return request.make_response(
                    json.dumps({'result': {'success': False, 'message': f'An unexpected error occurred: {str(e)}'}}),
                    headers=[('Content-Type', 'application/json')]
                )
        
        # Who Should Take This Course? Data Updating
        elif kwargs.get('audience_data'):
            try:
                print("\n\n\n=========7==============", kwargs.get('audience_data'))
                # Parse JSON data
                form_data_json = kwargs.get('audience_data')
                form_data_list = json.loads(form_data_json) if form_data_json else []

                # Search for the course
                course_id = request.env['slide.channel'].sudo().search([('id', '=', form_data_list[0]['courseID'])], limit=1)
                para_lines = []
                for para in form_data_list[1:]:
                    para_lines.append(para)
                if course_id:
                    course_id.sudo().write({
                        'course_ids': [(6, 0, para_lines)],
                    })
                    return request.make_response(
                        json.dumps({'result': {'success': True, 'message': 'Data received successfully!'}}),
                        headers=[('Content-Type', 'application/json')]
                    )
                else:
                    return request.make_response(
                        json.dumps({'result': {'success': False, 'message': 'Course not found!'}}),
                        headers=[('Content-Type', 'application/json')]
                    )
            except Exception as e:
                return request.make_response(
                    json.dumps({'result': {'success': False, 'message': f'An unexpected error occurred: {str(e)}'}}),
                    headers=[('Content-Type', 'application/json')]
                )
        
        # Our Students - Testimonials Data Updating
        elif kwargs.get('testimonials_data'):
            try:
                print("\n\n\n=========8==============", kwargs.get('testimonials_data'))
                # Parse JSON data
                form_data_json = kwargs.get('testimonials_data')
                form_data_list = json.loads(form_data_json) if form_data_json else []

                # Search for the course
                course_id = request.env['slide.channel'].sudo().search([('id', '=', form_data_list[0]['courseID'])], limit=1)
                para_lines = []
                file_content = False
                i = 0
                for para in form_data_list[1:]:
                    upload_file = kwargs.get('upload_file_'+str(i))
                    file_content = upload_file.read()
                    if para['testimonial_type'] == 'text':
                        vals = {
                            'name':para['name'],
                            'content_type':para['testimonial_type'],
                            'p1':para['text'],
                            'rating':para['rating'],
                            'image': base64.b64encode(file_content),
                        }
                    else:
                        vals = {
                            'name':para['name'],
                            'content_type':para['testimonial_type'],
                            'p1':para['content'],
                            'rating':para['rating'],
                            'image': base64.b64encode(file_content),
                        }
                    i +=1
                    para_lines.append((0, 0, vals))
                if course_id:
                    course_id.sudo().write({
                        'student_line_ids': para_lines,
                    })
                    return request.make_response(
                        json.dumps({'result': {'success': True, 'message': 'Data received successfully!'}}),
                        headers=[('Content-Type', 'application/json')]
                    )
                else:
                    return request.make_response(
                        json.dumps({'result': {'success': False, 'message': 'Course not found!'}}),
                        headers=[('Content-Type', 'application/json')]
                    )
            except Exception as e:
                return request.make_response(
                    json.dumps({'result': {'success': False, 'message': f'An unexpected error occurred: {str(e)}'}}),
                    headers=[('Content-Type', 'application/json')]
                )
        
        # FAQs Data Updating
        elif kwargs.get('faq_data'):
            try:
                print("\n\n\n=========9==============", kwargs.get('faq_data'))
                # Parse JSON data
                form_data_json = kwargs.get('faq_data')
                form_data_list = json.loads(form_data_json) if form_data_json else []

                # Search for the course
                course_id = request.env['slide.channel'].sudo().search([('id', '=', form_data_list[0]['courseID'])], limit=1)
                para_lines = []
                for para in form_data_list[1:]:
                    vals = {
                        'q1':para['question'],
                        'a1':para['answer'],
                    }
                    para_lines.append((0, 0, vals))
                if course_id:
                    course_id.sudo().write({
                        'faq_ids': para_lines
                    })
                    return request.make_response(
                        json.dumps({'result': {'success': True, 'message': 'Data received successfully!'}}),
                        headers=[('Content-Type', 'application/json')]
                    )
                else:
                    return request.make_response(
                        json.dumps({'result': {'success': False, 'message': 'Course not found!'}}),
                        headers=[('Content-Type', 'application/json')]
                    )
            except Exception as e:
                return request.make_response(
                    json.dumps({'result': {'success': False, 'message': f'An unexpected error occurred: {str(e)}'}}),
                    headers=[('Content-Type', 'application/json')]
                )

        # Footer Information Data Updating
        elif kwargs.get('completeGuide_data'):
            try:
                print("\n\n\n=========10==============", kwargs.get('completeGuide_data'))
                # Parse JSON data
                form_data_json = kwargs.get('completeGuide_data')
                form_data_list = json.loads(form_data_json) if form_data_json else []

                # Search for the course
                course_id = request.env['slide.channel'].sudo().search([('id', '=', form_data_list[0])], limit=1)
                para_lines = []
                file_content = False
                upload_file = kwargs.get('completeGuide_file')
                if upload_file:
                    file_content = upload_file.read()
                if course_id:
                    course_id.sudo().write({
                        'c11': form_data_list[1],
                        'image1':base64.b64encode(file_content),
                    })
                    return request.make_response(
                        json.dumps({'result': {'success': True, 'message': 'Data received successfully!'}}),
                        headers=[('Content-Type', 'application/json')]
                    )
                else:
                    return request.make_response(
                        json.dumps({'result': {'success': False, 'message': 'Course not found!'}}),
                        headers=[('Content-Type', 'application/json')]
                    )
            except Exception as e:
                return request.make_response(
                    json.dumps({'result': {'success': False, 'message': f'An unexpected error occurred: {str(e)}'}}),
                    headers=[('Content-Type', 'application/json')]
                )
        
        # Certificate Data Updating
        elif kwargs.get('certificate_data'):
            try:
                print("\n\n\n=========11==============", kwargs.get('certificate_data'))
                # Parse JSON data
                form_data_json = kwargs.get('certificate_data')
                form_data_list = json.loads(form_data_json) if form_data_json else []

                # Search for the course
                course_id = request.env['slide.channel'].sudo().search([('id', '=', form_data_list[0])], limit=1)
                para_lines = []
                file_content = False
                upload_file = kwargs.get('certificate_upload_file')
                if upload_file:
                    file_content = upload_file.read()
                if course_id:
                    if form_data_list[1] == 'yes':
                        course_id.sudo().write({
                            'is_this_certificate_course': 'yes',
                            'issued_by': form_data_list[2],
                            'upload_signature': base64.b64encode(file_content),
                            })
                    else:
                        course_id.sudo().write({
                            'is_this_certificate_course': 'no',
                            })
                    return request.make_response(
                        json.dumps({'result': {'success': True, 'message': 'Data received successfully!'}}),
                        headers=[('Content-Type', 'application/json')]
                    )
                else:
                    return request.make_response(
                        json.dumps({'result': {'success': False, 'message': 'Course not found!'}}),
                        headers=[('Content-Type', 'application/json')]
                    )
            except Exception as e:
                return request.make_response(
                    json.dumps({'result': {'success': False, 'message': f'An unexpected error occurred: {str(e)}'}}),
                    headers=[('Content-Type', 'application/json')]
                )
        
        # Course Thumbnail Data Updating
        elif kwargs.get('courseThumbnail_data'):
            try:
                print("\n\n\n=========12==============", kwargs.get('courseThumbnail_data'))
                # Parse JSON data
                form_data_json = kwargs.get('courseThumbnail_data')
                form_data_list = json.loads(form_data_json) if form_data_json else []

                # Search for the course
                course_id = request.env['slide.channel'].sudo().search([('id', '=', form_data_list[0])], limit=1)
                file_content = False
                upload_file = kwargs.get('courseThumbnail_upload_file')
                if upload_file:
                    file_content = upload_file.read()
                if course_id:
                    course_id.sudo().write({
                        'image_1920': base64.b64encode(file_content),
                        })
                    return request.make_response(
                        json.dumps({'result': {'success': True, 'message': 'Data received successfully!'}}),
                        headers=[('Content-Type', 'application/json')]
                    )
                else:
                    return request.make_response(
                        json.dumps({'result': {'success': False, 'message': 'Course not found!'}}),
                        headers=[('Content-Type', 'application/json')]
                    )
            except Exception as e:
                return request.make_response(
                    json.dumps({'result': {'success': False, 'message': f'An unexpected error occurred: {str(e)}'}}),
                    headers=[('Content-Type', 'application/json')]
                )
        

        else:
            return request.make_response(
                json.dumps({'result': {'success': False, 'message': 'No data provided!'}}),
                headers=[('Content-Type', 'application/json')]
            )
        

    @http.route('/creator-landing-page', type='http', auth='public', website=True, csrf=True, methods=['GET', 'POST'])
    def creator_landing_page(self, **post):
        # Fetch the current logged-in user
        user = http.request.env.user
        courses = request.env['slide.channel'].sudo().search([('create_uid', '=', user.id)])  # Fetch user's courses
        combination_id = request.env['colour.combination'].sudo().search([])  # Fetch colour combination

        # Fetch the course ID from query parameters
        course_id = post.get('course_id')
        selected_course = request.env['slide.channel'].sudo().browse(int(course_id)) if course_id else None

        # Fetch the course based on the provided ID or fall back to the default course
        course = request.env['slide.channel'].sudo().browse(int(course_id)) if course_id else request.env[
            'slide.channel'].sudo().browse(1)
        if not course.exists():
            return request.not_found()
        # Fetch target audience options from course.course model
        target_audience_options = request.env['course.course'].sudo().search(
            [])  # Assuming 'course.course' is the model
        if http.request.httprequest.method == 'POST':
            # Handle POST request
            description = post.get('shortDescription')  # Get the description from the form
            primaryColor = post.get('primaryColor')  # Get the description from the form
            secondaryColor = post.get('secondaryColor')  # Get the description from the form
            section_upload_files = http.request.httprequest.files.get('uploadFile')  # Get the uploaded file
            creator_name = post.get('creatorName')
            ups_name1 = post.get('ups_content1')
            ups_name2 = post.get('ups_content2')
            ups_name3 = post.get('ups_content3')
            ups_name4 = post.get('ups_content4')
            face_book = post.get('face_book')
            social_media_x = post.get('social_media_x')
            linked_in = post.get('linked_in')
            you_tube = post.get('you_tube')
            instagram = post.get('instagram')
            pinInterest = post.get('pinInterest')
            aboutme_upload_files = http.request.httprequest.files.get('creator_image_file')  # Get the uploaded file
            shortDescription = post.get('shortDescription')
            certificate_course = post.get('certificate_course')
            certificate = post.get('certificate')

            name = post.get('name')
            testimonial_type = post.get('testimonial_type')
            text_value = post.get('text')  # For 'text' type
            testimonial_content = post.get('content')  # For 'video' type
            rating = post.get('rating')
            upload_file = http.request.httprequest.files.get('pushFile')  # Uploaded file
            guide_uploadFiless = http.request.httprequest.files.get('uploadFiless')  # Uploaded file
            certificate_File = http.request.httprequest.files.get('certificate_File')  # Uploaded file
            upload_thumbnail = http.request.httprequest.files.get('upload_thumbnail')  # Uploaded file

            # Handle FAQ input
            faq_data = []
            for key in post:
                if key.startswith('question') and post.get(key):
                    question_number = key.replace('question', '')  # Extract the question number
                    question = post.get(f'question{question_number}')
                    answer = post.get(f'answer{question_number}', '')  # Default to empty string if no answer provided
                    faq_data.append({'q1': question, 'a1': answer})

            # Prepare data for One2many relation
            faq_lines = [(0, 0, faq) for faq in faq_data]

            # Prepare data for the `our.student.line` model
            student_line_data = {
                'name': name,
                'content_type': testimonial_type,
                'p1': text_value or testimonial_content,
                'rating': rating,
            }

            if upload_file:
                # Encode the uploaded file as base64
                image_data = base64.b64encode(upload_file.read())
                student_line_data['image'] = image_data

            if guide_uploadFiless:
                # Encode the uploaded file as base64
                guide_uploadFile = guide_uploadFiless.read()
                course.sudo().write({'image1': base64.b64encode(guide_uploadFile)})
            if certificate_File:
                # Encode the uploaded file as base64
                certificate_File_upload = certificate_File.read()
                course.sudo().write({'upload_signature': base64.b64encode(certificate_File_upload)})
            if upload_thumbnail:
                # Encode the uploaded file as base64
                upload_thumbnail_file = upload_thumbnail.read()
                course.sudo().write({'image_1920': base64.b64encode(upload_thumbnail_file)})

            course_curriculum_data = post.get('course_curriculum_data')  # Retrieve lines data
            print("course_curriculum_data", course_curriculum_data)
            try:
                curriculum_lines = json.loads(course_curriculum_data) if course_curriculum_data else []
            except json.JSONDecodeError:
                curriculum_lines = []
            # Update the `slide.channel` with the FAQ data
            if course:
                course.sudo().write({
                    'faq_ids': faq_lines,
                    # Add lines to One2many
                    'line_ids': [(0, 0, {'h1': line['title'], 'c1': line['content']}) for line in curriculum_lines],
                    'student_line_ids': [(0, 0, student_line_data)]
                })

            selected_target_audiences = request.httprequest.form.getlist('target_audience[]')
            if isinstance(selected_target_audiences, str):
                selected_target_audiences = [
                    selected_target_audiences]  # Ensure it's a list if only one checkbox is selected

            # Fetch the course model for updating the many2many field
            if selected_target_audiences:
                audience_courses = request.env['course.course'].sudo().search(
                    [('name', 'in', selected_target_audiences)])
                # Update the 'course_ids' field of the 'slide.channel' model
                courses.sudo().write({
                    'course_ids': [(6, 0, audience_courses.ids)]  # Update the many2many field
                })

            about_course_paragraphs = [
                post[key] for key in post if key.startswith('paragraph') and post[key] not in [None, '']
            ]

            # Collect all dynamic paragraphs for `individual_line_ids`
            individual_paragraphs = [
                post[key] for key in post if key.startswith('individual_paragraph') and post[key] not in [None, '']
            ]

            # Initialize the updates dictionary
            updates = {
                'p2': description,
                'primary_color': primaryColor,
                'secondary_color': secondaryColor,
                'creator_name': creator_name,
                'main_heading': 'THE COMPLETE GUIDE TO STARTING UP',
                'course_title': 'ABOUT THIS COURSE',
                'h1': 'WHAT AN INDIVIDUAL CAN LEARN FROM THIS?',
                'h2': 'COURSE CURRICULUM',
                'h3': 'ABOUT ME',
                'h6': 'WHO SHOULD TAKE THIS COURSE ?',
                'h7': 'FROM OUR STUDENTS',
                'h5': 'FREQUENTLY ASKED QUESTIONS',
                'h4': 'The Complete Guide To Starting Up',
                'c1': ups_name1,
                'c2': ups_name2,
                'c3': ups_name3,
                'c4': ups_name4,
                'm1': face_book,
                'm2': social_media_x,
                'm3': linked_in,
                'm4': you_tube,
                'm5': instagram,
                'm6': pinInterest,
                'c11': shortDescription,
                'is_this_certificate_course': certificate_course,
                'issued_by': certificate,
            }

            # Remove fields with empty values (`None`, `''`, etc.)
            updates = {key: value for key, value in updates.items() if value not in [None, '']}
            # Update the course if it exists
            if course.exists():
                course.sudo().write({
                    **updates
                })

            if section_upload_files:
                # Save the uploaded image
                image_data = section_upload_files.read()
                course.sudo().write({'image_icon': base64.b64encode(image_data)})
            if aboutme_upload_files:
                about_me_file = aboutme_upload_files.read()
                course.sudo().write({'my_image_icon': base64.b64encode(about_me_file)})
            # Add `about.course` dynamic paragraphs
            if about_course_paragraphs:
                course.sudo().write({
                    'course_line_ids': [(0, 0, {'p1': paragraph}) for paragraph in about_course_paragraphs]
                })

            # Add dynamic paragraphs to `individual_line_ids`
            if individual_paragraphs:
                course.sudo().write({
                    'individual_line_ids': [(0, 0, {'c1': paragraph}) for paragraph in individual_paragraphs]
                })
        # Render the page for GET request
        print("course", course.name)
        return http.request.render('custom_web_kreator.creator_landing_page_js', {
            'user_name': user.name,
            'courses': courses,
            'combinations':combination_id,
            'selected_course': selected_course,
            'description': course.p2,
            'target_audience_options': target_audience_options
        })

    @http.route('/edit-landing-page', type='http', auth='public', website=True, csrf=True, methods=['GET', 'POST'])
    def edit_landing_page(self, course_id=False, **post):
        # Fetch the current logged-in user
        if not course_id:
            raise NotFound("Course ID is missing.")
        user = http.request.env.user
        # courses = request.env['slide.channel'].sudo().search([('create_uid', '=', user.id)])  # Fetch user's courses

        # Fetch the course ID from query parameters
        # course_id = post.get('course_id')
        selected_course = request.env['slide.channel'].sudo().browse(int(course_id)) if course_id else None
        course_lines_p1 = selected_course.course_line_ids.mapped('p1') if selected_course else []
        course_lines_p1 = [
            {"index": idx, "value": paragraph}
            for idx, paragraph in enumerate(course_lines_p1, start=1)
        ]
        individual_line_c1 = selected_course.individual_line_ids.mapped('c1') if selected_course else []
        individual_line_c1 = [
            {"index": idx, "value": paragraph}
            for idx, paragraph in enumerate(individual_line_c1, start=1)
        ]
        # Fetch the course based on the provided ID or fall back to the default course
        course = request.env['slide.channel'].sudo().browse(int(course_id)) if course_id else request.env[
            'slide.channel'].sudo().browse(1)
        if not course.exists():
            return request.not_found()
        # Fetch target audience options from course.course model
        target_audience_options = request.env['course.course'].sudo().search(
            [])  # Assuming 'course.course' is the model
        if http.request.httprequest.method == 'POST':
            # Handle POST request
            description = post.get('shortDescription')  # Get the description from the form
            section_upload_files = http.request.httprequest.files.get('uploadFile')  # Get the uploaded file
            creator_name = post.get('creatorName')
            ups_name1 = post.get('ups_content1')
            ups_name2 = post.get('ups_content2')
            ups_name3 = post.get('ups_content3')
            ups_name4 = post.get('ups_content4')
            face_book = post.get('face_book')
            social_media_x = post.get('social_media_x')
            linked_in = post.get('linked_in')
            you_tube = post.get('you_tube')
            instagram = post.get('instagram')
            pinInterest = post.get('pinInterest')
            aboutme_upload_files = http.request.httprequest.files.get('creator_image_file')  # Get the uploaded file
            shortDescription = post.get('shortDescription')
            certificate_course = post.get('certificate_course')
            certificate = post.get('certificate')

            name = post.get('name')
            testimonial_type = post.get('testimonial_type')
            text_value = post.get('text')  # For 'text' type
            testimonial_content = post.get('content')  # For 'video' type
            rating = post.get('rating')
            upload_file = http.request.httprequest.files.get('pushFile')  # Uploaded file
            guide_uploadFiless = http.request.httprequest.files.get('uploadFiless')  # Uploaded file
            certificate_File = http.request.httprequest.files.get('certificate_File')  # Uploaded file
            upload_thumbnail = http.request.httprequest.files.get('upload_thumbnail')  # Uploaded file

            # Handle FAQ input
            faq_data = []
            for key in post:
                if key.startswith('question') and post.get(key):
                    question_number = key.replace('question', '')  # Extract the question number
                    question = post.get(f'question{question_number}')
                    answer = post.get(f'answer{question_number}', '')  # Default to empty string if no answer provided
                    faq_data.append({'q1': question, 'a1': answer})

            # Prepare data for One2many relation
            faq_lines = [(0, 0, faq) for faq in faq_data]

            # Prepare data for the `our.student.line` model
            student_line_data = {
                'name': name,
                'content_type': testimonial_type,
                'p1': text_value or testimonial_content,
                'rating': rating,
            }

            if upload_file:
                # Encode the uploaded file as base64
                image_data = base64.b64encode(upload_file.read())
                student_line_data['image'] = image_data

            if guide_uploadFiless:
                # Encode the uploaded file as base64
                guide_uploadFile = guide_uploadFiless.read()
                course.sudo().write({'image1': base64.b64encode(guide_uploadFile)})
            if certificate_File:
                # Encode the uploaded file as base64
                certificate_File_upload = certificate_File.read()
                course.sudo().write({'upload_signature': base64.b64encode(certificate_File_upload)})
            if upload_thumbnail:
                # Encode the uploaded file as base64
                upload_thumbnail_file = upload_thumbnail.read()
                course.sudo().write({'image_1920': base64.b64encode(upload_thumbnail_file)})

            course_curriculum_data = post.get('course_curriculum_data')  # Retrieve lines data
            try:
                curriculum_lines = json.loads(course_curriculum_data) if course_curriculum_data else []
            except json.JSONDecodeError:
                curriculum_lines = []
            # Update the `slide.channel` with the FAQ data
            if course:
                course.sudo().write({
                    'faq_ids': faq_lines,
                    # Add lines to One2many
                    'line_ids': [(0, 0, {'h1': line['title'], 'c1': line['content']}) for line in curriculum_lines],
                    'student_line_ids': [(0, 0, student_line_data)]
                })

            selected_target_audiences = request.httprequest.form.getlist('target_audience[]')
            if isinstance(selected_target_audiences, str):
                selected_target_audiences = [
                    selected_target_audiences]  # Ensure it's a list if only one checkbox is selected

            # Fetch the course model for updating the many2many field
            if selected_target_audiences:
                audience_courses = request.env['course.course'].sudo().search(
                    [('name', 'in', selected_target_audiences)])
                # Update the 'course_ids' field of the 'slide.channel' model
                selected_course.sudo().write({
                    'course_ids': [(6, 0, audience_courses.ids)]  # Update the many2many field
                })

            about_course_paragraphs = [
                post[key] for key in post if key.startswith('paragraph') and post[key] not in [None, '']
            ]

            # Collect all dynamic paragraphs for `individual_line_ids`
            individual_paragraphs = [
                post[key] for key in post if key.startswith('individual_paragraph') and post[key] not in [None, '']
            ]

            # Initialize the updates dictionary
            updates = {
                'p2': description,
                'creator_name': creator_name,
                'main_heading': 'THE COMPLETE GUIDE TO STARTING UP',
                'course_title': 'ABOUT THIS COURSE',
                'h1': 'WHAT AN INDIVIDUAL CAN LEARN FROM THIS?',
                'h2': 'COURSE CURRICULUM',
                'h3': 'ABOUT ME',
                'h6': 'WHO SHOULD TAKE THIS COURSE ?',
                'h7': 'FROM OUR STUDENTS',
                'h5': 'FREQUENTLY ASKED QUESTIONS',
                'h4': 'The Complete Guide To Starting Up',
                'c1': ups_name1,
                'c2': ups_name2,
                'c3': ups_name3,
                'c4': ups_name4,
                'm1': face_book,
                'm2': social_media_x,
                'm3': linked_in,
                'm4': you_tube,
                'm5': instagram,
                'm6': pinInterest,
                'c11': shortDescription,
                'is_this_certificate_course': certificate_course,
                'issued_by': certificate,
            }

            # Remove fields with empty values (`None`, `''`, etc.)
            updates = {key: value for key, value in updates.items() if value not in [None, '']}
            # Update the course if it exists
            if course.exists():
                course.sudo().write({
                    **updates
                })

            if section_upload_files:
                # Save the uploaded image
                image_data = section_upload_files.read()
                course.sudo().write({'image_icon': base64.b64encode(image_data)})
            if aboutme_upload_files:
                about_me_file = aboutme_upload_files.read()
                course.sudo().write({'my_image_icon': base64.b64encode(about_me_file)})
            # Add `about.course` dynamic paragraphs
            if about_course_paragraphs:
                course.sudo().write({
                    'course_line_ids': [(0, 0, {'p1': paragraph}) for paragraph in about_course_paragraphs]
                })

            # Add dynamic paragraphs to `individual_line_ids`
            if individual_paragraphs:
                course.sudo().write({
                    'individual_line_ids': [(0, 0, {'c1': paragraph}) for paragraph in individual_paragraphs]
                })
        # Render the page for GET request
        return http.request.render('custom_web_kreator.edit_landing_page', {
            'user_name': user.name,
            # 'courses': selected_course,
            'selected_course': selected_course,
            'description1': selected_course.p2,
            'primary_color': selected_course.primary_color,
            'secondary_color': selected_course.secondary_color,
            'usp1': selected_course.c1,
            'usp2': selected_course.c2,
            'usp3': selected_course.c3,
            'usp4': selected_course.c4,
            'course_lines_p1': course_lines_p1,
            'individual_line_c1': individual_line_c1,
            'm1': selected_course.m1,
            'm2': selected_course.m2,
            'm3': selected_course.m3,
            'm4': selected_course.m4,
            'm5': selected_course.m5,
            'm6': selected_course.m6,
            'c11': selected_course.c11,
            'is_this_certificate_course': selected_course.is_this_certificate_course,
            'issued_by': selected_course.issued_by,
            # 'image_url': image_url,
            # 'files': files,
            'target_audience_options': target_audience_options,
            'course_ids': selected_course.course_ids.ids if selected_course else []

        })

    @http.route('/landing_page', type='http', auth='public', website=True, sitemap=False)
    def landing_page(self, course_id=False, **post):
        if not course_id:
            raise NotFound("Course ID is missing.")
        landing_id = request.env['slide.channel'].sudo().search([('id', '=', int(course_id))], limit=1)
        student = []  # List to hold the pairs
        first_record = None  # Store the first record for reuse
        data = {}  # Temporary dictionary for a single pair
        i = 1  # Counter to alternate between 'a' and 'b'

        if landing_id.student_line_ids:
            for rec in landing_id.student_line_ids:
                if first_record is None:  # Capture the first record
                    first_record = {
                        'name': rec.name,
                        'type': rec.content_type,
                        'content': rec.p1,
                        'rating': int(rec.rating),
                        'image': rec.image
                    }
                if i == 1:  # Populate 'a' part of the pair
                    data = {'a': {
                        'name': rec.name,
                        'type': rec.content_type,
                        'content': rec.p1,
                        'content': rec.p1,
                        'rating': int(rec.rating),
                        'image': rec.image
                    }}
                    i += 1
                else:  # Populate 'b' part of the pair
                    data['b'] = {
                        'name': rec.name,
                        'type': rec.content_type,
                        'content': rec.p1,
                        'rating': int(rec.rating),
                        'image': rec.image
                    }
                    student.append(data)  # Add the completed pair to the list
                    data = {}  # Reset for the next pair
                    i = 1

        # Handle the case of an unpaired last 'a' by repeating the first record in 'b'
        if data and 'a' in data:
            data['b'] = first_record  # Use the first record to fill the missing 'b'
            student.append(data)
        primary_color = '#044e99'
        secondary_color = '#FFD000'
        text_color = '#FFFFFF'
        background_color = '#000000'
        if landing_id.combination_id:
            primary_color = landing_id.combination_id.primary_color
            secondary_color = landing_id.combination_id.secondary_color
            text_color = landing_id.combination_id.text_color
            background_color = landing_id.combination_id.background_color
        values = {
            'landing_id': landing_id,
            'students': student,
            'secondary_color': secondary_color,
            'primary_color': primary_color,
            'text_color': text_color,
            'background_color': background_color,
        }
        print("values",values)
        
        if landing_id:
            product_id = landing_id.product_id.id
            if not product_id:
                raise UserError("No product found for this course")
            product_template_id = landing_id.product_id.id
            values['product_id'] = product_id
            values['product_template_id'] = product_template_id
            
        # Check if session has referral access
        session_data = request.session.get('course_access', {})
        partner_id = session_data.get('partner_id')
        
        user = request.env.user
        partner = user.partner_id

        if not partner_id and partner.user_type == 'customer':
            return request.redirect('/404')

        return request.render('custom_web_kreator.landing_page', values)

    # @http.route('/partner-referral', type='http', auth='public', website=True)
    # def partner_referral(self, **kwargs):
    #     # Render the data page template
    #     return http.request.render('custom_web_kreator.partner_referral_link_page')

    @http.route('/partner-leaderboard', type='http', auth='public', website=True)
    def partner_leaderboard(self, **kwargs):
        orders_lines = request.env['sale.order.line'].sudo().search([('is_commission','=', True),('state', '=', 'sale'),('partner_commission_partner_id', '!=', False)])
        order_lines = sorted(orders_lines, key=attrgetter('partner_commission_partner_id'))
        # Group by commission partner ID
        grouped_data = {}
        leaderboard = []
        for partner, lines in groupby(order_lines, key=attrgetter('partner_commission_partner_id')):
            grouped_data[partner] = {
                'total_commission': sum(line.partner_commission_amount for line in lines),
            }
        for data in grouped_data:
            lines = orders_lines.search([('partner_commission_partner_id','=',data.id)])
            leaderboard.append({
                'partner_name':data.name,
                'total_commission': sum(line.partner_commission_amount for line in lines),
            })
        leaderboard = sorted(leaderboard, key=lambda x: x['total_commission'], reverse=True)
        values = {
            'leaderboard':leaderboard,
            'currency_id': request.env.company.currency_id
        }
        # Render the data page template
        return http.request.render('custom_web_kreator.partner_leaderboard_page',values)

    @http.route('/partner-training', type='http', auth='public', website=True)
    def partner_training(self, **kwargs):
        print("comingggggg")
        # Fetch courses where is_training_course is True and sort them alphabetically by name
        training_courses = request.env['slide.channel'].sudo().search(
            [('is_training_course', '=', True),('state', '=', 'published')],
            order='name asc'
        )
        print("training_courses",training_courses)
        # Render the template and pass the courses
        return request.render('custom_web_kreator.partner_training', {
            'training_courses': training_courses
        })

    @http.route('/promotional-detail', type='http', auth='public', website=True)
    def promotional_details(self, **kwargs):
        # Render the data page template
        course_id = kwargs.get('course_id')

        if not course_id:
            return request.not_found()

        course = request.env['slide.channel'].sudo().browse(int(course_id))

        if not course.exists():
            return request.not_found()

        return request.render('custom_web_kreator.promotional_detail', {
            'course': course,
            'promotional_materials': course.promotional_material_ids
        })


    @http.route('/download_attachment/<int:material_id>', type='http', auth='public')
    def download_attachment(self, material_id, **kwargs):
        material = request.env['slide.channel.promotional.material'].sudo().browse(material_id)
        if material and material.promotional_attachment:
            file_content = base64.b64decode(material.promotional_attachment)
            filename = material.promotional_attachment_name or "attachment"

            return request.make_response(file_content, [
                ('Content-Type', 'application/octet-stream'),
                ('Content-Disposition', content_disposition(filename))
            ])
        return request.not_found()

    @http.route('/coming-soon', type='http', auth='public', website=True)
    def coming_soon(self, **kwargs):
        # Render the data page template
        return http.request.render('custom_web_kreator.coming_soon')

    @http.route('/creator-profile', type='http', auth='user', website=True, methods=['GET', 'POST'],csrf=False)
    def creator_profile(self, **post):
        user = request.env.user
        partner = user.partner_id  # Get the linked partner record
        image_file = request.httprequest.files.get('image')
        print("image_file",image_file)
        # Map input fields to social media types
        social_media_map = {
            'facebook': 'facebook',
            'twitter': 'twitter',
            'instagram': 'instagram',
            'youtube': 'youtube',
            'linkedin': 'linkedin'
        }
        if request.httprequest.method == 'POST':
            social_data = []  # List to store updates
            if image_file:
                image_data = image_file.read()
                user.image_1920 = base64.b64encode(image_data)
                print("user.image_1920",user.image_1920)
            # Get existing social media records
            existing_socials = {line.social_media: line for line in partner.social_section_line}

            for field_name, social_label in social_media_map.items():
                social_link = post.get(field_name)  # Get user input

                if social_link:  # Only update if value is provided
                    if social_label in existing_socials:  # Update existing record
                        existing_socials[social_label].social_media_link = social_link
                    else:  # Create new record if it doesn't exist
                        social_data.append((0, 0, {
                            'social_media': social_label,
                            'social_media_link': social_link
                        }))

            # Update the res.partner model with new values
            if social_data:
                partner.write({'social_section_line': social_data})

        user_image = user.image_1920 and f"data:image/png;base64,{user.image_1920.decode('utf-8')}" or "/web/image/res.users/%s/image_1920" % user.id
        print("user_image",user_image)
        # Pass existing values to the template
        values = {
            'name': user.name,
            'email': user.email,
            'phone': user.phone,
            'user_image': user_image
        }

        return request.render('custom_web_kreator.creator_profile', values)

    @http.route('/partner-profile', type='http', auth='user', website=True, methods=['GET', 'POST'])
    def partner_profile(self, **kwargs):
        user = request.env.user  # Get the logged-in user
        partner = user.partner_id  # Get related partner

        # If form is submitted (POST request)
        if request.httprequest.method == 'POST':
            new_name = kwargs.get('name')
            new_email = kwargs.get('email')
            new_mobile = kwargs.get('mobile')
            new_image = kwargs.get('profile_image')

            # Update user and partner details if changed
            if new_name and new_name != user.name:
                user.name = new_name  # Update user name

            if new_email and new_email != user.email:
                user.login = new_email  # Update user email

            if new_mobile:
                # Ensure mobile number starts with +91
                if not new_mobile.startswith('+91'):
                    new_mobile = f'+91 {new_mobile}'

                if partner and new_mobile != partner.phone:
                    partner.phone = new_mobile  # Update partner's phone
            # Update profile image if uploaded
            if new_image:
                file_storage = request.httprequest.files.get('profile_image')
                if file_storage:
                    image_data = file_storage.read()
                    user.image_1920 = base64.b64encode(image_data)  # Save image in res.users

        # Fetch updated details
        phone = partner.phone if partner and partner.phone else ''
        profile_image = user.image_1920 and f"data:image/png;base64,{user.image_1920.decode()}" or "/custom_web_kreator/static/src/user1.png"
        if phone and not phone.startswith('+91'):
            phone = f'+91 {phone}'

        values = {
            'name': user.name,
            'email': user.login,
            'mobile': phone,
            'profile_image': profile_image
        }

        return request.render('custom_web_kreator.partner_profile', values)

    @http.route('/user/profile/image', type='http', auth='user', website=True)
    def user_profile_image(self):
        user = request.env.user  # Get the logged-in user
        profile_image = user.image_1920  # Fetch profile image

        if profile_image:
            image_data = base64.b64decode(profile_image)  # Decode base64 image
            return request.make_response(image_data, [('Content-Type', 'image/png')])  # Serve image dynamically
        else:
            return request.redirect('/custom_web_kreator/static/src/user1.png')  # Default image fallback

    @http.route('/customer-support', type='http', auth='public', website=True, methods=['GET', 'POST'])
    def customer_support(self, **kwargs):
        print("comingggg11111")
        user = request.env.user  # Get the logged-in user
        partner = user.partner_id  # Get related partner

        # If form is submitted (POST request)
        if request.httprequest.method == 'POST':
            print("cominggg22222")
            new_name = kwargs.get('name')
            new_email = kwargs.get('email')
            new_mobile = kwargs.get('mobile')
            new_subject = kwargs.get('subject')  # Extract subject
            new_question = kwargs.get('question')  # Extract question

            # Update user and partner details if changed
            if new_name and new_name != user.name:
                user.name = new_name  # Update user name

            if new_email and new_email != user.email:
                user.login = new_email  # Update user email

            if new_mobile:
                if not new_mobile.startswith('+91'):
                    new_mobile = f'+91 {new_mobile}'

                if partner and new_mobile != partner.phone:
                    partner.phone = new_mobile  # Update partner's phone

            # Save the form submission to helpdesk.ticket
            if new_subject and new_question:
                print("comingg3333")
                request.env['helpdesk.ticket'].sudo().create({
                    'name': new_subject,  # Set subject in name field
                    'description': new_question,  # Set question in description field
                    'partner_id': partner.id if partner else False,  # Link to the user
                })

        # Fetch updated details
        phone = partner.phone if partner and partner.phone else ''
        profile_image = user.image_1920 and f"data:image/png;base64,{user.image_1920.decode()}" or "/custom_web_kreator/static/src/user1.png"
        if phone and not phone.startswith('+91'):
            phone = f'+91 {phone}'

        values = {
            'name': user.name,
            'email': user.login,
            'mobile': phone,
            'profile_image': profile_image
        }
        return request.render('custom_web_kreator.customer_support', values)

    @http.route('/customer-profile', type='http', auth='public', website=True)
    def customer_profile(self, **kwargs):
        # Render the data page template
        return http.request.render('custom_web_kreator.customer_profile')

    @http.route('/master-partner', type='http', auth='public', website=True)
    def master_partner(self, **kwargs):
        # Render the data page template
        return http.request.render('custom_web_kreator.partner_master')

    @http.route('/partner-video1', type='http', auth='public', website=True)
    def partner_video_one(self, **kwargs):
        # Render the data page template
        return http.request.render('custom_web_kreator.partner_video1')

    @http.route('/partner-video2', type='http', auth='public', website=True)
    def partner_video_two(self, **kwargs):
        # Render the data page template
        return http.request.render('custom_web_kreator.partner_video2')


    @http.route('/partner-video3', type='http', auth='public', website=True)
    def partner_video_three(self, **kwargs):
        # Render the data page template
        return http.request.render('custom_web_kreator.partner_video3')

    @http.route('/partner-term', type='http', auth='public', website=True)
    def partner_term(self, **kwargs):
        # Render the data page template
        return http.request.render('custom_web_kreator.partner_term',)

    @http.route('/submit-terms', type='http', auth='public', website=True, methods=['POST'])
    def submit_terms(self, **post):
        agreement_value = request.params.get('agreement')

        if agreement_value not in ['agree', 'disagree']:
            return request.redirect('/terms-page')  # Redirect back if no selection is made

        # Store the agreement value in session
        request.session['agreement'] = agreement_value

        if agreement_value == 'disagree':
            # Create a lead in crm.lead
            request.env['crm.lead'].sudo().create({
                'name': 'Disagreed User',  # You can make this dynamic
                'description': 'User disagreed to the terms and conditions.',
                'type': 'lead',
            })

        return request.redirect('/partner-welcome')


    @http.route('/partner-welcome', type='http', auth='public', website=True)
    def partner_welcome(self, **kwargs):
        # Render the data page template
        
        agreement = request.session.get('agreement', 'No Selection')
        return http.request.render('custom_web_kreator.partner_welcome',{'agreement':agreement})
