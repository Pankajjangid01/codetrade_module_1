from odoo import models, fields, api

class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'Student Record'

    name = fields.Char(string='Student Name')
    subject_ids = fields.One2many('school.subject', 'student_id', string='Subjects')

    @api.model
    def create(self, vals):
        """Function to create new student with log"""
        print("Printing record data------", vals)
        return super(SchoolStudent, self).create(vals)

    def create_student_with_subjects(self):
        """
        (0, 0, values): Create a new record and link it
        """
        student = self.env['school.student'].create({
            'name': 'Pankaj Kumar',
            'subject_ids': [
                fields.Command.create({'name': 'Math', 'marks': 90}),
                fields.Command.create({'name': 'Science', 'marks': 85}),
            ]
        })
        return student

    def update_subject_marks(self):
        """
        (1, id, values): Update a record with id
        """
        if self.subject_ids:
            subject = self.subject_ids[0]
            self.write({
                'subject_ids': [fields.Command.update(subject.id, {'marks': 99})]
            })

    def remove_subject(self):
        """
        (2, id): Delete the linked record from database
        """
        if self.subject_ids:
            subject = self.subject_ids[0]
            self.write({
                'subject_ids': [fields.Command.delete(subject.id)]
            })

    def unlink_subject_relation_only(self):
        """
        (3, id): Unlink the record from the relation (keep record in DB)
        Works in many2many but also allowed in one2many
        """
        if self.subject_ids:
            subject = self.subject_ids[0]
            self.write({
                'subject_ids': [fields.Command.unlink(subject.id)]
            })

    def link_existing_subject(self):
        """
        (4, id): Link existing record by ID
        (Works in many2many mostly, shown here for concept)
        """
        existing_subject = self.env['school.subject'].create({
            'name': 'History',
            'marks': 80,
        })
        self.write({
            'subject_ids': [fields.Command.link(existing_subject.id)]
        })

    def replace_all_subjects(self):
        """
        (6, 0, [ids]): Replace all with specific IDs
        (Used mostly in many2many)
        """
        subject1 = self.env['school.subject'].create({'name': 'English', 'marks': 75})
        subject2 = self.env['school.subject'].create({'name': 'Biology', 'marks': 88})
        self.write({
            'subject_ids': [fields.Command.set([subject1.id, subject2.id])]
        })


class SchoolSubject(models.Model):
    _name = 'school.subject'
    _description = 'Subjects'

    name = fields.Char(string='Subject Name')
    marks = fields.Integer(string='Marks')
    student_id = fields.Many2one('school.student', string='Student')
