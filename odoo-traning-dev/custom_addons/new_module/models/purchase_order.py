from odoo import models,fields

class PurchaseOrder(models.Model):
    
    _inherit = "purchase.order"

    vendor_address = fields.Char(string="Vendor Address")