from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import date, timedelta

class TestPatientModel(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Patient = self.env['patient.patient']
        self.physician = self.env['physician.physician'].create({'name': 'Dr. Smith'})
        self.disease = self.env['diseases.category'].create({'name': 'Fever'})

    def test_patient_name_valid(self):
        patient = self.Patient.create({
            'name': 'John Doe',
            'patient_gender': 'male',
            'patient_date_of_birth': '2000-01-01',
        })
        self.assertEqual(patient.name, 'John Doe')

    def test_patient_name_invalid(self):
        with self.assertRaises(ValidationError):
            self.Patient.create({
                'name': 'John123!',
                'patient_gender': 'male',
                'patient_date_of_birth': '2000-01-01',
            })

    def test_patient_age_computation(self):
        dob = date.today() - timedelta(days=365*25 + 30)  # Approx 25 years and 30 days ago
        patient = self.Patient.create({
            'name': 'Jane Smith',
            'patient_gender': 'female',
            'patient_date_of_birth': dob,
        })
        patient._onchange_compute_patient_age()
        self.assertIn('years', patient.patient_age)

    def test_patient_dob_in_future(self):
        future_dob = date.today() + timedelta(days=5)
        with self.assertRaises(ValidationError):
            self.Patient.create({
                'name': 'Future Patient',
                'patient_gender': 'male',
                'patient_date_of_birth': future_dob,
            })

    def test_action_show_patient_appointments(self):
        patient = self.Patient.create({
            'name': 'Alex',
            'patient_gender': 'male',
            'patient_date_of_birth': '1995-06-15',
        })
        action = patient.action_show_patient_appointments()
        self.assertEqual(action['res_model'], 'appointment.appointment')
        self.assertIn(('patient_id', '=', patient.id), action['domain'])

    def test_action_show_lab_results(self):
        patient = self.Patient.create({
            'name': 'Test Lab',
            'patient_gender': 'female',
            'patient_date_of_birth': '1990-05-10',
        })
        action = patient.action_show_patient_lab_result()
        self.assertEqual(action['res_model'], 'lab.test.info')
        self.assertIn(('patient_id', '=', patient.id), action['domain'])

    def test_action_show_prescriptions(self):
        patient = self.Patient.create({
            'name': 'Test Prescription',
            'patient_gender': 'female',
            'patient_date_of_birth': '1988-12-12',
        })
        action = patient.action_show_patient_prescription_orders()
        self.assertEqual(action['res_model'], 'prescription.prescription')
        self.assertIn(('patient_id', '=', patient.id), action['domain'])

    def test_action_show_pcs(self):
        patient = self.Patient.create({
            'name': 'Test PCS',
            'patient_gender': 'male',
            'patient_date_of_birth': '2002-09-09',
        })
        action = patient.action_show_patient_pcs_total()
        self.assertEqual(action['res_model'], 'pediatrics.pediatrics')
        self.assertIn(('patient_id', '=', patient.id), action['domain'])from datetime import date
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
