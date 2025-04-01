from odoo import models, fields, api

class PatientIDWizard(models.TransientModel):
    _name = 'patient.id.wizard'
    _description = 'Wizard to Enter Government ID'

    govt_id = fields.Char(string="Government ID", required=True)

    def action_fetch_patient(self):
        patient = self.env['patient.details'].search([('govt_id', '=', self.govt_id)], limit=1)
        if patient:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Patient Details Wizard',
                'res_model': 'patient.details.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {'default_patient_id': patient.id}
            }
        else:
            return {'type': 'ir.actions.act_window_close'}


class PatientDetailsWizard(models.TransientModel):
    _name = 'patient.details.wizard'
    _description = 'Wizard to Display Patient Details'

    patient_id = fields.Many2one('patient.details', string="Patient", required=True, readonly=True)
    name = fields.Char(related='patient_id.name', string="Patient Name", readonly=True)
    age = fields.Integer(related='patient_id.age', string="Age", readonly=True)
    assessment_line_ids = fields.One2many('patient.assessment.line', 'patient_id', string="Assessment Lines", readonly=True)
