from odoo import models, fields, api,_
from datetime import datetime

class CompanyInterns(models.TransientModel):
    _name = "intern.register"
    _description = "HR adds new Interns"
    _rec_name = "intern_name"

    select_intern_id = fields.Many2one("company.intern", string="Inter Data")
    select_employee_id = fields.Many2one('company.employee', string="Assign to Employee")
    select_hr_id = fields.Many2one('company.hr', string="HR Reference") 
    intern_name = fields.Char(string="Intern Name")
    intern_email = fields.Char(string="Intern Email", required=True)
    intern_id = fields.Integer(string="Intern ID")
    intern_tech_stack = fields.Selection([
        ('odoo', 'Odoo Developer'),
        ('tester', 'Testing Developer'),
        ('python', 'Python Developer'),
        ('web', 'Web Developer'),
    ])
    hr_ids = fields.Many2many('company.hr', 'intern_hr_rel', 'intern_id', 'hr_id', string="HRs")
    created_by = fields.Char(string="Created By")
    created_at = fields.Date(string="Created At")

    _sql_constraints = [
        ('unique_email', 'UNIQUE(intern_email)', 'The email must be unique for each Intern!'),
    ]

    def confirm(self):
        """Confirm and close wizard"""
        return {'type': 'ir.actions.act_window_close'}

    @api.model
    def create(self, vals):
        """Function to add user name, date, and send email notification"""
        vals['created_by'] = self.env.user.name
        vals['created_at'] = datetime.today()

        record = super(CompanyInterns, self).create(vals)
        template = self.env.ref('codetrade_module.email_template_intern_registration')
        if template:
            template.send_mail(record.id,force_send = True)
        notification = {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _("Registered Successfully"),
                    'type': 'success',
                    'message': _("Registration email sent successfully"),
                    'sticky': True,
                    }
                }
        return record,notification


    @api.model
    def send_intern_reminders(self):
        """Scheduled cron job to remind HR about interns"""
        # import pdb;
        # pdb.set_trace()
        today = datetime.today().date()
        interns = self.search([('created_at', '<=', today)])

        template = self.env.ref('codetrade_module.email_template_hr_reminder')
        if template:
            for intern in interns:
                if intern.select_hr_id:
                    template.send_mail(intern.id, force_send=True)

    @staticmethod    
    def cancel():
        """This function close the wizard window"""
        return {'type': 'ir.actions.act_window_close'}