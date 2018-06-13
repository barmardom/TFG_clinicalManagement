# -*- coding: utf-8 -*-
{
    'name': "gestionPacientes",

    'summary': """
        Gestión del historial clínico/dosis""",

    'description': """
        Este módulo permite principalmente a los Doctores, pero tambien a Pacientes tener acceso a la gestión de dosisself.
        El paciente solo puede consultar y los doctores gestionar el historial clínico de este teniendo como parte principal las Dosis.
        Otros modulos relacionados:
            -> Gestión de medicamentos
            -> Estudio estadístico
    """,

    'author': "Bartolomé MD",
    'website': "github.com/barmardom)",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/pacientes.xml',
        'views/templates.xml',
        'security/access.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
