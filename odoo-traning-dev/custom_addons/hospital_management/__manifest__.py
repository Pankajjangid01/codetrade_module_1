{
    'name': 'Hospital Management',
    'version': '18.0.0.1',
    'summary': 'Hospital Management system to manage Patient Data',
    'author': 'Codetrade.io',
    'depends': ['account', 'mail'],
    'website': 'https://www.codetrade.io/',
    'category': "Hospital Management",
    'data': [
        'security/ir.model.access.csv',
        'views/menuitems.xml',
        'views/patient_views.xml',
        'views/report_paper_format.xml',
        'views/patient_report.xml',
        'views/patient_details_report.xml',
        'views/appointment_views.xml',
        'views/appointment_report_server_action.xml',
        'views/appointment_report.xml',
        'views/prescription_views.xml'
    ],
    'installable': True,
    'license': 'LGPL-3',
}
