from odoo import models,fields,api
from odoo.exceptions import ValidationError

class PatientAssessment(models.TransientModel):
    
    _name = "patient.assessment"
    _inherit = "gov.code.source"

    gov_code_source_id = fields.Many2one(
        'gov.code.source', string='Source ID')
    govt_code = fields.Char(string="Government Identity",size=14)
    
    @api.constrains("govt_code")
    def check_govt_code(self):
        """Method to validate the govt. code"""
        for record in self:
            if not record.govt_code.isdigit():
                raise ValidationError("Enter Valid Govt ID")

            if len(record.govt_code) < 10 or len(record.govt_code) > 14:
                raise ValidationError("Enter Valid Govt ID bwtween 10 to 14")
    
    def apply(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Assessments',
            'res_model': 'assessments.assessments',
            'view_mode': 'list',
            'target': 'new',
            'context': {'default_govt_code':self.govt_code},
        }

class Assessmets(models.TransientModel):
    _name = "assessments.assessments"

    patient_name = fields.Char(string="Patient Name", readonly=True)
    patient_age = fields.Char(string="Age",readonly=True)
    patient_code = fields.Char(string="Code",readonly=True)
    patient_doctor = fields.Char(string="Doctor",readonly=True)

    @api.model
    def default_get(self, fields):
        import pdb;pdb.set_trace()
        res = super(Assessmets, self).default_get(fields)
# in my hms.appointment i have gov_id of patient so the gov_code i  sending in context on this basis i want get the pateint info and its appointment
