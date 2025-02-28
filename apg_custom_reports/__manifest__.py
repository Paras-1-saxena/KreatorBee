
{
    'name': 'Apg Report Module',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Generate and download report template.',
    'depends': ['account','mail','base'],  # Ensure it depends on the Invoicing module
    'data': [
        'security/ir.model.access.csv',
        'views/account_payment.xml',
        'views/menu.xml'
    ],
    'installable': True,
    'application': False,
}
