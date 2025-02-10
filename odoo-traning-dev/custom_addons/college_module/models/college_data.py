from odoo import models,fields,api,_
from datetime import datetime
import re
import logging
from odoo.exceptions import ValidationError,UserError

_logger = logging.getLogger(__name__)

class CollegeData(models.Model):
    _name = 'college.student'
    _description = 'College Management to manage Teachers and Students'
    _rec_name = "student_name"

    student_name = fields.Char(string="Student Name", required=True)
    student_roll_num = fields.Integer(string="Roll No.")
    student_dob = fields.Date(string="Date of Birth(D.O.B)")
    student_age = fields.Integer(string="Age")
    student_contact = fields.Char(string="Contact No.")
    student_email = fields.Char(string="Email", required=True)
    student_branch = fields.Selection([
        ('cse', 'Computer Science'),
        ('ece', 'Electronics and Communication'),
        ('mech', 'Mechanical Engineering'),
        ('civil', 'Civil Engineering'),
        ('it', 'Information Technology'),
    ], string="Branch")
    student_image = fields.Binary(string="Student Image")
    student_description = fields.Text(string="Student Description")
    created_by = fields.Char(string="Created By-")
    created_at = fields.Datetime(string="Created At-")
    isactive = fields.Boolean(string="Active", default=True)
    student_class_teacher_id = fields.Many2one('college.teacher','Class Teacher')
    student_teacher_ids = fields.Many2many('college.teacher','student_teacher_rel', string="List of Teachers")
    class_teacher_id = fields.Many2one('college.teacher', string="Messaged Teacher")
    teacher_message = fields.Text(string="Teacher's Message")


    @api.constrains('student_email', 'student_contact')
    def _check_validations(self):
        """This function validate the email and contact number"""
        for record in self:
            if record.student_email and not re.match(r"[^@]+@[^@]+\.[^@]+", record.student_email):
                raise ValidationError("Invalid email format. Please enter a valid email address.")
            
            if record.student_contact:
                student_contact = str(record.student_contact)
                if not re.match(r"^(0|\+91|91)?[6-9][0-9]{9}$", student_contact):
                    raise ValidationError("Contact number must start with [7,8,9] and must be exactly 10 numeric digits.")
            else:
                raise ValidationError("Contact number is required.")


    @api.model
    def create(self, vals):
        """This function check is the email already exist or not"""
        if 'student_email' in vals and self.search([('student_email', '=', vals['student_email'])]):
            _logger.error("A student with this email already exists!")
            raise ValidationError("A student with this email already exists!")
        vals['created_by'] = self.env.user.name
        vals['created_at'] = datetime.today()
        return super(CollegeData, self).create(vals)

    @api.ondelete(at_uninstall=False)
    def _unlink_if_not_done(self):
        """This function dont allow to delete if student is active"""
        if any(record.isactive is True for record in self):
            raise UserError(("Student is active, can't delete"))
        
    def action_open_wizard(self):
        """This function confirm and close the wizard window"""
        return {
            'name': _('Register Message'),
            'type': 'ir.actions.act_window',
            'res_model': 'student.register',
            'view_mode': 'form',
            'view_id': self.env.ref('college_module.register_student_form').id,
            'target': 'new',
            'context': {'default_student_id': self.id}
        }
