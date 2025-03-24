from odoo import http
from odoo.http import request

class EmployeeForm(http.Controller):

    @http.route('/employee/form', type='http', auth="public", website=True)
    def employee_form(self, **kwargs):
        """Render the employee form"""
        intern_ids = request.env['intern.register'].sudo().search([])
        employee = request.env['company.employee'].sudo().fields_get()
        tech_list = employee["tech_stack"]["selection"]
        tech_stack = []
        for tech in tech_list:
            tech_stack.append(tech[0])
        datas = {
            'intern_ids': intern_ids,
            'employee_rec':tech_stack
        }
        return request.render('codetrade_module.employee_form_template',datas)

    @http.route('/employee/form/submit', type='http', auth="public", website=True, methods=['POST'])
    def submit_employee_form(self, **post):
        """Handle form submission and save data"""
        intern_ids = request.httprequest.form.getlist('intern_name_ids')
        try:
            intern_ids = [(6, 0, [int(id) for id in intern_ids])] if intern_ids else [(6, 0, [])]
        except ValueError:
            intern_ids = [(6, 0, [])]

        request.env['company.employee'].sudo().create({
            'name': post.get('name'),
            'email': post.get('email'),
            'tech_stack': post.get('tech-stack'),
            'contact': post.get('contact'),
            'intern_name_ids': intern_ids,
        })

        return request.redirect('/employee/form/success')

    @http.route('/employee/form/success', type='http', auth="public", website=True)
    def form_success(self, **kwargs):
        """Success page after submission"""
        return request.render('codetrade_module.employee_form_success')
