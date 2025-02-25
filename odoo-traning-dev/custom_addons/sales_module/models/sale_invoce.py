from odoo import models,fields,modules
import base64

class SaleInvoice(models.Model):
    _inherit='sale.order'

    def _get_default_image(self):
        """sets the default image of the record"""
        image_path = modules.get_module_resource('sales_module', 'static/src/img', 'image.SS2M12.png')
        with open(image_path, 'rb') as img:
            image = base64.b64encode(img.read())
        return image
    
    def action_download_invoice(self):
        """Triggers the PDF report generation and download."""
        return self.env.ref('sales_module.action_report_sale_product').report_action(self)
    