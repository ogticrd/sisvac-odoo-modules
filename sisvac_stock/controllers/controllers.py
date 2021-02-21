# -*- coding: utf-8 -*-
# from odoo import http


# class SisvacStock(http.Controller):
#     @http.route('/sisvac_stock/sisvac_stock/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sisvac_stock/sisvac_stock/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sisvac_stock.listing', {
#             'root': '/sisvac_stock/sisvac_stock',
#             'objects': http.request.env['sisvac_stock.sisvac_stock'].search([]),
#         })

#     @http.route('/sisvac_stock/sisvac_stock/objects/<model("sisvac_stock.sisvac_stock"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sisvac_stock.object', {
#             'object': obj
#         })
