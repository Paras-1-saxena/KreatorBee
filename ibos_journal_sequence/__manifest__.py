
{
    'name': "Add  custom journal Sequence in odoo 16",
    'summary': """
       Odoo16 journal sequence.""",
    'category': 'Extra Tools',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['account'],
    'license': 'LGPL-3',
    'data': [
        'views/account.xml',
    ],
    'application': False
}
