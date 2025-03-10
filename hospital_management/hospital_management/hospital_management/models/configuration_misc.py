from odoo import models,fields,api

class MedicamentsMisc(models.Model):

    _name = "medicament.misc"
    _description = 'Model to store the details of medicines'

    name = fields.Char(string="Name",required=True)
    active_component = fields.Char(string="Active Component")
    category_id = fields.Many2one("diseases.category",string="Category")
    quantity_available = fields.Integer(string="Quantity Available")
    therapeutic_effect = fields.Char(string="Therapeutic Effect")
    pregnancy_warning = fields.Boolean(string="Pregnancy Warning")
    price = fields.Integer(string="Price")


class MedicalSpeciality(models.Model):

    _name = "medical.speciality"
    _description = "specialities of doctor"
    _rec_name = "speciality_description"

    speciality_description = fields.Char(string="Description",required=True)
    code = fields.Char(default=lambda self: (''),readonly=True, copy=False)

    @api.model
    def create(self, vals):
        """Automatically generate a reference number for new speciality."""
        vals['code'] = self.env['ir.sequence'].next_by_code('medical.speciality')
        return super(MedicalSpeciality, self).create(vals)


class MedicamentUnits(models.Model):

    _name = "medicament.units"
    _description = "This model store the units of the medicine"
    _rec_name = "unit"

    unit = fields.Char(string="Unit",required=True)
    description = fields.Char(string="Description",store=True)

    @api.onchange('unit')
    def _onchange_unit(self):
        """This method set the description on changing unit"""
        if self.unit:
            self.description = self.unit

class Occupation(models.Model):

    _name = "occupation.occupation"
    _description = "Creates the Occupations"

    occupation = fields.Char(string="Occupation",required=True)
    code = fields.Char(string="Code",store = True)

    @api.onchange('occupation')
    def _onchange_unit(self):
        """This method set the code on changing occupation"""
        if self.occupation:
            self.code = self.occupation