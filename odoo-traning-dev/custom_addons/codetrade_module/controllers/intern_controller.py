from odoo import http
from odoo.http import request

class InternController(http.Controller):
    @http.route('/intern-details',type='http',auth='public',website=True)
    def intern_detail(self, **arg):
        """This function fetches the Intern data from the odoo database and render it on the web page"""
        try:
            intern_detail = request.env['intern.register'].sudo().search([])
            values = {'record': intern_detail}
            return request.render('codetrade_module.all_intern_data', values)
        except Exception as exe:
           return f"Error in rendering the page {str(exe)}"