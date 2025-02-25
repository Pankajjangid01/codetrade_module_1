from odoo import models,fields,modules

class SaleInvoice(models.Model):
    _inherit='sale.order'

    def display_notification(self):
        """Function to display the notification after email is sent to the"""
        template = self.env.ref('codetrade_module.email_template_sale_quotation')
        if template:
            template.send_mail(self.id,force_send = True)
        notification = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': ("Sale Qutation Created Successfully"),
                'type': 'success',
                'message': ("Email sent successfully"),
                'sticky': False,
            }
        }
        return notification