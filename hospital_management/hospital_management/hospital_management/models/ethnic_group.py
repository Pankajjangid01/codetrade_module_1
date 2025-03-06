from odoo import models,fields

class EthnicGroup(models.Model):

    _name = "ethnic.group"
    _description = "Creates the ethnic group for the patient"
    _rec_name = "ethnic_group"

    ethnic_group = fields.Char(string="Ethnic Group",required=True)
    code = fields.Char(string="Code",required=True)
    