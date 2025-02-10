from odoo import models,fields,api,_
from odoo.exceptions import ValidationError
from datetime import datetime
import re


class HRData(models.Model):
    _name = "company.hr"
    _description = "Store the Data of the HRs of the company"

    name = fields.Char(string="HR Name")
    email = fields.Char(string="HR Email", required=True)
    contact = fields.Char(string="Contact No.")
    salary = fields.Integer(string="Salary")
    hr_post = fields.Selection([
        ('manager', 'HR Manager'),
        ('junior', 'Junior HR'),
        ('senior', 'Senior HR'),
    ])
    image = fields.Binary(string="Image")
    joining_date = fields.Date(string="Joining Date")
    address = fields.Text(string="Address")
    created_by = fields.Char(string="Created By")
    created_at = fields.Date(string="Created At")
    hr_office = fields.Char(string="Assigned Office")
    intern_ids_m2m = fields.Many2many('intern.register', 'intern_hr_rel', 'hr_id', 'intern_id', string="Interns")



    intern_ids = fields.One2many('intern.register', 'select_hr_id', string="Interns Under HR")

    _sql_constraints = [
        ('unique_email', 'UNIQUE(email)', 'The email must be unique for each HR!'),
    ]

    @api.constrains('contact')
    def _check_validations(self):
        """Function to validate the Contact number"""
        for record in self:
            if record.contact:
                if not re.match(r"^(0|\+91|91)?[6-9][0-9]{9}$", record.contact):
                    raise ValidationError("Contact number must start with [6,7,8,9] and must be exactly 10 numeric digits.")
            else:
                raise ValidationError("Contact number is required.")

    @api.model
    def create(self, vals):
        """Function to add user name and date"""
        vals['created_by'] = self.env.user.name
        vals['created_at'] = datetime.today()
        return super(HRData, self).create(vals)

    def action_open_hr_wizard(self):
        """Function to open the HR wizard"""
        return {
            'name': _('Register Office'),
            'type': 'ir.actions.act_window',
            'res_model': 'office.register',
            'view_mode': 'form',
            'view_id': self.env.ref('codetrade_module.register_hr_form').id,
            'target': 'new',
            'context': {'default_select_hr_id': self.id}
        }

    def action_open_intern_wizard(self):
        """Function to open the intern Wizard"""
        return {
            'name': _('Register Intern'),
            'type': 'ir.actions.act_window',
            'res_model': 'intern.register',
            'view_mode': 'form',
            'view_id': self.env.ref('codetrade_module.register_intern_form').id,
            'target': 'new',
            'context': {'default_select_hr_id': self.id}
        }

    def get_sorted_hr_list(self):
        """Function that sort the hr list who have interns"""
        hrs = self.search([])
        return hrs.sorted(key=lambda hr: len(hr.intern_ids_m2m), reverse=True)
    
    def get_hr_with_multiple_interns(self):
        """Function that sort the hr list who have interns more than 2"""
        hrs = self.search([])
        filtered_hrs = hrs.filtered(lambda hr: len(hr.intern_ids_m2m) > 2)
        return filtered_hrs