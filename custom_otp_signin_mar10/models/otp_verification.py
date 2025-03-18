from odoo import fields, models, api


class OtpVerification(models.Model):
    _name = "otp.verification"
    _description = 'Otp Verification'

    otp = fields.Text(string="OTP")
    state = fields.Selection([
            ('verified', 'Verified'),
            ('unverified', 'Unverified'),
            ('rejected', 'Rejected')], string="State", default="unverified")
    mobile = fields.Char(string="mobile")

    @api.model
    def _cron_delete_verified_otp(self):
        otp = self.search([('state', '=', 'verified')])
        otp.unlink()

