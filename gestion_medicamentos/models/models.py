# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Medicamento(models.Model):
    _name = 'gestion_medicamentos.medicamento'
    _rec_name = 'nombre'

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
	
