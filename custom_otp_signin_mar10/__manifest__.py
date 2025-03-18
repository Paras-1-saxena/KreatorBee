# -*- coding: utf-8 -*-
{
    "name": "Custom Otp Signin",
    "version": "18.0.1.0",
    "author": "Apagen solutions",
    'category': 'Tools',
    "website": "",
    "description": """
        """,
    "summary": """
        This module allows the user signin via OTP.
    """,
    'depends': ['base', 'mail', 'web', 'website', 'auth_signup'],
    'data': [
        "security/ir.model.access.csv",
        "security/security_group.xml",
        "views/otp_verification.xml",
        "views/login_view.xml",
        "data/cron.xml"
    ],
    "license": "LGPL-3",
    'installable': True,
    'application': False,
}
