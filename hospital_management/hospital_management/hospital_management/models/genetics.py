from odoo import models,fields,api

class Genetics(models.Model):

    _name = "genetics.genetics"
    _description = "store the genetics data"

    name = fields.Char(string="Name",required=True)
    official_long_name = fields.Char(string="Official Long Name")
    affected_chromosome = fields.Char(string="Affected Chromosome")
    dominance = fields.Char(string="Dominance")
    location = fields.Char(string="Location")
    information = fields.Char(string="Information")