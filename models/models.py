# -*- coding: utf-8 -*-

from odoo import exceptions
from odoo import models, fields, api, time
from datetime import timedelta
import datetime
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from openerp.api import Environment
from urlparse import urlparse, parse_qs
import os
import inspect


class Medicamento(models.Model):
    _name = 'gestion_clinica.medicamento'
    _description = 'Medicamento'
    _rec_name = 'codigo'

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
        help='Tipo de fármaco',
        size=40,
        required=True,
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
    estado = fields.Selection(
        [('activo','Activo'),('retirado','Retirado')],
        string='Estado',
        default='activo',
        help='Informa si el fármaco está activo o retirado'
    )
    #Derivadas
    eficaciaMedia = fields.Integer(
        string='Eficacia',
        help='Eficacía general del medicamento',
        readonly=True,
        compute ='calcula_eficacia'
    )
    dosisPuntuadas = fields.Integer(
        string='Dosis relacionadas y evaluadas',
        help='Muestra el número de dosis relacionadas con este medicamento que el doctor ha puntuado y que por tanto se han tenido en cuenta para calcular la eficacia del fármaco.',
        readonly=True,
        compute ='calcula_dosis_puntuadas'
    )
    totalDosis = fields.Integer(
        string='Dosis relacionadas',
        readonly=True,
        compute ='calcula_dosis_totales'
    )
    dosis_ids = fields.One2many('gestion_clinica.dosis', 'medicamento_id', string='Medicamento de la dosis')

    @api.multi
    def calcula_eficacia(self):
        suma_eficacia = 0
        cont = 0
        existenDosis = False

        for dosis in self.dosis_ids:
            if dosis.eficiencia:
                eficacia = int(dosis.eficiencia)
                suma_eficacia = suma_eficacia + eficacia
                cont = cont + 1
        
        if (cont != 0):
            res = int(suma_eficacia/cont)
            self.eficaciaMedia = res

    @api.multi
    def calcula_dosis_puntuadas(self):
        cont = 0
    
        for dosis in self.dosis_ids:
            if dosis.eficiencia:
                cont = cont + 1
        
        if (cont != 0):
            self.dosisPuntuadas = cont

    @api.one
    @api.depends('dosis_ids')
    def calcula_dosis_totales(self):
        self.totalDosis = len(self.dosis_ids)



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
        help='Apellidos del paciente',
        size=50,
        required=True
    )
    nif = fields.Char(
		string='NIF',
		help='Documento de identificacion del paciente',
		required=True
	)
    fechaNacimiento = fields.Date(
		string='Fecha de nacimiento',
		help='Día, mes y año de nacimiento del paciente',
        default=time.strftime('1900-01-01'),
		required=True
	)
    genero = fields.Selection(
		[('femenino','Femenino'),('masculino','Masculino')],
        string='Género',
        required=True
	)
    telefono = fields.Char(
		string='Teléfono',
		help='Número de teléfono del paciente'
	)
    email = fields.Char(
		string='Email',
		help='Correo electrónico del paciente',
        required=True
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
    dosis_ids = fields.One2many('gestion_clinica.dosis', 'paciente_id', string='Dosis')

    @api.one
    @api.constrains('email')
    def _check_function(self):
        if (("@" not in self.email) or ("." not in self.email)):
            raise exceptions.ValidationError("El campo email no es válido.")

class Patologia(models.Model):
    _name = 'gestion_clinica.patologia'
    _description = 'Patologias'
    
    nombre = fields.Char(
        string="Nombre",
        help='Nombre de patologia',
        size=60,
        required=True
    )
    descripcion = fields.Text(
        string="Descripción",
        help='Descripción de patologia'
    )
    paciente_id = fields.Many2one('gestion_clinica.paciente', string="Paciente", required=True, ondelete='cascade')

class Visita(models.Model):
    _name = 'gestion_clinica.visita'
    _description = 'Visitas'
    _rec_name = 'asunto'
    _order = "fecha desc"

    fecha = fields.Date(
        string='Fecha',
        help='Fecha de la visita',
        required=True,
    )
    asunto = fields.Char(
        string="Asunto",
        help='Tema relacionado con la visita',
        size=30,
        required=True   
    )
    descripcion = fields.Text(
        string="Descripción",
        help='Descripción'
    )
    tratamiento = fields.Boolean(
        string='Tratamiento',
        help='Si existe o no tratamiento con dosis para la visita'
    )
    pruebas = fields.Boolean(
        string='Pruebas',
        help='Pruebas médicas a realizar, de existir se detallan en la descripción de la visita'
    )
    paciente_id = fields.Many2one('gestion_clinica.paciente', string="Paciente", required=True, ondelete='cascade')
    dosis_ids = fields.One2many('gestion_clinica.dosis', 'visita_id', string='Dosis relacionadas')
    #Derivadas
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
        help='Fecha inicial en la que se comienza a tomar la dosis',
        required=True
    )
    duraccion = fields.Integer(
        string="Duraccion",
        help='Duraccion en días del tratamiento con la dosis',
        required=True   
    )
    cantidad = fields.Integer(
        string='Cantidad',
        help='Número de tomas o aplicaciones en aplicación'
    )
    tipo = fields.Selection(
        [('toma','Toma'),('aplicacion','Aplicación')],
        string='Tipo',
        help='Forma de aplicar la dosis'
    )
    frecuencia = fields.Selection(
        [('2','2 horas'),('4','4 horas'),('8','8 horas'),('12','12 horas'),('24','24 horas')],
        string='Frecuencia',
        help='Periodo de tiempo que datalla cada cuanto se debe de tomar la dosis'
    )
    cancelado = fields.Boolean(
        string='Cancelado',
        help='Cancelación o no de la dosis'
    )
    eficiencia = fields.Selection(
        [('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10')],
        string='Eficacia',
        help='Eficacía del medicamento asoiciado en la dosis sobre el paciente'
    )
    especificaciones = fields.Text(
        string="Especificaciones",
        help='Especificaciones y/o detalles'
    )
    alertaEnviada = fields.Boolean(
        string='Notificación',
        help='Informa si se ha enviado o no notificación al paciente sobre la proximidad de fin de la dosis',
        readonly=True
    )
    #Derivada
    fechaFin = fields.Date('Fecha de fin',
        compute ='_get_fecha_fin',
        help='Fecha de fin del tratamiento de la dosis',
        readonly=True
    )
    visita_id = fields.Many2one('gestion_clinica.visita', store=True, ondelete='cascade', string="Visita", required=True)
    medicamento_id = fields.Many2one('gestion_clinica.medicamento', string="Medicamento", required=True)
    paciente_id = fields.Many2one(related='visita_id.paciente_id', string="Paciente", required=True, readonly=True, ondelete='cascade') 
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

        pacientes = self.env['gestion_clinica.paciente'].search([]) #Ya filtra por los pacientes que vel el doctor logeado. Caso de que se quiera limitar la busqueda: .search([('id','=', '2')], limit=1)
        
        gmailUser = ''
        gmailPassword = ''

        directory_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        dir_file = os.path.join(directory_path, 'pdata.txt')

        with open(dir_file,'r') as f:
            gmailUser = f.readline().rstrip('\n')
            gmailPassword = f.readline().rstrip('\n')


        for paciente in pacientes:
            if ((len(gmailUser) > 1) and (len(gmailUser) > 0)):
                for dosis in paciente.dosis_ids:
                    fecha_sumada = datetime.datetime.now() + datetime.timedelta(7)
                    date_fecha = datetime.datetime.strftime(fecha_sumada, '%Y-%m-%d')
                    fecha_hoy = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
                    if (dosis.cancelado == False) and (dosis.alertaEnviada ==False) and (date_fecha > dosis.fechaFin) and (dosis.fechaFin >= fecha_hoy):

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

###############################################################################


class Estadistica(models.TransientModel):
    _name = 'gestion_clinica.estadistica'
    _description = 'Estadistica'


    @api.multi
    def carga_graficos(self):
        return 1