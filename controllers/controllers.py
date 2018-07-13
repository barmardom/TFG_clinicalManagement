# -*- coding: utf-8 -*-
from odoo import http

# class GestionClinica(http.Controller):
#     @http.route('/gestion_clinica/gestion_clinica/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_clinica/gestion_clinica/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_clinica.listing', {
#             'root': '/gestion_clinica/gestion_clinica',
#             'objects': http.request.env['gestion_clinica.gestion_clinica'].search([]),
#         })

#     @http.route('/gestion_clinica/gestion_clinica/objects/<model("gestion_clinica.gestion_clinica"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_clinica.object', {
#             'object': obj
#         })