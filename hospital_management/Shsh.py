# models/student.py

from odoo import models, fields

class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'Student Record'

    name = fields.Char(string='Student Name')
    subject_ids = fields.One2many('school.subject', 'student_id', string='Subjects')

class SchoolSubject(models.Model):
    _name = 'school.subject'
    _description = 'Subjects'

    name = fields.Char(string='Subject Name')
    marks = fields.Integer(string='Marks')
    student_id = fields.Many2one('school.student', string='Student')


student = self.env['school.student'].create({
    'name': 'Pankaj Kumar',
    'subject_ids': [
        (0, 0, {'name': 'Math', 'marks': 90}),
        (0, 0, {'name': 'Science', 'marks': 85}),
    ]
})
