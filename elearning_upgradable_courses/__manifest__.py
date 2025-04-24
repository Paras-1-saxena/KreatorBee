{
    'name': 'Elearning Upgradable Courses',
    'version': '18.0.1.0.0',
    'summary': '',
    'description': """""",
    'author': 'Kreator Bee',
    'website': 'https://www.kreatorbee.com',
    'category': 'website',
    'depends': ['product','website_slides','website_sale_slides','sale', 'website_sale', 'apg_signup', 'payment', 'website'],  # List of dependent modules
    'data': [
        'security/ir.model.access.csv',
        'views/slide_channel_view.xml',
        'views/payment_message.xml',
        'views/res_partner.xml',
        'views/slide_content_upgradable.xml',
        'wizard/unblocked_third_party_domains.xml',
        'wizard/website_configuration_form_inherit.xml'
        # 'views/slide_content_upgradable.xml'
    ],
    'demo': [
        # Demo data (optional)
    ],
    'installable': True,  # Determines if the module can be installed
    'auto_install': False,  # If True, it will auto-install if its dependencies are installed
    'license': 'LGPL-3',
    # # License for the module (typically 'LGPL-3' for Odoo apps)
}
