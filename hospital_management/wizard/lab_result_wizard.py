from odoo import models

class LabResult(models.TransientModel):
    
    _name = "lab.result"
    _description = "Create the lab test result"

    def confirm(self):
        """This function confirm and close the wizard window"""
        return {
                'name': ('Lab Test Result Info'),
                'type': 'ir.actions.act_window',
                'res_model': 'lab.test.info',
                'view_mode': 'list,form',
                }

    @staticmethod    
    def cancel():
        """This function close the wizard window"""
        return {'type': 'ir.actions.act_window_close'}
