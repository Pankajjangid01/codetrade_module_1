from odoo import http
from odoo.http import request

class EmployeeController(http.Controller):

    @http.route('/employee-details', type='http', auth='public', website=True)
    def employee_detail(self, **kwargs):
        """Fetch Employee and Intern data from the database and render it on the webpage."""
        try:
            employee_detail = request.env['company.employee'].sudo().search([])
            values = {'record': employee_detail}
            return request.render('codetrade_module.all_employee_data', values)
        except Exception as exe:
            return f"Error in rendering the page {str(exe)}"

    @http.route('/delete-employee/<int:employee_id>', type='http', auth='public', website=True)
    def delete_employee(self, employee_id, **kwargs):
        """Delete an employee record based on the given employee_id."""
        try:
            employee = request.env['company.employee'].sudo().browse(employee_id)
            if employee:
                employee.unlink()
            return request.redirect('/employee-details')
        except Exception as exe:
            return f"Error in deleting the record: {str(exe)}"

    @http.route('/employee-details/<int:employee_id>', type='http', auth='public', website=True)
    def employee_full_detail(self, employee_id):
        """Fetch and display full details of a particular employee"""
        try:
            employee = request.env['company.employee'].sudo().browse(employee_id)
            if not employee.exists():
                return "Employee Not Found"
            
            values = {'employee': employee}
            return request.render('codetrade_module.single_employee_detail', values)
        except Exception as exe:
            return f"Error in rendering the page {str(exe)}"