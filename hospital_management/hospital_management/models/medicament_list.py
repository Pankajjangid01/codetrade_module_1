from odoo import models,fields

class MedicamentList(models.Model):

    _name = 'medicament.list'
    _description = 'Model to store the details of medicines'

    name = fields.Char(string="Name",required=True)
    active_component = fields.Char(string="Active Component")
    category = fields.Selection([
        ('antibiotics','Anitibiotics'),
        ('cough-syrup','Cough Syrup')
    ])
    quantity_available = fields.Integer(string="Quantity Available")
    therapeutic_effect = fields.Char(string="Therapeutic Effect")
    pregnancy_warning = fields.Char(string="Pregnancy Warning")
    price = fields.Integer(string="Price")

