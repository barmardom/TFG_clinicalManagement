# -*- coding: utf-8 -*-

from odoo import models, fields, api, time
from datetime import timedelta
import datetime


class Medicamento(models.Model):
    _name = 'gestion_clinica.medicamento'
    _rec_name = 'nombre'

    nombre = fields.Char(
        string="Nombre",
        size=60,
        required=True,
        help='Nombre del medicamento',
        translate=True
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
    dosis_ids = fields.One2many('gestion_clinica.dosis', 'medicamento_id', string='Medicamento de la dosis')

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
    donante = fields.Boolean(
        string='Donante',
        help='Donante de ovulos o semen'
    )
    doctor_id = fields.Many2one('res.users', string='Doctor', required=True)
    patologia_ids = fields.One2many('gestion_clinica.patologia', 'paciente_id', string='Patologia')
    visita_ids = fields.One2many('gestion_clinica.visita', 'paciente_id', string='Visita')
    dosis_ids = fields.One2many('gestion_clinica.dosis', 'paciente_id', string='Dosis2')
    #todasDosis = fields.One2many(related='visita_ids.dosis_ids', store=True)
    
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
    _order = "fecha desc"

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
    pruebas = fields.Boolean(
        string='Pruebas',
        help='Pruebas médicas a realizar'
    )
    paciente_id = fields.Many2one('gestion_clinica.paciente', ondelete='cascade', string="Paciente")
    dosis_ids = fields.One2many('gestion_clinica.dosis', 'visita_id', string='Dosis relacionadas')
    #Otras
    nombreDoctor = fields.Char(related='paciente_id.doctor_id.name', store=True, string="Doctor", readonly=True)
    idDoctor = fields.Integer(related='paciente_id.doctor_id.id', store=True, string="ID Doctor", readonly=True)

class Dosis(models.Model):
    _name = 'gestion_clinica.dosis'
    _description = 'Dosis'
    _rec_name = 'duraccion'

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
    tipo = fields.Selection(
        [('toma','Toma'),('4','Aplicación')],
        string='Tipo'
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
    especificaciones = fields.Text(
        string="Especificaciones",
        help='Especificaciones'
    )
    visita_id = fields.Many2one('gestion_clinica.visita', ondelete='cascade', string="Visita")
    medicamento_id = fields.Many2one('gestion_clinica.medicamento', string="Medicamento", required=True)
    paciente_id = fields.Many2one('gestion_clinica.paciente', ondelete='cascade', string="Paciente", required=True)
   
    @api.one
    @api.depends('fechaInicio', 'duraccion')
    def _get_fecha_fin(self):
        if self.fechaInicio and self.duraccion:
            fechaDeInicio = datetime.datetime.strptime(self.fechaInicio, '%Y-%m-%d')
            self.fechaFin = fechaDeInicio + datetime.timedelta(self.duraccion)