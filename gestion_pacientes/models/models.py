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


#class res_users(models.Model):
#    _inherit = 'res.users'  
#
#    _columns = {            
#       'doctor_u' : fields.many2one('doctores', 'Doctor', help="Selecciona doctor"),           
#    }
#res_users()

class Paciente(models.Model):
    _name = 'gestion_pacientes.paciente'
    _description = 'Pacientes'
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
		help='Documento de identificacion del o la paciente',
		required=True
	)
    fechaNacimiento = fields.Date(
		string='Fecha de nacimiento',
		help='Fecha de nacimiento del o la paciente',
		required=True
	)
    genero = fields.Selection(
		[('femenino','Femenino'),('masculino','Masculino')],
        string='Género'
	)
    telefono = fields.Char(
		string='Teléfono',
		help='Télefono del o la paciente'
	)
    email = fields.Char(
		string='Email',
		help='Correo del o la paciente'
	)
    poblacion = fields.Char(
        string='Población',
        help='Lugar de residencia'
    )
    doctor_id = fields.Many2one('res.users', string='Doctor')
    patologia_ids = fields.One2many('gestion_pacientes.patologia', 'paciente_id', string='Patologia')
    


class Patologia(models.Model):
    _name = 'gestion_pacientes.patologia'
    _description = 'Patologias'
    nombre = fields.Char(
        string="Nombre",
        size=20,
        required=True,
        help='Nombre de patologia'
    )
    nombre = fields.Text(
        string="Descripción",
        size=260,
        help='Descripción de patologia'
    )
    paciente_id = fields.Many2one('gestion_pacientes.paciente', ondelete='cascade', string="Paciente")