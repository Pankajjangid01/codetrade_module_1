from odoo import models,fields

class Prescription(models.Model):

    _name="prescription.prescription"
    _description = "Prescription model to manage the prescription of the patient"

    patient_id = fields.Many2one("patient.patient",string="Patient")
    prescription_date = fields.Datetime(string="Prescription Date")
    pharmacy = fields.Many2one("appointment.appointment",string="Pharmacy")
    prescription_id = fields.Char(string="Prescription Id",compute="_compute_prescription_id")
    login_user = fields.Char(string="Login User",compute="_compute_login_user")
    prescribing_doctor = fields.Many2one("patient.patient",string="Prescribing Doctor")
    invoice_to_insurance = fields.Boolean(string="Invoice to Insurance")
    prescription_details = fields.Many2many("medicine.medicine")

    def _compute_prescription_id(self):
        """Function to compute Prescription ID"""
        for record in self:
            if record.id:
                record.prescription_id = f"PRES2017/{record.id}"

    def _compute_login_user(self):
        """Function to compute Prescription ID"""
        self.login_user = self.env.user.name
