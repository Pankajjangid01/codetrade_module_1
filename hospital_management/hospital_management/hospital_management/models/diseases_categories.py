from odoo import models,fields

class DiseasesCategory(models.Model):

    _name = "diseases.category"
    _description = "This model stores the categories of the diseases"

    name = fields.Char(string="Diseases Name",required=True)

class DiseasesStructure(models.Model):

    _name = "diseases.structure"
    _description = "This model stores the categories of the diseases"

    name = fields.Char(string="Diseases Name",required=True)