from odoo import models,fields

class CompanyOffice(models.TransientModel):
    _name = "office.register"
    _description = "Assign Office to the HR "

    select_hr_id = fields.Many2one('company.hr', string="HR list-")
    company_office = fields.Selection([
        ('Gujrat','Gujrat'),
        ('Jaipur','Jaipur'),
        ('Mumbai','Mumbai'),
    ])
        
    def confirm(self):
        if self.select_hr_id:
            self.select_hr_id.write({
                'hr_office': self.company_office
            })
            return {'type': 'ir.actions.act_window_close'}

    @staticmethod    
    def cancel(self):
        return {'type': 'ir.actions.act_window_close'}
