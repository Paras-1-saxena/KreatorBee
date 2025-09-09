
{
    'name': 'Apg Report Module',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Generate and download report template.',
    'depends': ['account','mail','base', 'sale', 'apg_sale_commission'],  # Ensure it depends on the Invoicing module
    'data': [
        'security/ir.model.access.csv',
        'views/account_payment.xml',
        'views/sales_custom_report.xml',
        'views/sales_commission_report.xml',
        'views/menu.xml',
        'views/custom_layout.xml',
    ],
    'installable': True,
    'application': False,
}
