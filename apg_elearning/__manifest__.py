{
    'name': 'Apg elearning Changes',
    'version': '18.0.1.0.0',
    'summary': '',
    'description': """""",
    'author': 'Apagen solutions',
    'website': 'https://www.apagen.com',
    'category': 'website',
    'depends': ['base','product','website_slides','website_sale_slides','sale','documents'],  # List of dependent modules
    'data': [
        'data/documents_document_data.xml',
        'security/ir.model.access.csv',
        'views/configuration_view.xml',
        'views/slide_channel.xml',
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
