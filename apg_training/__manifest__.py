{
    'name': 'Apg Training',
    'version': '18.0.1.0.0',
    'summary': 'Apg Training',
    'description': """Apg Course Referral""",
    'author': 'Apagen solutions',
    'website': 'https://www.apagen.com',
    'category': 'website',
    'depends': ['base', 'website', 'custom_web_kreator'],  # List of dependent modules
    'data': [
        'security/ir.model.access.csv',
        'views/course_training_views.xml',
        # 'views/nreferral.xml',
        # 'views/partner_refferal_template.xml',
        # 'views/landing_template.xml',
    ],
    'demo': [
        # Demo data (optional)
    ],
    'installable': True,  # Determines if the module can be installed
    'auto_install': False,  # If True, it will auto-install if its dependencies are installed
    'license': 'LGPL-3',
}
