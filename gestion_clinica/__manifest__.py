# -*- coding: utf-8 -*-
{
    'name': "Gestion de Clínica",

    'summary': """
        Gestión de clínica""",

    'description': """
        Este módulo permite a los profesionales de la clínica:
            -Gestionar la lista completa de medicamentos registrados (vademecum), junto con su eficiencia global en los pacientes.
            -Gestionar a los pacientes, crear, editar, borrar. Así como las patologías, visitas, dosis y alertas asociados a ellos.
            -Estudio de estadísticas por parte de los proveedores de fármacos
        **Como funcionalidades a desarrollar en el futuro destacan:
            -Sistema para gestionar el inventario completo disponible (desde medicamentos a maquinarias).
            -Acceso a pacientes
    """,

    'author': "Bartolomé MD",
    'website': "github.com/barmardom",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/access.xml',
        'views/pacientes.xml',
        'views/medicamentos.xml',
        'views/visitas.xml',
        'views/estadisticas.xml',
        'views/alertas.xml',

    ],
    'css': [
        'static/src/css/style.css'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
