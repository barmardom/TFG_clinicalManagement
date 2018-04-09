# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class gestion_pacientes(models.Model):
#     _name = 'gestion_pacientes.gestion_pacientes'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class Medicamento(models.Model):
    _name = 'gestion_pacientes.paciente'

    nombre = fields.Char(
        string="Nombre",
        size=20,
        required=True,
        help='Nombre del o la paciente'
    )
    apellidos = fields.Char(
        string="Apellidos",
        size=50,
        required=True,
        help='Apellidos del o la paciente'
    )
    nif = fields.Char(
		string='NIF',
		help='Documento de identificacion del o la paciente'
	)
    fechaNacimiento = fields.Char(
		string='Fecha de nacimiento',
		help='Fecha de nacimiento del o la paciente'
	)
    genero = fields.Char(
		string='Género',
		help='Genero del o la paciente'
	)
    telefono = fields.Char(
		string='Teléfono',
		help='Enlace del o la medicamento'
	)
    email = fields.Char(
		string='Email',
		help='Enlace del o la medicamento'
	)
