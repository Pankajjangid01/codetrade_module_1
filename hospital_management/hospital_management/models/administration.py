from odoo import fields, models, api,exceptions,_
from datetime import date
from odoo.exceptions import ValidationError

class Administration(models.Model):
    _name = "administration.administration"
    _description = "Administration model to keep the data of patient in hospital"
    _rec_name = "registration_code"

    registration_code = fields.Char(default=lambda self: _('New'), readonly=True)
    patient_id = fields.Many2one("patient.patient", string="Patient", required=True)
    hospital_bed_num = fields.Many2one("hospital.bed",string="Hospital Bed",required=True)
    hospitalization_date = fields.Datetime(string="Hospitalization Date")
    discharge_date = fields.Datetime(string="Expected Discharge Date")
    attending_physician = fields.Char(string="Attending Physician")
    operating_physician = fields.Char(string="Operating Physician")
    admission_type = fields.Char(string="Admission Type")
    illness_reason = fields.Char(string="Illness Reason")
    state = fields.Selection(selection=[
       ('draft', 'Free'),
       ('in_progress', 'Confirmed'),
       ('cancel', 'Cancelled'),
       ('ongoing', 'Hospitalized'),
       ('done', 'Done'),
    ], string='Status', readonly=True, copy=False,
    tracking=True, default='draft')
    transfer_history_ids = fields.One2many('bed.transfer', 'administration_id', string="Bed Transfer History")


    @api.model
    def create(self, vals):
        """Automatically generate a reference number for new Administration."""
        vals['registration_code'] = self.env['ir.sequence'].next_by_code('administration.administration')
        return super(Administration, self).create(vals)
    
    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        """Update the Attending Physician field when a patient is selected"""
        for record in self:
            if record.patient_id:
                record.attending_physician = record.patient_id.patient_primary_care_doctor
                record.operating_physician = record.patient_id.patient_primary_care_doctor
            else:
                record.attending_physician = ""

    @api.constrains('hospitalization_date')
    def check_hospitalization_date(self):
        """Method to calidate the patient hospitalization date"""
        today = date.today()
        if self.hospitalization_date > today:
            raise ValidationError("Please enter today's date or past date")

    def button_in_progress(self):
        """Used to change the state to in_progress"""
        self.write({
           'state': "in_progress"
        })

    def confirm_update(self):
        """Used to change the state to ongoing"""
        self.write({
           'state': "ongoing"
       })

    def completed(self):
        """Used to change the state to don"""
        self.write({
           'state': "done"
       })

    def button_in_draft(self):
        """Used to change the state draft"""
        self.write({
           'state': "draft"
       })
        
    
    def action_transfer_bed(self):
        """Open the Bed Transfer Wizard."""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Transfer Bed',
            'res_model': 'hospital.bed.transfer.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_patient_id': self.id, 'default_from_bed': self.hospital_bed_num.id},
        }

class HospitalBed(models.Model):
    _name = "hospital.bed"
    _description = "Patient Allocated Bed"
    _rec_name="bed_name"

    bed_name = fields.Char(string="Bed Number", required=True)
    is_allocated = fields.Boolean(string="Allocated", default=False)


class BedTransfer(models.Model):
    _name = "bed.transfer"
    _description = "Hospital Bed Transfer"

    administration_id = fields.Many2one('administration.administration', string="Patient", required=True, ondelete="cascade")
    date = fields.Datetime(string="Date", default=fields.Datetime.now, required=True)
    from_bed = fields.Many2one('hospital.bed', string="From Bed", required=True)
    to_bed = fields.Many2one('hospital.bed', string="To Bed", required=True)
    reason = fields.Text(string="Reason", required=True)

    @api.constrains('to_bed')
    def _check_bed_availability(self):
        """Check For the availability of the bed"""
        for record in self:
            if record.to_bed.is_allocated:
                raise exceptions.ValidationError(f"Bed {record.to_bed.name} is already allocated!")

    def action_transfer(self):
        """Transfer the patient to a new bed."""
        if self.to_bed.is_allocated:
            raise exceptions.ValidationError("Selected bed is already allocated.")

        self.from_bed.is_allocated = False
        self.to_bed.is_allocated = True

        self.administration_id.hospital_bed_num = self.to_bed.id
