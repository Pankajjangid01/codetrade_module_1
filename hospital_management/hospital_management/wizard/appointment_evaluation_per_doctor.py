from odoo import models,fields

class AppointmentEvaluation(models.TransientModel):

    _name = "appointment.evaluation"
    _description = "This model store the appointment evaluation data per doctor"

    name_of_physician = fields.Many2many('appointment.appointment',string="Name of Physician")
    speciality = fields.Char(string="Speciality")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")

    @staticmethod    
    def save():
        """This function close the wizard window"""
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'appointment.appointment',
            'view_mode': 'list',
            'target': 'current',
        }
        
    @staticmethod    
    def cancel():
        """This function close the wizard window"""
        return {'type': 'ir.actions.act_window_close'}
