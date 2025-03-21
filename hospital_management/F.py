from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re
from datetime import date


class Patient(models.Model):
    _name = "patient.patient"
    _description = "Patient model to handle the patient data"
    _inherit = ['mail.thread']
    _order = 'name'

    name = fields.Char("Name", required=True)
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
    patient_age = fields.Char(string="Age", readonly=True)
    blood_type = fields.Selection([
        ('A', 'A'), ('B', 'B'), ('O', 'O'), ('AB', 'AB'),
    ], string="Blood Type")
    patient_rh = fields.Selection([
        ('+', '+'), ('-', '-')
    ], string="Rh")
    ethnic_group = fields.Selection([
        ('Asian', 'Asian'), ('African', 'African'), ('White', 'White')
    ], string="Ethnic Group")
    insurance = fields.Selection([
        ('General Insurance', 'General Insurance Company'),
        ('Life Insurance', 'Life Insurance')
    ], string="Insurance")

    family = fields.Char(string="Family")
    patient_receivable = fields.Float(string="Receivable")
    patient_primary_care_doctor = fields.Char(string="Primary Care Doctor")
    patient_deceased = fields.Boolean(string="Deceased")

    **company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, index=True, store=True, required=True)**

    # CONSTRAINTS
    @api.constrains('name')
    def check_patient_name(self):
        if self.name and re.findall(r"[^a-zA-Z\s]", self.name):
            raise ValidationError("Please enter a valid name.")

    # COMPUTE AGE
    @api.onchange('patient_date_of_birth')
    def _onchange_compute_patient_age(self):
        for record in self:
            if record.patient_date_of_birth:
                today = date.today()
                dob = record.patient_date_of_birth
                years = today.year - dob.year
                months = today.month - dob.month
                days = today.day - dob.day

                if days < 0:
                    months -= 1
                    days += 30
                if months < 0:
                    years -= 1
                    months += 12

                record.patient_age = f"{years} years, {months} months, {days} days"
            else:
                record.patient_age = "N/A"

    def action_download_patient_data(self):
        return self.env.ref('hospital_management.action_report_patient_data').report_action(self)⁹<record id="patient_multi_company_rule" model="ir.rule">
    <field name="name">Patient Multi-Company Access</field>
    <field name="model_id" ref="model_patient_patient"/>
    <field name="domain_force">[('company_id', '=', company_id)]</field>
    <field name="groups" eval="[(4, ref('base.group_user'))]"/>
</record>
