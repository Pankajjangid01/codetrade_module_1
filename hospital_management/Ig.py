from odoo import models, fields, api

class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'Student Record'

    name = fields.Char(string='Student Name')
    subject_ids = fields.One2many('school.subject', 'student_id', string='Subjects')

    @api.model
    def create(self, vals):
        """Function to create new student"""
        print("printing record data------",vals)
        return super(SchoolStudent, self).create(vals)

    # def create_student(self):
    #     student = self.env['school.student'].create({
    #         'name': 'Pankaj Kumar',
    #         'subject_ids': [
    #             (0, 0, {'name': 'Math', 'marks': 90}),
    #             (0, 0, {'name': 'Science', 'marks': 85}),
    #         ]
    #     })
    #     return student

    def update_student_data(self):
        self.update({
            'subject_ids': [(fields.Command.update(self.id, {'marks':55}))]
        })
    
    def delete_student_data(self):
        self.update({
            'subject_ids': [(fields.Command.delete(self.id)) ]
        })




class SchoolSubject(models.Model):
    _name = 'school.subject'
    _description = 'Subjects'

    name = fields.Char(string='Subject Name')
    marks = fields.Integer(string='Marks')
    student_id = fields.Many2one('school.student', string='Student')
