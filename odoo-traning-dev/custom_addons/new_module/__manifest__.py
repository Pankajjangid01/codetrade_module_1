{
    'name': 'Student Data',
    'version': '18.0.0.1',
    'summary': 'Module to manage student details',
    'author': 'Codetrade.io',
    'depends': ['base','purchase'],
    'category':"School Management",
    'data': [
        'data/student.student.csv',
        'data/student_data_file.xml',
        'security/ir.model.access.csv',
        'security/security_groups.xml',
        'views/student_details_views.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
