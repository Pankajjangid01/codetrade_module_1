from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class TestAppointments(TransactionCase):
    
    def setUp(self):
        """Setup test environment"""
        super(TestAppointments, self).setUp()
        self.appointment_model = self.env['appointment.appointment']

        # Create test patient
        self.patient = self.env['patient.patient'].create({'name': 'Test Patient'})

        # Create a test appointment
        self.appointment = self.appointment_model.create({
            'patient_id': self.patient.id,
            'physician': 'Dr. Smith',
            'speciality': 'Cardiology',
            'appointment_date': datetime.now(),
            'appointment_end': datetime.now() + timedelta(hours=2),
            'patient_status': 'stable',
            'invoice_exempt': True,
            'appointment_status': 'pending',
            'validity_date': datetime.now().date(),
            'health_center': 'sms',
            'inpatient_registration': '12345',
            'urgency_level': 'urgent',
            'invoice_to_insaurance': False,
            'consulting_service': 'consulting',
        })

    def test_appointment_creation(self):
        """Test that appointment is created with a valid ID"""
        self.assertTrue(self.appointment)
        self.assertEqual(self.appointment.patient_id.name, 'Test Patient')
        self.assertTrue(self.appointment.appointment_id.startswith('New') == False)

    def test_compute_duration(self):
        """Test computation of appointment duration"""
        self.appointment.appointment_date = datetime.now()
        self.appointment.appointment_end = self.appointment.appointment_date + timedelta(hours=3)
        self.appointment._onchange_compute_duration()
        self.assertEqual(self.appointment.appointment_duration, 3)

    def test_compute_duration_with_no_end_date(self):
        """Test duration calculation when appointment_end is missing"""
        self.appointment.appointment_end = False
        self.appointment._onchange_compute_duration()
        self.assertEqual(self.appointment.appointment_duration, 0)

    def test_validate_appointment_end_date_valid(self):
        """Test that no validation error is raised for valid dates"""
        self.appointment.appointment_date = datetime.now()
        self.appointment.appointment_end = self.appointment.appointment_date + timedelta(hours=1)
        self.appointment.validate_appointment_end_date()  # Should pass without error

    def test_validate_appointment_end_date_invalid(self):
        """Test validation error for appointment_end before appointment_date"""
        self.appointment.appointment_date = datetime.now()
        self.appointment.appointment_end = self.appointment.appointment_date - timedelta(hours=1)
        with self.assertRaises(ValidationError):
            self.appointment.validate_appointment_end_date()

    def test_appointment_status_selection(self):
        """Test appointment status selection values"""
        self.appointment.appointment_status = 'completed'
        self.assertEqual(self.appointment.appointment_status, 'completed')

    def test_health_center_selection(self):
        """Test valid health center selection"""
        self.appointment.health_center = 'niims'
        self.assertEqual(self.appointment.health_center, 'niims')

    def test_action_download_appointment_report(self):
        """Test PDF report action"""
        action = self.appointment.action_download_appointment_report()
        self.assertTrue(action)
        self.assertEqual(action.get('type'), 'ir.actions.report')
    
    def test_invoice_exemption(self):
        """Test invoice exemption boolean"""
        self.appointment.invoice_exempt = True
        self.assertTrue(self.appointment.invoice_exempt)

    def test_invoice_to_insurance(self):
        """Test invoice to insurance boolean field"""
        self.appointment.invoice_to_insaurance = True
        self.assertTrue(self.appointment.invoice_to_insaurance)





from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class TestAppointment(TransactionCase):

    def setUp(self):
        super(TestAppointment, self).setUp()

        # Create a test patient (Assuming patient.patient model exists)
        self.test_patient = self.env['patient.patient'].create({
            'name': 'John Doe',
        })

    def test_create_appointment(self):
        # Create appointment
        appointment = self.env['appointment.appointment'].create({
            'patient_id': self.test_patient.id,
            'physician': 'Dr. Smith',
            'speciality': 'Cardiology',
            'appointment_date': datetime.now(),
            'appointment_end': datetime.now() + timedelta(hours=2),
            'patient_status': 'Outpatient',
            'invoice_exempt': True,
            'appointment_status': 'pending',
            'validity_date': datetime.now().date(),
            'health_center': 'sms',
            'inpatient_registration': 'IP123',
            'urgency_level': 'urgent',
            'invoice_to_insaurance': True,
            'consulting_service': 'clinical'
        })
        self.assertTrue(appointment.appointment_id)
        self.assertEqual(appointment.patient_id.name, 'John Doe')

    def test_compute_duration_onchange(self):
        appointment = self.env['appointment.appointment'].create({
            'appointment_date': datetime(2025, 3, 19, 10, 0, 0),
            'appointment_end': datetime(2025, 3, 19, 13, 0, 0),
            'patient_id': self.test_patient.id
        })
        appointment._onchange_compute_duration()
        self.assertEqual(appointment.appointment_duration, 3.0)

    def test_compute_duration_zero(self):
        appointment = self.env['appointment.appointment'].create({
            'appointment_date': datetime(2025, 3, 19, 10, 0, 0),
            'appointment_end': False,
            'patient_id': self.test_patient.id
        })
        appointment._onchange_compute_duration()
        self.assertEqual(appointment.appointment_duration, 0)

    def test_appointment_end_date_constraint_valid(self):
        # Should not raise validation error
        self.env['appointment.appointment'].create({
            'appointment_date': datetime(2025, 3, 19, 10, 0, 0),
            'appointment_end': datetime(2025, 3, 19, 11, 0, 0),
            'patient_id': self.test_patient.id
        })

    def test_appointment_end_date_constraint_invalid(self):
        with self.assertRaises(ValidationError):
            self.env['appointment.appointment'].create({
                'appointment_date': datetime(2025, 3, 19, 15, 0, 0),
                'appointment_end': datetime(2025, 3, 19, 12, 0, 0),
                'patient_id': self.test_patient.id
            })

    def test_invoice_id_compute_stub(self):
        appointment = self.env['appointment.appointment'].create({
            'patient_id': self.test_patient.id,
            'appointment_date': datetime.now(),
            'appointment_end': datetime.now() + timedelta(hours=1)
        })
        # Since `invoice_id` is a computed field with no logic, it should remain False
        self.assertFalse(appointment.invoice_id)

    def test_action_download_report(self):
        appointment = self.env['appointment.appointment'].create({
            'patient_id': self.test_patient.id,
            'appointment_date': datetime.now(),
            'appointment_end': datetime.now() + timedelta(hours=1)
        })
        action = appointment.action_download_appointment_report()
        self.assertIsInstance(action, dict)
        self.assertIn('type', action)
