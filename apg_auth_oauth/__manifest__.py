{
    'name': 'Apg OAuth2 Authentication',
    'version': '18.0.1.0.0',
    'summary': '',
    'description': """Allow users to login through OAuth2 Provider.""",
    'author': 'Apagen solutions',
    'website': 'https://www.apagen.com',
    'category': 'website',
    'depends': ['base', 'auth_oauth', 'apg_signup', 'custom_otp_signin'],  # List of dependent modules
    'data': [
        'views/auth_oauth_templates.xml',
    ],
    'demo': [
        # Demo data (optional)
    ],
    'installable': True,  # Determines if the module can be installed
    'auto_install': False,  # If True, it will auto-install if its dependencies are installed
    'license': 'LGPL-3',
}
