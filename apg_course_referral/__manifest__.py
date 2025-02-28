{
    'name': 'Apg Course Referral',
    'version': '18.0.1.0.0',
    'summary': 'Apg Course Referral',
    'description': """Apg Course Referral""",
    'author': 'Apagen solutions',
    'website': 'https://www.apagen.com',
    'category': 'website',
    'depends': ['base', 'website', 'contacts', 'web', 'website_sale_slides', 'website_slides', 'custom_web_kreator', 'apg_signup', 'apg_sale_commission'],  # List of dependent modules
    'data': [
        'security/ir.model.access.csv',
        'views/course_referral_view.xml',
        'views/nreferral.xml',
        'views/partner_refferal_template.xml',
        'views/landing_template.xml',
    ],
    'demo': [
        # Demo data (optional)
    ],
    'installable': True,  # Determines if the module can be installed
    'auto_install': False,  # If True, it will auto-install if its dependencies are installed
    'post_init_hook': 'set_encryption_key',
    'uninstall_hook': "uninstall_encryption_key",
    'license': 'LGPL-3',
    'assets':{
        'web.assets_frontend':[
            # '/apg_course_referral/static/src/js/course_referral.js',
        ],
    }
    # # License for the module (typically 'LGPL-3' for Odoo apps)
}
