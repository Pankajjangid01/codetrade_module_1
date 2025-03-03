from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Appointments(models.Model):
    """Appointment Class to create the appointment dof the patient"""
    _name = "appointment.appointment"
    _description = "Appointment model to handle the patient appointments"
    _rec_name = "appointment_id"

    appointment_id = fields.Char(default=lambda self: ('New'), readonly=True, copy=False,)
    patient_id = fields.Many2one('patient.patient')
    physician = fields.Char(string="Physician")
    speciality = fields.Char(string="Speciality")
    appointment_date = fields.Datetime(string="Appointment Date")
    appointment_end = fields.Datetime(string="Appointment End")
    appointment_duration = fields.Float(string="Duration (Hours)")
    patient_status = fields.Selection([
        ('Outpatient','Outpatient'),
        ('critical','Critical'),
        ('stable','Stable'),
        ('good','Good')
    ], string="Patient Status")
    invoice_exempt = fields.Boolean(string="Invoice Exempt")
    appointment_status = fields.Selection([
        ('completed',"Invoiced"),
        ('pending','To be invoiced')
    ], string="Status")
    validity_date = fields.Date(string="Validity Date")
    health_center = fields.Selection([
        ('sms',"Swai Man Singh Hospital"),
        ('niims',"NIIMS"),
        ('shh',"Steve Hopkins Hospital")
    ], string="Health Center")
    inpatient_registration = fields.Char(string="Inpatient Registration")
    urgency_level = fields.Selection([
        ('urgent','Urgent'),
        ('good','Good')
    ], string="Urgency Level")
    invoice_to_insaurance = fields.Boolean(string="Invoice to Insurance")
    consulting_service = fields.Selection([
        ('consulting','Consulting'),
        ('clinical','Clinical Consulting'),
        ('operations','Operations Consulting')
    ], string="Consulting Service")
    invoice_id = fields.Char(compute="action_create_invoice")

    def create(self, vals):
        """Automatically generate a reference number for new Administration."""
        vals['appointment_id'] = self.env['ir.sequence'].next_by_code('appointment.appointment')
        return super(Appointments, self).create(vals)

    @api.onchange('appointment_date', 'appointment_end')
    def _onchange_compute_duration(self):
        """Compute appointment duration in hours"""
        for record in self:
            if record.appointment_date and record.appointment_end:
                datetime_difference = record.appointment_end - record.appointment_date
                record.appointment_duration = datetime_difference.total_seconds() / 3600
            else:
                record.appointment_duration = 0

    def action_download_appointment_report(self):
        """Triggers the PDF report generation and download."""
        return self.env.ref('hospital_management.action_report_appointment_data').report_action(self)
    
    @api.constrains('appointment_end')
    def validate_appointment_end_date(self):
        """"""
        if self.appointment_end < self.appointment_date:
            raise ValidationError("Appointment End Date can not be the date before Appointment Start Date")
