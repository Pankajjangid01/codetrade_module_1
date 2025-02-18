from odoo import http
from odoo.http import request

class EmployeeController(http.Controller):

    @http.route('/employee-details',type='http',auth='public',website=True)
    def employee_detail(self, **arg):
        """This function fetches the Employee data from the odoo database and render it in the web page"""
        try:
            employee_detail = request.env['company.employee'].sudo().search([])
            values = {'record': employee_detail}
            return request.render('codetrade_module.all_employee_data', values)
        except Exception as exe:
           return f"Error in rendering the page {str(exe)}"
    