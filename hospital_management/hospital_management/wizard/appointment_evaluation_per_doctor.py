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
from odoo import models, fields, api

class AppointmentEvaluation(models.TransientModel):
    _name = "appointment.evaluation"
    _description = "This model stores the appointment evaluation data per doctor"

    name_of_physician = fields.Many2many('appointment.appointment', string="Name of Physician")
    speciality = fields.Char(string="Speciality")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")

    def save(self):
        """Filters appointments based on the provided field values and opens the filtered list"""
        domain = []

        if self.name_of_physician:
            domain.append(('physician', 'in', self.name_of_physician.mapped('physician')))

        if self.speciality:
            domain.append(('speciality', '=', self.speciality))

        if self.start_date:
            domain.append(('appointment_date', '>=', self.start_date))

        if self.end_date:
            domain.append(('appointment_end', '<=', self.end_date))

        return {
            'type': 'ir.actions.act_window',
            'name': 'Filtered Appointments',
            'res_model': 'appointment.appointment',
            'view_mode': 'tree,form',
            'domain': domain,
            'target': 'current',
        }

    def cancel(self):
        """Closes the wizard window"""
        return {'type': 'ir.actions.act_window_close'}
