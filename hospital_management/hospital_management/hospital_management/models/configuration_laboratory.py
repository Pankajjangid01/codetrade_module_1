from odoo import models, fields,api

class TestingUnits(models.Model):

    _name = "testing.units"
    _description = "This model store the lab testing units"
    _rec_name = "name"

    name = fields.Selection([
        ('gream','Grams(g)'),
        ('milligrams','Milligrams(mg)'),
        ('mililiters','Mililiters(ml)')
    ],string="Name",required=True)
    code = fields.Selection([
        ('gream','Grams(g)'),
        ('milligrams','Milligrams(mg)'),
        ('mililiters','Mililiters(ml)')
    ],string="Code")

class TestType(models.Model):

    _name = "test.type"
    _description = "this model store the test type details"

    code = fields.Many2one("lab.test.info",string="Code")
    name = fields.Char(string="name",readonly=True,required=True)

    @api.onchange('code')
    def set_test_name(self):
        """On change of code set the test type"""
        for record in self:
            if record.code:
                record.name = record.code.test_type
            else:
                record.name = ""