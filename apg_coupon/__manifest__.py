{
    'name': 'Apg Coupon Customization',
    'version': '18.0.1.0.0',
    'summary': '',
    'description': """ """,
    'author': 'Apagen solutions',
    'website': 'https://www.apagen.com',
    'category': 'website',
    'depends': ['base', 'sale', 'sale_management', 'loyalty'],  # List of dependent modules
    'data': [
        'security/ir.model.access.csv',
        'wizard/loyalty_generate_wizard.xml',
        'views/discount_view.xml',
        'views/duration_view.xml',
        'views/menu_view.xml',
        'views/loyalty_program_view.xml',
    ],
    'demo': [
        # Demo data (optional)
    ],
    'installable': True,  # Determines if the module can be installed
    'auto_install': False,  # If True, it will auto-install if its dependencies are installed
    'license': 'LGPL-3',
    'assets':{
    }
    # # License for the module (typically 'LGPL-3' for Odoo apps)
}
