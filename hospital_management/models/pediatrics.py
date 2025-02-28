from odoo import models,fields,api

class Pediatrics(models.Model):

    _name = "pediatrics.pediatrics"
    _description = "Pediatrics model to store the patient pediatric symptomps"

    patient_id = fields.Many2one("patient.patient")
    health_professional = fields.Char(string="Health Professional")
    pediatrics_symptomps_date = fields.Datetime(string="Date")
    appointment_id = fields.Char(string="Appointment")
    pcs_total = fields.Integer(string="PCS Total")

    symptomps_complain = fields.Selection([('never','Never'),('sometimes','Sometimes'),('often','Often'),('daily','daily')],string="Complains of aches and pains")
    spend_more_time_alone = fields.Selection([('never','Never'),('sometimes','Sometimes'),('often','Often'),('daily','daily')],string="Spends more time alone")
    patient_tires_easily = fields.Selection([('never','Never'),('sometimes','Sometimes'),('often','Often'),('daily','daily')],string="Tires easily,has little energy")
    unable_to_sit_still = fields.Selection([('never','Never'),('sometimes','Sometimes'),('often','Often'),('daily','daily')],string="Fidgety, unable to sit still")
    has_trouble_with_teacher = fields.Selection([('never','Never'),('sometimes','Sometimes'),('often','Often'),('daily','daily')],string="Has trouble with teaher")
    less_inerested_in_school = fields.Boolean(string="Less interested in school")
    acts_as_driven_by_motor = fields.Selection([('never','Never'),('sometimes','Sometimes'),('often','Often'),('daily','daily')],string="Acts as if driven by a motor")
    daydreams_too_much = fields.Selection([('never','Never'),('sometimes','Sometimes'),('often','Often'),('daily','daily')],string="")

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        """Update the health proffessional field when a patient is selected"""
        for record in self:
            if record.patient_id:
                record.health_professional = record.patient_id.patient_primary_care_doctor
            else:
                record.health_professional = ""
            
            patient_appointment_id = self.env["appointment.appointment"].search([('patient_id','=',record.patient_id.id)])
            self.appointment_id = patient_appointment_id.appointment_id