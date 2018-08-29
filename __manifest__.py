# -*- coding: utf-8 -*-
{
    'name': "Gestion de Clínica",

    'summary': """
        Gestión de un centro de reprodución asistida""",

    'description': """
        Este módulo permite a los profesionales de la clínica:
            -Gestionar la lista completa de medicamentos registrados (vademecum), junto con su eficacia en pacientes.
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
    'category': 'Gestion','Medicina'
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/access.xml',
        'views/templates.xml',
        'views/pacientes.xml',
        'views/medicamentos.xml',
        'views/visitas.xml',
        'views/dosis.xml',
        'views/alertas.xml',
        'views/estadisticas.xml',
        'security/ir.model.access.csv'
        
    ],
    'css': [
        'static/src/css/style.css'
    ],
    'js': [
        'static/src/js/javascriptfile.js'
    ],
    #'qweb': [
    #    'static/src/xml/qweb_file.xml',
    #],
    # only loaded in demonstration mode
    #'demo': [
    #    'demo/demo.xml',
    #],
}
