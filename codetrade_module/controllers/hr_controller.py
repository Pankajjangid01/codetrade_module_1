from odoo import http
from odoo.http import request

class HrController(http.Controller):
    @http.route('/hr-details',type='http',auth='public',website=True)
    def hr_detail(self, **arg):
        """This function fetches the HR data from the odoo database and render it in the web page"""
        try:
            hr_detail = request.env['company.hr'].sudo().search([])
            values = {'record': hr_detail}
            return request.render('codetrade_module.all_hr_data', values)
        except Exception as exe:
           return f"Error in rendering the page {str(exe)}"
