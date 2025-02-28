{
    'name': 'Apg Social Media',
    'version': '18.0.1.0.0',
    'summary': '',
    'description': """""",
    'author': 'Apagen solutions',
    'website': 'https://www.apagen.com',
    'category': 'website',
    'depends': ['base', 'web', 'website', 'mail', 'custom_web_kreator'],  # List of dependent modules
    'data': [
        'security/ir.model.access.csv',
        # 'views/assets.xml',
        'views/media_post_view.xml',
        'views/fbpost.xml',
        'views/fbpost_partner.xml',
        'views/fbpost_customer.xml',
        'views/menu.xml',
    ],
    'demo': [
        # Demo data (optional)
    ],
    'installable': True,  # Determines if the module can be installed
    'auto_install': False,  # If True, it will auto-install if its dependencies are installed
    'license': 'LGPL-3',
    # 'assets':{
    #     'web.assets_frontend':[
    #         '/apg_social_media/static/src/scss/social.css',
    #         '/apg_social_media/static/src/scss/menu.css',
    #         '/apg_social_media/static/src/js/social.js',
    #         '/apg_social_media/static/src/js/hide.js',
    #         '/apg_social_media/static/src/js/menu.js',
    #     ],
    # }
    # # License for the module (typically 'LGPL-3' for Odoo apps)
}
