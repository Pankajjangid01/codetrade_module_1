from odoo import models,fields

class StudentRegisterMessage(models.TransientModel):
    _name = "student.register"
    _description = "message that student is registered"

    student_id = fields.Many2one('college.student', string="Student")
    select_class_teacher_id = fields.Many2one('college.teacher', string="Teachers-")
    message = fields.Text(string="Message")
        
    def confirm(self):
        if self.student_id:
            self.student_id.write({
                'class_teacher_id': self.select_class_teacher_id.id,
                'teacher_message': self.message
            })
            return {'type': 'ir.actions.act_window_close'}

    @staticmethod    
    def cancel():
        return {'type': 'ir.actions.act_window_close'}
