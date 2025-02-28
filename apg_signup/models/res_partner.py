from odoo import api, fields, models, exceptions,_
from odoo.exceptions import UserError, ValidationError
from random import randint


class NicheType(models.Model):
    _name = 'niche.type'
    _description = 'Niche Type'

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Color', default=_get_default_color, aggregator=False)
    # color_new = fields.Integer(string='Color New', default=0)
    color_new = fields.Char(string='Color New', default='#FFFFFF')


class EducationType(models.Model):
    _name = 'education.type'
    _description = 'Education Type'

    name = fields.Char(string="Education Type", required=True)
    description = fields.Text(string="Description")


class EntertainmentType(models.Model):
    _name = 'entertainment.type'
    _description = 'Entertainment Type'

    name = fields.Char(string="Entertainment Type", required=True)
    description = fields.Text(string="Description")

class ResPartner(models.Model):
    _inherit = 'res.partner'


    user_type = fields.Selection(
        [('creator', 'Creator'),('partner', 'Partner'), ('customer', 'Customer'),('internal_user', 'Internal')],
        string='User Type',
        required=True,
    )
    niche_type = fields.Selection(
        [('education', 'Education'),('entertainment', 'Entertainment'),('others', 'Others')],
        string='Niche Selection',
        required=True,
    )
    niche_type_ids = fields.Many2many('niche.type')
    product_type = fields.Selection([('live_workshop', 'Live Workshop'),('pre_orded_course', 'Per-recorded Course'),('one_to_one', 'One to One')],
        string='Type Of Product',
        required=True,
        default='pre_orded_course',
        readonly=True,
    )
    reference = fields.Selection(
        [('friend', 'Friend'),('instagram', 'Instagram'), ('youtube', 'YouTube'),('partner', 'Partner'),('google', 'Google'),('ad', 'Ad'),('other', 'Other')],
        string='Reference',
        required=True,
        default='google'
    )
    description = fields.Text(string='Description')

    # Add KYC-specific fields here
    select_document = fields.Selection([('aadhaar', 'Aadhaar'),
                                   ('driving_license', 'Driving License'),
                                   ('voter_identity_card', 'Voter Identity Card'),
                                   ('passport', 'Passport')], string='Select Document')
    state_selection = fields.Selection([('pending', 'Pending'),
                                        ('under_review', 'Under Review'),
                                   ('approved', 'Approved'),
                                   ('rejected', 'Rejected')], string='Status',default='pending')

    def action_approve(self):
        self.write({'state_selection': 'approved'})

    def action_reject(self):
        self.write({'state_selection': 'rejected'})

    aadhaar_number = fields.Char('Aadhaar Number')
    aadhaar_name = fields.Char('Name on Aadhaar')
    aadhaar_front = fields.Binary('Upload Front Side')
    aadhaar_back = fields.Binary('Upload Back Side')
    driving_license_number = fields.Char('Driving License Number')
    driving_license_name = fields.Char('Name on Driving License')
    driving_license_front = fields.Binary('Upload Front Side')
    driving_license_back = fields.Binary('Upload Back Side')
    voter_identity_number = fields.Char('Voter Identity Number')
    voter_identity_name = fields.Char('Name on Voter Identity')
    voter_identity_front = fields.Binary('Upload Front Side')
    voter_identity_back = fields.Binary('Upload Back Side')
    passport_number = fields.Char('Passport Number')
    passport_name = fields.Char('Name on Passport')
    passport_front = fields.Binary('Upload Front Side')
    passport_back = fields.Binary('Upload Back Side')
    pan_card_number = fields.Char('PAN Number')
    pan_card_name = fields.Char('PAN Name')
    pan_card_file = fields.Binary('Upload PAN Card File')
    Account_holder_name = fields.Char('Account Holder Name')
    Account_holder_number = fields.Char('Account Number')
    bank_id = fields.Many2one('res.partner.bank',tracking=True)
    ifsc_code = fields.Char('IFSC Code')
    upload_file = fields.Binary('Upload Cancel Cheque/Passbook/bank Statement')
    paytm_mobile_number = fields.Binary('Paytm Mobile Number')
    upi_mobile_number = fields.Char('UPI Mobile Number')
    social_section_line = fields.One2many("social.media", "partner_id",
                                       string="Social Media")

    # video_ids = fields.Many2many('ir.attachment', 'res_partner_video_rel', 'partner_id', 'attachment_id',
    #                              domain=[('mimetype', 'ilike', 'video/')], string="Videos")
    # rules_regulations = fields.Boolean(string="Agrees to Rules and Regulations")


    # @api.constrains('video_ids')
    # def _check_video_duration(self):
    #     for partner in self:
    #         if len(partner.video_ids) < 3:
    #             raise exceptions.ValidationError(_("You must upload at least 3 videos."))
    #
    #         for video in partner.video_ids:
    #             video_duration = self._get_video_duration(video)
    #             if video_duration < 60:
    #                 raise exceptions.ValidationError(_("Each video must be at least 1 minute long."))

    @api.constrains('mobile')
    def _check_mobile(self):
        for rec in self:
            partner_id = self.env["res.partner"].search([("mobile", "=", rec.mobile),("id", "!=", rec.id)])
            if partner_id:
                raise ValidationError(_('Another user is already registered using this mobile No.'))


    def _get_video_duration(self, video_attachment):
        video_duration = 120  # placeholder, assume 2-minute video
        return video_duration

    @api.constrains('country_id')
    def _check_country_id(self):
        for record in self:
            if record.country_id and record.country_id.name != 'India':
                raise exceptions.ValidationError(
                    _("The country must be 'India'. Please select 'India' as the country.")
                )

class SocialMedia(models.Model):
    _name = 'social.media'

    partner_id = fields.Many2one("res.partner", "Partner Line ID")

    social_media = fields.Selection(
        selection=[
            ('facebook', 'Facebook'),
            ('twitter', 'Twitter'),
            ('instagram', 'Instagram'),
            ('linkedin', 'LinkedIn'),
            ('youtube', 'YouTube'),
            ('x_portal', 'X Portal'),
        ],
        string='Social Media'
    )
    social_media_link = fields.Char(string='Social Media Handle')
    
class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def signup(self, values, token=None):
        if token:
            partner = self.env['res.partner']._signup_retrieve_partner(token, check_validity=True, raise_exception=True)
            partner_user = partner.user_ids and partner.user_ids[0] or False
            if partner_user:
                values['user_type'] = values.get('user_type')
                values['mobile'] = values.get('phone')
        else:
            values['user_type'] = values.get('user_type')
            values['mobile'] = values.get('phone')
        return super(ResUsers, self).signup(values, token)



