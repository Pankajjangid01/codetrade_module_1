from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError


class CompanyInterns(models.TransientModel):

    _name = "intern.register"
    _description = "HR adds new Interns"
    _rec_name = "intern_name"
    _inherit = ['mail.thread','mail.activity.mixin']

    select_intern_id = fields.Many2one("intern.register", string="Intern Data")
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
    date_of_birth = fields.Date(string="Date of Birth(D.O.B)")

    
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
            
        return record
    

    @api.constrains('date_of_birth')
    def _check_birth_date_validation(self):
        for record in self:
            if record.date_of_birth > datetime.today().date():
                raise ValidationError("Date of birth can not be future date. Enter valid date of birth")

    def display_notification(self):
        """Function to display the notification after email is sent to the intern"""
        notification = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': ("Registered Successfully"),
                'type': 'success',
                'message': ("Registration email sent successfully"),
                'sticky': False,
            }
        }
        return notification

    @api.model
    def display_birthday_notification(self):
        """Function to display the notification to the intern on his birthday"""
        today_date = datetime.today().date()
        intern_birth_day = self.search([('date_of_birth','=',today_date)])

        template = self.env.ref('codetrade_module.birthday_email_template')
        if template:
            for intern in intern_birth_day:
                template.send_mail(intern.id,force_send=True)

    @api.model
    def send_intern_reminders(self):
        """Scheduled cron job to remind HR about interns"""
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