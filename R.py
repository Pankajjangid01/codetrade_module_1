class Patient(models.Model):
    _name = 'hms.patient'
    
    name = fields.Char(string="Patient Name", required=True)
    age = fields.Char(string="Age")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    gov_code = fields.Char(string="Gov Code")
    gov_code_source_id = fields.Many2one('gov.code.source', string='Gov Code Source')
    appointment_ids = fields.One2many('hms.appointment', 'patient_id', string="Appointments")class PatientDetailsWizard(models.TransientModel):
    _name = 'patient.details.wizard'
    _description = 'Wizard to Display Patient Details'

    patient_id = fields.Many2one('hms.patient', string="Patient", required=True, readonly=True)
    age_of_patient = fields.Char(related='patient_id.age', string="Age", readonly=True)
    patient_gender = fields.Selection(related='patient_id.gender', string="Gender", readonly=True)
    assessment_line_ids = fields.One2many('hms.appointment', 'patient_id', string="Assessment Lines", readonly=True)<odoo>
    <data>
        <record id="patient_details_wizard_form" model="ir.ui.view">
            <field name="name">patient.details.wizard.form</field>
            <field name="model">patient.details.wizard</field>
            <field name="arch" type="xml">
                <form>
                    <sheet>
                        <group>
                            <field name="patient_id"/>
                            <field name="age_of_patient"/>
                            <field name="patient_gender"/>
                        </group>
                        <group>
                            <field name="assessment_line_ids" readonly="1">
                                <tree>
                                    <field name="treatment_id"/>
                                    <field name="appointment_date"/>
                                    <field name="doctor_id"/>
                                    <field name="state"/>
                                </tree>
                            </field>
                        </group>
                    </sheet>
                </form>
            </field>
        </record>
    </data>
</odoo>from odoo import models,fields,api
from odoo.exceptions import ValidationError

class PatientAssessment(models.TransientModel):
    
    _name = "patient.assessments"

    govt_code_source_id = fields.Many2one(
        'gov.code.source', string='Source ID')
    govt_code = fields.Char(string="Government Identity",size=14)
    
    @api.constrains("govt_code")
    def check_govt_code(self):
        """Method to validate the govt. code"""    
        # import pdb;pdb.set_trace()
        for record in self:
            if not record.govt_code.isdigit():
                raise ValidationError("Enter Valid Govt ID")

            if len(record.govt_code) < 10 or len(record.govt_code) > 14:
                raise ValidationError("Enter Valid Govt ID bwtween 10 to 14")
    
    def apply(self):
        import pdb;pdb.set_trace()
        patient = self.env['hms.patient'].search([('gov_code', '=', self.govt_code)])
        
        if patient:
            if patient.gov_code_source_id == self.govt_code_source_id:
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Patient Details Wizard',
                    'res_model': 'patient.details.wizard',
                    'view_mode': 'form',
                    'target': 'new',
                    'context': {'default_patient_id': patient.id}
                }
            else:
                raise ValidationError("Source Id and Govt. Code not matched")
        else:
            raise ValidationError("Enter Valid Data")

class PatientDetailsWizard(models.TransientModel):
    _name = 'patient.details.wizard'
    _description = 'Wizard to Display Patient Details'

    patient_id = fields.Many2one('hms.patient', string="Patient", required=True, readonly=True)
    age_of_patient = fields.Char(related='patient_id.age', string="Age", readonly=True)
    patient_gender = fields.Selection(related='patient_id.gender', string="Gender",readonly=True)
    assessment_line_ids = fields.One2many(related='patient_id.appointment_ids', string="Assessment Lines", readonly=True)

    <odoo>
    <data>
        <record id="patient_details_wizard_form" model="ir.ui.view">
            <field name="name">patient.details.wizard.form</field>
            <field name="model">patient.details.wizard</field>
            <field name="arch" type="xml">
                <form>
                    <sheet>
                        <group>
                            <field name="patient_id"/>
                            <field name="age_of_patient"/>
                            <field name="patient_gender"/>
                        </group>
                        <field name="assessment_line_ids">
                            <tree editable="bottom">
                                <field name="treatment_id"/>
                            </tree>
                        </field>
                    </sheet>
                </form>
            </field>
        </record>
    </data>
</odoo>
# hms.patient mai apne pass appointment_ids field hai jo one2many hai relate to model hms.appointment, abhi tak mene patient_id,age,gender nikala hai but mujhe abb uske appointments bhi lane hai or list ki form mai form k andar
