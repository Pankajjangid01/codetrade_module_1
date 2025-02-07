from odoo import models, fields, api
from datetime import datetime
import re
import logging
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class TeacherData(models.Model):
    _name = 'college.teacher'
    _description = 'College Management Module to manage Teachers'
    _rec_name = 'teacher_name'

    teacher_name = fields.Char(string="Teacher Name", required=True)
    teacher_age = fields.Integer(string="Age")
    teacher_contact = fields.Char(string="Contact No.")
    teacher_email = fields.Char(string="Email", required=True)
    teacher_course_name = fields.Char(string="Course Name")
    teacher_description = fields.Text(string="Description")
    teacher_image = fields.Binary(string="Teacher Image")
    teacher_department = fields.Selection([
        ('cse', 'Computer Science'),
        ('ece', 'Electronics and Communication'),
        ('mech', 'Mechanical Engineering'),
        ('civil', 'Civil Engineering'),
        ('it', 'Information Technology'),
    ], string="Department")
    course_price = fields.Float(string="Course Price")
    total_amount = fields.Float(string="Total amount", compute="_total_course_price", inverse="_inverse_total_price")
    selected_department = fields.Char(string="Teacher Department")
    created_by = fields.Char(string="Created By-")
    created_at = fields.Datetime(string="Created At-")
    class_students_ids = fields.One2many('college.student', 'student_class_teacher_id', string="Associated Students")

    @api.constrains('teacher_email', 'teacher_contact')
    def _check_validations(self):
        for record in self:
            if record.teacher_email and not re.match(r"[^@]+@[^@]+\.[^@]+", record.teacher_email):
                raise ValidationError("Invalid email format. Please enter a valid email address.")
            
            if record.student_contact:
                teacher_contact = str(record.teacher_contact)
                if not re.match(r"^(0|\+91|91)?[6-9][0-9]{9}$", teacher_contact):
                    raise ValidationError("Contact number must start with [7,8,9] and must be exactly 10 numeric digits.")
            else:
                raise ValidationError("Contact number is required.")

    @api.model
    def create(self, vals):
        if 'teacher_email' in vals and self.search([('teacher_email', '=', vals['teacher_email'])]):
            _logger.error("A teacher with this email already exists!")
            raise ValidationError("A teacher with this email already exists!")

        vals['created_by'] = self.env.user.name
        vals['created_at'] = datetime.today()
        return super(TeacherData, self).create(vals)

    @api.depends('course_price')
    def _total_course_price(self):
        for record in self:
            record.total_amount = record.course_price

    def _inverse_total_price(self):
        for record in self:
            record.course_price = record.total_amount

    @api.onchange('teacher_department')
    def _onchange_teacher_department(self):
        for record in self:
            record.selected_department = record.teacher_department
