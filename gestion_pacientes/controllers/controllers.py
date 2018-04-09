# -*- coding: utf-8 -*-
from odoo import http

# class GestionPacientes(http.Controller):
#     @http.route('/gestion_pacientes/gestion_pacientes/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_pacientes/gestion_pacientes/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_pacientes.listing', {
#             'root': '/gestion_pacientes/gestion_pacientes',
#             'objects': http.request.env['gestion_pacientes.gestion_pacientes'].search([]),
#         })

#     @http.route('/gestion_pacientes/gestion_pacientes/objects/<model("gestion_pacientes.gestion_pacientes"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_pacientes.object', {
#             'object': obj
#         })