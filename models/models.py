# -*- coding: utf-8 -*-

from odoo import models, fields, api, time
from datetime import timedelta
import datetime
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from openerp.api import Environment
from urlparse import urlparse, parse_qs

class Medicamento(models.Model):
    _name = 'gestion_clinica.medicamento'
    _description = 'Medicamento'
    _rec_name = 'nombre'

    nombre = fields.Char(
        string="Nombre",
        help='Nombre completo del fármaco',
        size=60,
        required=True,
        translate=True
    )
    codigo = fields.Char(
        string="Código",
        help='Código de identificacion único del fármaco',
        size=9,
        required=True
    )
    presentacion = fields.Char(
        string='Presentacion',
        help='´Tipo de fármaco',
        size=40,
    )
    cantidad = fields.Char(
        string='Cantidad',
        help='Cantidad de dosis del fármaco'
    )
    unidad = fields.Char(
        string='Unidad',
        help='Unidad en la que se expresa la cantidad de fármaco'
    )
    enlace = fields.Char(
        string='Enlace',
        help='Enlace del fármaco a una web informativa'
    )
    dosis_ids = fields.One2many('gestion_clinica.dosis', 'medicamento_id', string='Medicamento de la dosis')

class Paciente(models.Model):
    _name = 'gestion_clinica.paciente'
    _description = 'Pacientes'
    _rec_name = 'nif'


    nombre = fields.Char(
        string="Nombre",
        help='Nombre del paciente',
        size=20,
        required=True,
    )
    apellidos = fields.Char(
        string="Apellidos",
        help='Apellidos del o la paciente',
        size=50,
        required=True
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
    #REVISAR
    dosis_ids = fields.One2many('gestion_clinica.dosis', 'paciente_id', string='Dosis')

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

    @api.one
    @api.depends('fechaInicio', 'duraccion')
    def _get_fecha_fin(self):
        if self.fechaInicio and self.duraccion:
            fechaDeInicio = datetime.datetime.strptime(self.fechaInicio, '%Y-%m-%d')
            self.fechaFin = fechaDeInicio + datetime.timedelta(self.duraccion)

    #@api.multi
    #@api.onchange('visita_id')
    #def _get_filtra_pacientes_visitas_dosis(self):
        #url = "http://localhost/web?debug=1#id=2&view_type=form&model=gestion_clinica.paciente&menu_id=235&action=264"
        #uri = urlparse(url)
        #qs = uri.fragment
        #final = parse_qs(qs).get('id', None)
    #    visit = self.env['gestion_clinica.visita'].search([('id','=', self.visita_id.id)], limit=1)

    #    res = self.env['gestion_clinica.paciente'].search([('id','=', visit.id)], limit=1)
    #    return res

    #@api.multi
    #def _get_filtra_visitas(self):
    #    res = self.env['gestion_clinica.visita'].search([('id','=', '4')], limit=1)
    #    return res

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
    alertaEnviada = fields.Boolean(
        string='Alerta enviada',
        help='Alerta',
        readonly=True
    )
    visita_id = fields.Many2one('gestion_clinica.visita', store=True, ondelete='cascade', string="Visita")
    medicamento_id = fields.Many2one('gestion_clinica.medicamento', string="Medicamento", required=True)
    paciente_id = fields.Many2one(related='visita_id.paciente_id', string="Paciente", required=True, readonly=True) 
    #default=lambda self: self.env['gestion_clinica.paciente'].search([('id', '=', self.idPaciente)], limit=1)
   



class Alerta(models.TransientModel):
    _name = 'gestion_clinica.alerta'
    _description = 'Alerta'

    @api.multi
    def envia_email(self):
        #url = "http://localhost/web?debug=1#id=2&view_type=form&model=gestion_clinica.paciente&menu_id=235&action=264"
        #uri = urlparse(url)
        #qs = uri.fragment
        #final = parse_qs(qs).get('id', None)

        pacientes = self.env['gestion_clinica.paciente'].search([]) #Caso de que se quiera limitar la busqueda: .search([('id','=', '2')], limit=1)

        for paciente in pacientes:
            for dosis in paciente.dosis_ids:
                fecha_sumada = datetime.datetime.now() + datetime.timedelta(7)
                date_fecha = datetime.datetime.strftime(fecha_sumada, '%Y-%m-%d')
                fecha_hoy = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
                if (dosis.cancelado == False) and (dosis.alertaEnviada ==False) and (date_fecha > dosis.fechaFin) and (dosis.fechaFin >= fecha_hoy):

                    gmailUser = '***'
                    gmailPassword = '***'
                    recipient = paciente.email

                    asunto = dosis.visita_id.asunto.encode('utf-8')
                    medicamento = dosis.medicamento_id.nombre.encode('utf-8')
                    fechaF = str(dosis.fechaFin)
                    nombreCompleto = paciente.nombre.encode('utf-8') + ' ' + paciente.apellidos.encode('utf-8')
                    nombreDoctor = dosis.visita_id.paciente_id.doctor_id.name.encode('utf-8')
                    html = """\
                    <html>
                    <head></head>
                    <body>
                    <tr>
                    <td>
                      <table border="0" cellpadding="0" cellspacing="0">
                        <tr>
                          <td>
                            <p>Hola <strong>{nombreCompleto}</strong>,</p>
                            <p>Desde Inebir le recordamos que su tratamiento actual con <i>"{medicamento}"</i> relacionado con la visita <i>{asunto}</i>, termina muy pronto <strong>{fechaF}</strong>.</p>
                            <p>No dude en contactar con nosotros o con su doctor ({nombreDoctor}) ante cualquier duda.</p>
                            <p>Coordiales saludos, el equipo de Inebir.</p>
                          </td>
                        </tr>
                      </table>
                    </td>
                    </tr>
                    </body>
                    </html>
                    """.format(nombreCompleto=nombreCompleto, medicamento=medicamento, asunto=asunto, fechaF=fechaF, nombreDoctor=nombreDoctor)

                    msg = MIMEMultipart()
                    msg['From'] = gmailUser
                    msg['To'] = recipient
                    msg['Subject'] = "Notificacion"
                    cuerpo = MIMEText(html, 'html')
                    msg.attach(cuerpo)

                    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
                    mailServer.ehlo()
                    mailServer.starttls()
                    mailServer.ehlo()
                    mailServer.login(gmailUser, gmailPassword)
                    mailServer.sendmail(gmailUser, recipient, msg.as_string())
                    mailServer.close()

                    dosis.alertaEnviada = True



