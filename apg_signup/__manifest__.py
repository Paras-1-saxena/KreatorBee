{
    'name': 'Apg website Changes',
    'version': '18.0.1.0.0',
    'summary': 'this module allow your employees/users to do the customisations.',
    'description': """
his module allow your employees/users to do the customisations.
""",
    'author': 'Apagen solutions',
    'website': 'https://www.apagen.com',
    'category': 'website',
    'depends': ['custom_web_kreator', 'auth_signup','website', 'contacts', 'payment', 'web', 'website_sale', 'website_sale_slides', 'website_slides', 'payment_demo'],  # List of dependent modules
    'data': [
        'security/ir.model.access.csv',
        'views/asset_template.xml',
        'views/custom_signup_template.xml',
        'views/res_partner.xml',
        'views/signup_address_template.xml',
        'views/partner_details_template.xml',
        # 'views/landing_page_template1.xml',
        'views/landing_page_view.xml',
        'views/login_template.xml',
        'views/login_template_inherit.xml',
        'views/menu.xml',
        'views/partner_signup_second_page.xml',
    ],
    'demo': [
        # Demo data (optional)
    ],
    'installable': True,  # Determines if the module can be installed
    'auto_install': False,  # If True, it will auto-install if its dependencies are installed
    'license': 'LGPL-3',
    'assets':{
            'web.assets_frontend':[
                '/apg_signup/static/src/js/cust_signup.js',
                '/apg_signup/static/src/js/resend_otp.js',
                '/apg_signup/static/src/js/dynamic_states.js',
                '/apg_signup/static/src/js/otp.js',
                '/apg_signup/static/src/scss/signup_details.css',
        ],
    }
    # # License for the module (typically 'LGPL-3' for Odoo apps)
}
