from odoo import models,fields

class CompanyInterns(models.TransientModel):
    _name = "intern.register"
    _description = "HR adds new Interns"
    _rec_name = "intern_name"

    select_employee_id = fields.Many2one('company.employee', string="Assign to Employee")
    select_hr_id = fields.Many2one('company.hr', string="HR Reference") 
    intern_name = fields.Char(string="Intern Name")
    intern_email = fields.Char(string="Intern Email")
    intern_id = fields.Integer(string="Intern ID")
    intern_tech_stack = fields.Selection([
        ('odoo', 'Odoo Developer'),
        ('tester', 'Testing Developer'),
        ('python', 'Python Developer'),
        ('web', 'Web Developer'),
    ])
    hr_ids = fields.Many2many('hr.data', 'intern_hr_rel', 'intern_id', 'hr_id', string="HRs")


    @staticmethod
    def confirm():
        return {'type': 'ir.actions.act_window_close'}

    @staticmethod
    def cancel():
        return {'type': 'ir.actions.act_window_close'}
