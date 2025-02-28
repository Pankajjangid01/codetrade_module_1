"""
    Prescription Module to create the prescription table to store the patient prescription details
"""
from odoo import models, fields

class Prescription(models.Model):
    """Prescription Class to handle the prescription of patient"""

    _name = "prescription.prescription"
    _description = "Prescription model to manage the prescription of the patient"
    _rec_name = "prescription_id"

    patient_id = fields.Many2one("patient.patient", string="Patient")
    prescription_date = fields.Datetime(string="Prescription Date")
    health_center = fields.Selection([
        ('sms',"Swai Man Singh Hospital"),
        ('niims',"NIIMS"),
        ('shh',"Steve Hopkins Hospital")
        ], string="Pharmacy")
    prescription_id = fields.Char(default=lambda self:self.env['ir.sequence'].next_by_code('prescription.prescription'),readonly=True, copy=False,string="Prescription Id")
    login_user = fields.Many2one("res.users",default=lambda self:self.env.user.name, string="Login User",)
    prescribing_doctor = fields.Char(string="Prescribing Doctor")
    invoice_to_insurance = fields.Boolean(string="Invoice to Insurance")
    prescription_details_ids = fields.Many2many("medicine.medicine")

    def prescription_report_download(self):
        """Triggers the PDF report generation and download."""
        return self.env.ref('hospital_management.action_report_prescription_data').report_action(self)

class Medicines(models.Model):
    """Class to sotre the medicine of the patient and their details"""

    _name="medicine.medicine"
    _description = "Medicine model to manage the medicine of the patient"

    print_medicine = fields.Boolean(string="Print")
    medicine_name = fields.Selection([
        ('aspirin','Aspirine'),
        ('Canine','Adequan Canine')
    ],string="Medicament")
    indication = fields.Char(string="Indication")
    medicine_dose = fields.Float(string="Dose")
    medicine_dose_unit = fields.Selection([
        ('mg','mg'),
        ('gm','gm')
    ])
    medicine_from = fields.Char(string="From")
    medince_frequency = fields.Integer(string="Frequency")
    medicine_quantity = fields.Integer(string="Quantity")
    treatment_duration = fields.Integer(string="Treatment Duration")
    treatment_period = fields.Selection([
        ('days','Days'),
        ('week','Weeks'),
        ('month','Months')
    ],string="Treatment Period")
    comment = fields.Char("Comment")
    allow_substituion = fields.Boolean("Allow Substitution")
