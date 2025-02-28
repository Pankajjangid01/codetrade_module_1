from odoo import models,fields,api
from odoo.exceptions import ValidationError
import re

class NewbornBaby(models.Model):

    _name = "newborn.baby"
    _description = "Class to store the details of newborn baby"

    new_born_baby_id = fields.Char(default=lambda self: ('New'), readonly=True)
    baby_image = fields.Binary()
    baby_name = fields.Char(string="Baby's name")
    baby_gender = fields.Selection([
        ('male','Male'),
        ('female','Female')
    ])
    discharged_date = fields.Datetime(string="Discharged Date")
    baby_weight = fields.Float(string="Weight")
    docter_in_charge = fields.Char(string="Docter in charge")
    mother_name = fields.Many2one("patient.patient",string="Father")
    date_of_birth = fields.Date(string="Date of Birth")
    baby_length = fields.Integer(string="Length")
    cephalic_perimeter = fields.Integer(string="Cephalic Perimeter")
    apgar_score_ids = fields.Many2many("apgar.score")

    def create(self, vals):
        """Automatically generate a reference number for new born baby."""
        vals['new_born_baby_id'] = self.env['ir.sequence'].next_by_code('newborn.baby')
        return super(NewbornBaby, self).create(vals)

    def action_download_newborn_data(self):
        """Triggers the PDF report generation and download."""
        return self.env.ref('hospital_management.action_report_patient_data').report_action(self)
    

    @api.constrains('name')
    def check_baby_name(self):
        import pdb;
        pdb.set_trace()
        if self.baby_name and re.findall(r"[^a-zA-z][a-zA-z ]*", self.baby_name):
            raise ValidationError("Please enter a valid name.")

class ApgarScore(models.Model):

    _name = "apgar.score"
    _description = "Class to store APGAR score"

    minutes = fields.Integer(string="Minutes")
    respiration = fields.Char(string="Respiration")
    activity = fields.Char(string="Activity")
    appearnace = fields.Char(string="Appearance")
    pulse = fields.Char(string="Pulse")
    apgar_score = fields.Integer(string="Apgar Score")
    grimance = fields.Char(string="Grimance")
