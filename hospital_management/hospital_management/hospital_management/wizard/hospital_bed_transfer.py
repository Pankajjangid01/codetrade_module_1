"""
    hosppital bed transfer module to store the bed transfer history of patient nad transfer the patient
"""
from odoo import models, fields,exceptions

class HospitalBedTransferWizard(models.TransientModel):
    """Class to show the wizard for bed transfer"""
    
    _name = "hospital.bed.transfer.wizard"
    _description = "Hospital Bed Transfer Wizard"

    administration_id = fields.Many2one('administration.administration', string="Patient")
    from_bed = fields.Many2one('hospital.bed', string="Current Bed", required=True, readonly=True)
    to_bed = fields.Many2one('hospital.bed', string="New Bed", required=True)
    reason = fields.Text(string="Reason", required=True)

    def action_transfer_bed(self):
        """Validate and transfer the patient to a new bed."""
        if self.to_bed.is_allocated:
            raise exceptions.ValidationError("Selected bed is already occupied.")

        self.env['bed.transfer'].create({
            'administration_id': self.administration_id.id,
            'from_bed': self.from_bed.id,
            'to_bed': self.to_bed.id,
            'reason': self.reason,
        })

        self.from_bed.is_allocated = False
        self.to_bed.is_allocated = True

        self.administration_id.hospital_bed_num = self.to_bed.id
