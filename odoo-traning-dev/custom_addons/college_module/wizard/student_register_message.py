from odoo import models,fields,_

class StudentRegisterMessage(models.TransientModel):
    _name = "student.register"
    _description = "message that student is registered"

    student_id = fields.Many2one('college.student', string="Student")
    select_class_teacher_id = fields.Many2one('college.teacher', string="Teachers-")
    message = fields.Text(string="Message")
        
    def confirm(self):
        """function to close the wizard after cinfirm button click"""
        if self.student_id:
            self.student_id.write({
                'class_teacher_id': self.select_class_teacher_id.id,
                'teacher_message': self.message
            })
            return {'type': 'ir.actions.act_window_close'}
    @staticmethod    
    def cancel():
        """function to close the wizard after cancel button click"""
        return {'type': 'ir.actions.act_window_close'}
