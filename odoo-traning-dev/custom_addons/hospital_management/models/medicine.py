from odoo import models,fields

class Medicines(models.Model):

    _name="medicine.medicine"
    _description = "Medicine model to manage the medicine of the patient"

    print_medicine = fields.Boolean(string="Print")
    medicine_name = fields.Selection([
        ('aspirin','Aspirine'),
        ('Canine','Adequan Canine')
    ],string="Medicament")
    indication = fields.Char(string="Indication")
    medicine_dose = fields.Float(string="Dose")
    medicine_dose_unit = fields.Selection([
        ('mg','mg'),
        ('gm','gm')
    ])
    medicine_from = fields.Char(string="From")
    medince_frequency = fields.Integer(string="Frequency")
    medicine_quantity = fields.Integer(string="Quantity")
    treatment_duration = fields.Integer(string="Treatment Duration")
    treatment_period = fields.Selection([
        'days','Days',
        'week','Weeks',
        'month','Months'
    ],string="Treatment Duration")
    comment = fields.Char("Comment")
    allow_substituion = fields.Boolean("Allow Substitution")

    

    
