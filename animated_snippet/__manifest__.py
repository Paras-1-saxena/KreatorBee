# -*- coding: utf-8 -*-
#############################################################################
#############################################################################
{
    'name': "Animated Snippets",
    'version': '1.0.0',
    'category': 'Website',
    'summary': """Animated Snippets for Websites.""",
    'description': """Variety of Snippets With Animations to Beautify 
     your Website""",
    'author': "",
    'company': '',
    'maintainer': '',
    'website': "",
    'depends': ['base', 'website',],
    'data': [
        'views/snippets/snippets_templates.xml',
        'views/snippets/a_features_01_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/animated_snippet/static/src/css/a_features_01.css',
        ]},
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
