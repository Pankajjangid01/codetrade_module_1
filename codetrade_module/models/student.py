from odoo import models, fields

class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'Student Record'

    name = fields.Char(string='Student Name',required=True)
    subject_ids = fields.One2many('school.subject', 'student_id', string='Subjects')

    def create_student_with_subjects(self):
        """Create a new record and link it"""
        student = self.env['school.student'].create({
            'name': 'Pankaj Kumar',
            'subject_ids': [
                fields.Command.create({'name': 'Math', 'marks': 90}),
                fields.Command.create({'name': 'Science', 'marks': 85}),
            ]
        })
        return student

    def update_subject_marks(self):
        """Update a record with it"""
        if self.subject_ids:
            subject = self.subject_ids[0]
            self.write({
                'subject_ids': [fields.Command.update(subject.id, {'marks': 99})]
            })

    def remove_subject(self):
        """Delete the linked record from database"""
        if self.subject_ids:
            subject = self.subject_ids[0]
            self.write({
                'subject_ids': [fields.Command.delete(subject.id)]
            })

    def unlink_subject_relation_only(self):
        """Unlink the record from the relation (keep record in DB)"""
        if self.subject_ids:
            subject = self.subject_ids[0]
            self.write({
                'subject_ids': [fields.Command.unlink(subject.id)]
            })

    def link_existing_subject(self):
        """Link existing record by ID"""
        existing_subject = self.env['school.subject'].create({
            'name': 'History',
            'marks': 80,
        })
        self.write({
            'subject_ids': [fields.Command.link(existing_subject.id)]
        })

    def replace_all_subjects(self):
        """Replace all with specific IDs"""
        subject1 = self.env['school.subject'].create({'name': 'English', 'marks': 75})
        subject2 = self.env['school.subject'].create({'name': 'Biology', 'marks': 88})
        self.write({
            'subject_ids': [fields.Command.set([subject1.id, subject2.id])]
        })
        
    def unlink_all_relation(self):
        """Unlink all records from the relation with the self"""
        if self.subject_ids:
            self.write({
                'subject_ids': [fields.Command.clear()]
            })

class SchoolSubject(models.Model):
    _name = 'school.subject'
    _description = 'Subjects'

    name = fields.Char(string='Subject Name')
    marks = fields.Integer(string='Marks')
    student_id = fields.Many2one('school.student', string='Student')
