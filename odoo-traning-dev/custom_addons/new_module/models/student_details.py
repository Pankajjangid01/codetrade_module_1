from odoo import models, fields,api
import logging

_logger = logging.getLogger(__name__)

class StudentDetails(models.Model):
    _name = "student.student"
    _description = "Student Details"

    phone = fields.Integer("Phone")
    name = fields.Char(string="Name")
    age = fields.Integer(string="Age")
    email = fields.Char(string="Email", unique=True)
    branch = fields.Selection([
        ('cse', 'Computer Science'),
        ('ece', 'Electronics and Communication'),
        ('mech', 'Mechanical Engineering'),
        ('civil', 'Civil Engineering'),
        ('it', 'Information Technology'),
    ], string="Branch")
    college_name = fields.Char(string="College Name")
    student_id = fields.Char(string="Student ID")
    active = fields.Boolean(string="Active", default=True)
    start_date = fields.Date(string="Date")
    course_name = fields.Char(string="Course Name")
    course_amount = fields.Float(string="Course amount")
    course_description = fields.Html(string="Course Description")
    course_professor_name = fields.Char(string="Professor Name")
    course_professor_contact = fields.Integer(string="Professor Contact")

    @api.model
    def create_record(self, name, age, email, student_id, college_name, branch):
        _logger.debug("All okay in debugging")
        return self.create({
            'name': name,
            'age': age,
            'email': email,
            'student_id': student_id,
            'college_name': college_name,
            'branch': branch,
        })


    @api.model
    def write_record(self,id,email,college_name):
        searched_record = self.search([('id', '=', id)])
        if searched_record:
            searched_record.write(dict(email=email,college_name=college_name))
            _logger.info("Searched Record Information %s",searched_record)
        else:
            _logger.error("No record found with given id %s",searched_record)

    @api.model
    def delete_record(self,id):
        delete_data = self.search([('id', '=', id)])
        if delete_data:
            delete_data.unlink()

