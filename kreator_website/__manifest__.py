# -*- coding: utf-8 -*-
{
    'name': 'Kreator Website',
    'description': 'Kreator',
    'depends': ['website', 'web'],
    'data': [
        'views/templates.xml',
        'views/pixel_integration.xml',
        'views/video_editing_ayushman.xml',
        'views/freelancing_employees_ayushman.xml',
        'views/freelancing_genZ_ayushmaan.xml',
        'views/lead_generation_lakshit.xml',
        'views/paras_affiliate_marketing_basic.xml'
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
