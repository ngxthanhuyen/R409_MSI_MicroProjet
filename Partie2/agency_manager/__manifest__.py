{
    'name': "Agency Manager",
    'version': '1.0',
    'author': "NGUYEN Thanh Uyen",
    'category': 'Business',
    'summary': "Gestion des agences UberCircuit",
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/agency_view.xml',
    ],
    'installable': True,
    'application': True,
}

