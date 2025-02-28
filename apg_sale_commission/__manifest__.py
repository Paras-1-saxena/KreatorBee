{
    'name': 'Apg sale commission',
    'version': '18.0.1.0.0',
    'summary': '',
    'description': """""",
    'author': 'Apagen solutions',
    'website': 'https://www.apagen.com',
    'category': 'website',
    'depends': ['base','sale','apg_elearning'],  # List of dependent modules
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_commission.xml',
        'views/menu.xml',
    ],
    'demo': [
        # Demo data (optional)
    ],
    'installable': True,  # Determines if the module can be installed
    'auto_install': False,  # If True, it will auto-install if its dependencies are installed
    'license': 'LGPL-3',
    # # License for the module (typically 'LGPL-3' for Odoo apps)
}