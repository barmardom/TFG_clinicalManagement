# -*- coding: utf-8 -*-

from odoo import models, fields, api, time
from datetime import timedelta
import datetime
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

class Medicamento(models.Model):
    _name = 'gestion_clinica.medicamento'
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

class Paciente(models.Model):
    _name = 'gestion_clinica.paciente'
    _description = 'Pacientes'
    _rec_name = 'nif'

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
        default=time.strftime('1900-01-01'),
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
    patologia_ids = fields.One2many('gestion_clinica.patologia', 'paciente_id', string='Patologia')
    visita_ids = fields.One2many('gestion_clinica.visita', 'paciente_id', string='Visita')
    
class Patologia(models.Model):
    _name = 'gestion_clinica.patologia'
    _description = 'Patologias'
    nombre = fields.Char(
        string="Nombre",
        size=20,
        required=True,
        help='Nombre de patologia'
    )
    descripcion = fields.Text(
        string="Descripción",
        help='Descripción de patologia'
    )
    paciente_id = fields.Many2one('gestion_clinica.paciente', ondelete='cascade', string="Paciente")

class Visita(models.Model):
    _name = 'gestion_clinica.visita'
    _description = 'Visitas'
    _rec_name = 'asunto'

    fecha = fields.Date(
        string='Fecha',
        help='Fecha de la visita',
        required=True
    )
    asunto = fields.Char(
        string="Asunto",
        size=20,
        required=True,
        help='Tema relacionado con la visita'
    )
    descripcion = fields.Text(
        string="Descripción",
        help='Descripción'
    )
    tratamiento = fields.Boolean(
        string='Tratamiento',
        help='Tratamiento'
    )
    #REVISAR
    pruebas = fields.Char(
        string='Pruebas'
    )
    paciente_id = fields.Many2one('gestion_clinica.paciente', ondelete='cascade', string="Paciente")
    dosis_ids = fields.One2many('gestion_clinica.dosis', 'visita_id', string='Dosis de la visita')

class Dosis(models.Model):
    _name = 'gestion_clinica.dosis'
    _description = 'Dosis'
    _rec_name = 'duraccion'

    #@api.model
    #def _get_fecha_fin(self):
    #    date_1 = datetime.datetime.strptime(self.fechaInicio, "%m/%d/%y")
    #    end_date = date_1 + datetime.timedelta(days=10)
    #    return end_date.date()


    fechaInicio = fields.Date(
        string='Fecha de inicio',
        help='Fecha de inicio',
        required=True
    )
    duraccion = fields.Integer(
        string="Duraccion",
        required=True,
        help='Duraccion en días del tratamiento con la dosis'
    )
    cantidad = fields.Integer(
        string='Cantidad'
    )
    frecuencia = fields.Selection(
        [('2','2 horas'),('4','4 horas'),('8','8 horas'),('12','12 horas'),('24','24 horas')],
        string='Frecuencia',
        help='Cada cuanto tiempo se toma la dosis'
    )
    cancelado = fields.Boolean(
        string='Cancelado',
        help='Cancelado'
    )
    eficiencia = fields.Selection(
        [('muyBaja','Muy baja'),('baja','Baja'),('media','Media'),('alat','Alta'),('muyAlta','Muy alta')],
        string='Eficiencia'
    )
    fechaFin = fields.Date('Fecha de fin',
        compute='_get_fecha_fin',
        readonly=True,
        help='Fecha de fin para la toma de la dosis'
        )
    visita_id = fields.Many2one('gestion_clinica.visita', ondelete='cascade', string="Visita")

    @api.depends('fechaInicio', 'duraccion')
    def _get_fecha_fin(self):
        if self.fechaInicio and self.duraccion:
            fechaDeInicio = datetime.datetime.strptime(self.fechaInicio, '%Y-%m-%d')
            self.fechaFin = fechaDeInicio + datetime.timedelta(self.duraccion)