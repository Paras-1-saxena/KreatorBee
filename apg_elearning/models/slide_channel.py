from odoo import api, fields, models, exceptions,_

class SlideChannel(models.Model):
    _name = 'slide.channel'
    _inherit = ['slide.channel', 'documents.mixin']

    regular_price = fields.Float(string="Regular Price")
    sales_price = fields.Float(string="Sales Price")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('course_preview', 'Under Review'),
        ('published', 'Published')
    ], string="State", default='draft', required=True)
    partner_commission = fields.Float(string="Partner Sales Commission", compute='_compute_sales_price',store=True)
    direct_commission = fields.Float(string="Direct Sales Commission", compute='_compute_sales_price',store=True)
    google_drive_links = fields.Many2many(
        comodel_name='ir.attachment',  # This model manages file attachments
        relation='course_standard_attachment_rel',  # Relation table name
        column1='course_standard_id',  # Relation column for `course.standard`
        column2='attachment_id',  # Relation column for `ir.attachment`
        string="Google Drive Links"
    )
    partner_commission_id = fields.Many2one("partner.commission", "Partner Commission")
    direct_commission_id = fields.Many2one("direct.commission", "Direct Commission")
    product_id = fields.Many2one('product.product', 'Product', domain=[('service_tracking', '=', 'course')])
    enroll = fields.Selection([
        ('public', 'Open'), ('invite', 'On Invitation'),('payment', 'On payment')],
        compute='_compute_enroll', store=True, readonly=False,
        default='public', string='Enroll Policy', required=True,
        help='Defines how people can enroll to your Course.', copy=False)

    # promotional_attachment = fields.Binary(string="Promotional Attachment")
    # promotional_attachment_name = fields.Char(string="Promotional Attachment Filename")

    use_documents = fields.Boolean("Documents", default=True)

    documents_folder_id = fields.Many2one(
        'documents.document', string="Course", copy=False,
        domain="[('type', '=', 'folder'), ('shortcut_document_id', '=', False), "
               "'|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help="Folder in which all of the documents of this project will be categorized. All of the attachments of "
             "your tasks will be automatically added as documents in this workspace as well.")

    document_ids = fields.One2many('documents.document', compute='_compute_documents', export_string_translation=False)
    documents_tag_ids = fields.Many2many(
        'documents.tag', 'slide_channel_id', string="Default Tags", copy=True)
    promotional_material_ids = fields.One2many(
        'slide.channel.promotional.material',
        'slide_channel_id')
    # Add the new boolean field to indicate if it's a training course
    is_training_course = fields.Boolean(string="Is Training Course")
    google_drive_links1 = fields.One2many(
        'slide.channel.google.drive.link', 'channel_id', string='Google Drive Links')

    class SlideChannelGoogleDriveLink(models.Model):
        _name = 'slide.channel.google.drive.link'
        _description = 'Google Drive Link'

        link = fields.Char(string='Link', required=True)
        channel_id = fields.Many2one('slide.channel', string='Channel', ondelete='cascade')

    def action_open_landing_page(self, *args, **kwargs):  # Accept extra args
        for record in self:
            if record.website_url:
                return {
                    'type': 'ir.actions.act_url',
                    'url': record.website_url,  # Open the computed URL
                    'target': 'new',  # Opens in a new tab
                }


    @api.model_create_multi
    def create(self, vals_list):
        courses = super().create(vals_list)
        if not self.env.context.get('no_create_folder'):
            courses.filtered(lambda course: course.use_documents)._create_missing_folders()
        for course in courses:
            course._add_promotional_attachment()
        return courses

    def _add_promotional_attachment(self):
        """Add promotional materials to the course folder in the Documents module."""
        for course in self:
            folder = course.documents_folder_id
            if not folder:
                continue  # Skip if no folder exists for the course

            for material in course.promotional_material_ids:
                if material.promotional_attachment:
                    # Check if a document already exists for this attachment in the course folder
                    existing_document = self.env['documents.document'].search([
                        ('res_model', '=', 'slide.channel.promotional.material'),
                        ('res_id', '=', material.id),
                        ('folder_id', '=', folder.id)
                    ], limit=1)

                    if not existing_document:
                        # Create a new document for this promotional material
                        self.env['documents.document'].create({
                            'name': material.promotional_attachment_name or _("Promotional Material"),
                            'type': 'binary',
                            'datas': material.promotional_attachment,
                            'folder_id': folder.id,
                            'res_model': 'slide.channel.promotional.material',
                            'res_id': material.id,
                        })


    def action_submit_for_review(self):
        self.state = 'course_preview'

    def action_approve(self):
        product_obj = self.env['product.product']
        for rec in self:
            vals = {
                'name': rec.name,
                'list_price': rec.sales_price,
                'service_tracking': 'course',
                'type': 'service',
                'purchase_ok': False,
                'is_published': True,
            }
            product_id = product_obj.create(vals)
            rec.write({
                'product_id': product_id.id,
                'is_published': True,
                'state': 'published',
                'enroll': 'payment',
                })

    @api.depends('sales_price')
    def _compute_sales_price(self):
        self.partner_commission = False
        self.direct_commission = False
        partner_commission_id = self.env['partner.commission'].search([],order='create_date desc',  # Order by creation date, latest first
            limit=1
        )
        direct_commission_id = self.env['direct.commission'].search([],order='create_date desc',  # Order by creation date, latest first
            limit=1
        )
        if not partner_commission_id:
            raise exceptions.ValidationError(_("Please configure Partner Commission"))
        if not direct_commission_id:
            raise exceptions.ValidationError(_("Please configure Direct Commission"))
        
        for rec in self:
            if rec.sales_price:
                rec.partner_commission = (rec.sales_price * partner_commission_id.rate)/100
                rec.direct_commission = (rec.sales_price * direct_commission_id.rate)/100

    def write(self, vals):
        # Update the name of the documents folder if the project name changes
        if 'name' in vals and len(
                self.documents_folder_id.sudo().course_ids) == 1 and self.name == self.documents_folder_id.sudo().name:
            self.documents_folder_id.sudo().name = vals['name']

        # Handle updates for 'privacy_visibility'
        if new_visibility := vals.get('privacy_visibility'):
            self.documents_folder_id.action_update_access_rights(
                access_internal='none' if new_visibility == 'followers' else 'edit'
            )

        # Call the super method to perform the actual write operation
        res = super(SlideChannel, self).write(vals)

        # Automatically add promotional materials to the Documents module (Avoid duplicates)
        for record in self:
            folder = record.documents_folder_id
            for material in record.promotional_material_ids:
                if material.promotional_attachment and folder:
                    # Avoid duplicate documents in the folder
                    existing_document = self.env['documents.document'].search([
                        ('res_model', '=', 'slide.channel'),
                        ('res_id', '=', record.id),
                        ('attachment_id', '=', material.id),
                        ('folder_id', '=', folder.id)
                    ], limit=1)
                    if not existing_document:
                        self.env['documents.document'].create({
                            'name': material.promotional_attachment_name or 'Promotional Material',
                            'type': 'binary',
                            'attachment_id': material.id,
                            'folder_id': folder.id,
                            'res_model': 'slide.channel',
                            'res_id': record.id,
                        })

        # Create missing folders if 'use_documents' is enabled and context doesn't prevent it
        if not self.env.context.get('no_create_folder'):
            self.filtered('use_documents')._create_missing_folders()

        # Synchronize product details with SlideChannel updates
        if self.product_id:
            if 'sales_price' in vals:
                self.product_id.write({'list_price': vals.get('sales_price')})
            if 'name' in vals:
                self.product_id.write({'name': vals.get('name')})

        return res

    def action_view_documents_project(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("documents.document_action")
        return action | {
            'view_mode': 'kanban,list',
            'context': {
                'active_id': self.id,
                'active_model': 'slide.channel',
                'default_res_id': self.id,
                'default_res_model': 'slide.channel',
                'no_documents_unique_folder_id': True,
                'searchpanel_default_folder_id': self._get_document_folder().id,
            }
        }

    def _get_document_folder(self):
        return self.documents_folder_id

    def _get_document_tags(self):
        return self.documents_tag_ids

    def _get_document_access_ids(self):
        return False

    def _check_create_documents(self):
        return self.use_documents and super()._check_create_documents()

    def _create_missing_folders(self):
        folders_to_create_vals = []
        course_with_folder_to_create = []
        documents_course_folder_id = self.env.ref('apg_elearning.document_course_folder').id

        for course in self:
            if not course.documents_folder_id:
                folder_vals = {
                    'access_internal': 'edit',
                    'folder_id': documents_course_folder_id,
                    'name': course.name,
                    'type': 'folder',
                }
                folders_to_create_vals.append(folder_vals)
                course_with_folder_to_create.append(course)
                print("course_with_folder_to_create",course_with_folder_to_create)

        if folders_to_create_vals:
            created_folders = self.env['documents.document'].sudo().create(folders_to_create_vals)
            for course, folder in zip(course_with_folder_to_create, created_folders):
                course.sudo().documents_folder_id = folder


    @api.depends('name', 'website_id.domain')
    def _compute_website_url(self):
        """Override default website URL computation to use course ID instead of slug."""
        super(SlideChannel, self)._compute_website_url()  # Call the original method

        for channel in self:
            if channel.id:  # Ensure ID exists to avoid issues
                base_url = channel.get_base_url()
                print("Base URL:", base_url)
                # Customize the website_url with course ID instead of slug
                channel.website_url = '%s/landing_page?course_id=%s' % (base_url, channel.id)



class SlideChannelPromotionalMaterial(models.Model):
    _name = 'slide.channel.promotional.material'
    _description = 'Promotional Material'

    slide_channel_id = fields.Many2one(
        'slide.channel',
        string="Course",
        ondelete='cascade'
    )
    document_type = fields.Selection(
        [('url', 'URL'), ('doc', 'Document')],
        string="Document Type",
        default='doc'
    )
    promotional_attachment = fields.Binary(string="Attachment")
    promotional_attachment_name = fields.Char(string="Filename")
    promotional_url = fields.Char(string="URL")
