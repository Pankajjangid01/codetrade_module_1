class Physician(models.Model):
    _name = "physician.physician"
    _description = "This model stores the Details of physician"
    _rec_name="physisican_name"

    physisican_name = fields.Many2one("health.center", string="Name", required=True)
    physisican_id = fields.Char(default=lambda self: (''), readonly=True, copy=False, string="ID")
    institution = fields.Many2one("health.center.buildings", string="Institution", required=True)
    speciality = fields.Char(string="Speciality")
    is_available = fields.Boolean(string="Available", default=True)  # <-@api.constrains('patient_id')
    def check_physician_availability(self):
        """Ensure appointment is created only if physician is available."""
        for record in self:
            if record.patient_id and record.patient_id.patient_primary_care_doctor_id:
                physician = record.patient_id.patient_primary_care_doctor_id
                if not physician.is_available:
                    raise ValidationError(f"Physician '{physician.physisican_name.name}' is currently not available for appointments.")patient_primary_care_doctor_id = fields.Many2one(
    "physician.physician", 
    string="Primary Care Doctor",
    domain=[('is_available', '=', True)]
)- NEW FIELD
