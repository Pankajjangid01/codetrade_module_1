from datetime import date
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re;


class Patient(models.Model):
    """Patient Class to handle the patient data"""
    _name = "patient.patient"
    _description = "Patient model to handle the patient data"

    name = fields.Char("Name",required=True)
    patient_name = fields.Char()
    patient_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string="Gender")
    patient_date_of_birth = fields.Date(string="Date of Birth")
    patient_maritial_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married')
    ])
    patient_address = fields.Char(string="Address")
    patient_image = fields.Binary(string="Image")
    patient_age = fields.Char(string="Age",readonly=True)
    blood_type = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('O', 'O'),
        ('AB', 'AB'),
    ], string="Blood Type")
    patient_rh = fields.Selection([
        ('+', '+'),
        ('-', '-')
    ], string="Rh")
    ethnic_group = fields.Selection([
        ('Asian', 'Asian'),
        ('African', 'African'),
        ('White', 'White')
    ], string="Ethnic Group")
    insurance = fields.Selection([
        ('General Insurance', 'General Insurance Company'),
        ('Life Insurance', 'Life Insurance')
    ], string="Insurance")

    family = fields.Char(string="Family")
    patient_receivable = fields.Float(string="Receivable")
    patient_primary_care_doctor = fields.Char(string="Primary Care Doctor")
    patient_deceased = fields.Boolean(string="Deceased")

    @api.constrains('name')
    def check_patient_name(self):
        """Method to validate the name of the patient"""
        if self.name and re.findall(r"[^a-zA-z][a-zA-z ]*", self.name):
            raise ValidationError("Please enter a valid name.")

    @api.onchange('patient_date_of_birth')
    def _onchange_compute_patient_age(self):
        """Compute patient age in years, months, and days."""
        for record in self:
            if record.patient_date_of_birth:
                today = date.today()
                dob = record.patient_date_of_birth

                years = today.year - dob.year
                months = today.month - dob.month
                days = today.day - dob.day

                if days < 0:
                    months -= 1
                    days += (date(today.year, today.month, 1) - date(today.year, today.month - 1, 1)).days

                if months < 0:
                    years -= 1
                    months += 12

                record.patient_age = f"{years} years, {months} months, {days} days"
            else:
                record.patient_age = "N/A"

    def action_download_patient_data(self):
        """Triggers the PDF report generation and download."""
        return self.env.ref('hospital_management.action_report_patient_data').report_action(self)
