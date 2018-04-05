# -*- coding: utf-8 -*-
from odoo import http

# class GestionMedicamentos(http.Controller):
#     @http.route('/gestion_medicamentos/gestion_medicamentos/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_medicamentos/gestion_medicamentos/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_medicamentos.listing', {
#             'root': '/gestion_medicamentos/gestion_medicamentos',
#             'objects': http.request.env['gestion_medicamentos.gestion_medicamentos'].search([]),
#         })

#     @http.route('/gestion_medicamentos/gestion_medicamentos/objects/<model("gestion_medicamentos.gestion_medicamentos"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_medicamentos.object', {
#             'object': obj
#         })