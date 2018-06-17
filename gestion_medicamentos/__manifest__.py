# -*- coding: utf-8 -*-
{
    'name': "gestionMedicamentos",

    'summary': """
        Gestión de Medicamentos de existentes v3""",

    'description': """
        Este módulo permite a los Doctores tener acceso al listado completo fármacos existentes, este les facilita la gestión de dosis a los pacientes
        ya que tendran información disponible sobre los medicamentos recetados al instante.
        -> Gestión de dosis
        -> Estudio estadístico
    """,

    'author': "Bartolomé MD (github.com/barmardom)",
    'website': "http://www.yourcompany.com",

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
        'views/medicamentos.xml',
        'views/templates.xml',
    ],
    'css': [
        'static/src/css/style.css'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
