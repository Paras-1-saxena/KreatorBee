# -*- coding: utf-8 -*-
{
    'name': 'Kreator Website',
    'description': 'Kreator',
    'depends': ['website'],
    'data': [
        'views/templates.xml',
    ],
    "assets": {
        "web._assets_frontend_helpers": [
            'kreator_website/static/src/scss/**/*'
        ]
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
