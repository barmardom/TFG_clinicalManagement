# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class gestion_medicamentos(models.Model):
#     _name = 'gestion_medicamentos.gestion_medicamentos'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class Medicamento(models.Model):
    _name = 'gestion_medicamentos.medicamento'

    nombre = fields.Char(
        string="Nombre",
        size=60,
        required=True,
        help='Nombre del medicamento'
    )
    codigo = fields.Char(
        string="Código",
        size=9,
        required=True,
        help='Codigo del medicamento'
    )
    presentacion = fields.Char(
		string='Presentacion',
		help='Presentacion del medicamento'
	)
    cantidad = fields.Char(
		string='Cantidad',
		help='Cantidad de medicamento'
	)
    unidad = fields.Char(
		string='Unidad',
		help='Unidad de la cantidad'
	)
    enlace = fields.Char(
		string='Enlace',
		help='Enlace del medicamento'
	)
	
    #administracion = fields.Char(string="Administración")



#    name = fields.Char(
#        string="Name",                   # Etiqueta opcional para el Campo
#        compute="_compute_name_custom",  # Transforma un campo normal en campo funcion
#        store=True,                      # Si el campo es calculado, esta propiedad lo grabara en base de datos como una columna.
#        select=True,                     # Fuerza el indice en un campo.
#        readonly=True,                   # Campo solo lectura en las Vistas.
#        inverse="_write_name"            # Recalcular cuando ocurre un evento
#        required=True,                   # Campo Obligatorio.
#        translate=True,                  # Convertir texto para multiples traducciones.
#        help='Blabla',                   # Globo de ayuda.
#        company_dependent=True,          # Convierte el campo a campo de tipo propiedad(property)
#        search='_search_function'        # Funcion de Búsqueda para campos calculados.
#    )
