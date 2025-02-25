{
    'name': 'Sale Management',
    'version': '18.0.0.1',
    'summary': 'Sale Management system to manage and download invoice of Data',
    'author': 'Codetrade.io',
    'depends': ['sale'],
    'website':'https://www.codetrade.io/',
    'category':"Sale",
    'data': [
        'security/ir.model.access.csv',
        'views/sale_invoice_view.xml',
        'report/sale_invoice_paper_format.xml',
        'report/sale_invoice_report.xml',
        'report/sale_invoice_template.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
