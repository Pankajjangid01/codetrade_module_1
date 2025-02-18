from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
import re

class EmployeeData(models.Model):
    _name = "company.employee"
    _description = "Store the Data of the Employee's of the company"

    name = fields.Char(string="Employee Name")
    contact = fields.Char(string="Contact No.")
    email = fields.Char(string="Employee Email", required=True)
    employee_id = fields.Integer(string="Employee ID")
    salary = fields.Integer(string="Salary")
    tech_stack = fields.Selection([
        ('odoo', 'Odoo Developer'),
        ('tester', 'Testing Developer'),
        ('python', 'Python Developer'),
        ('web', 'Web Developer'),
    ])
    image = fields.Binary(string="Image")
    joining_date = fields.Date(string="Joining Date")
    address = fields.Text(string="Address")
    created_by = fields.Char(string="Created By")
    created_at = fields.Date(string="Created At")
    intern_name_ids = fields.One2many("intern.register", "select_employee_id", string="Intern List")

    _sql_constraints = [
        ('unique_email', 'UNIQUE(email)', 'The email must be unique for each employee!'),
        ('unique_employee_id', 'UNIQUE(employee_id)', 'Employee ID must be unique!'),
    ]

    @api.constrains('contact')
    def _check_validations(self):
        """Function that Validate the Contact"""
        for record in self:
            if record.email and not re.match(r"[^@]+@[^@]+\.[^@]+", record.email):
                raise ValidationError("Invalid email format. Please enter a valid email address.")

            if record.contact:
                if not re.match(r"^(0|\+91|91)?[6-9][0-9]{9}$", record.contact):
                    raise ValidationError("Contact number must start with [6,7,8,9] and must be exactly 10 numeric digits.")
            else:
                raise ValidationError("Contact number is required.")

    @api.model
    def create(self, vals):
        """Function to add current user-name and date"""
        vals['created_by'] = self.env.user.name
        vals['created_at'] = datetime.today()
        return super(EmployeeData, self).create(vals)
