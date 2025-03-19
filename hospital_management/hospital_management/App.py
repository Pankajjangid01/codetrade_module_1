from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class TestAppointmentModel(TransactionCase):

    def setUp(self):
        super(TestAppointmentModel, self).setUp()
        self.patient = self.env['patient.patient'].create({
            'name': 'Test Patient',
            # Add any required fields of patient model here
        })

    def test_create_appointment(self):
        """Test basic creation of appointment and auto generation of appointment_id"""
        appointment = self.env['appointment.appointment'].create({
            'patient_id': self.patient.id,
            'physician': 'Dr. John',
            'speciality': 'Cardiology',
            'appointment_date': datetime.now(),
            'appointment_end': datetime.now() + timedelta(hours=2),
        })
        self.assertTrue(appointment.appointment_id.startswith("APT") or appointment.appointment_id != 'New')
        self.assertEqual(appointment.patient_id.id, self.patient.id)

    def test_duration_computation(self):
        """Test computation of appointment duration"""
        start = datetime.now()
        end = start + timedelta(hours=3)
        appointment = self.env['appointment.appointment'].create({
            'patient_id': self.patient.id,
            'appointment_date': start,
            'appointment_end': end,
        })
        appointment._onchange_compute_duration()
        self.assertEqual(appointment.appointment_duration, 3.0)

    def test_invalid_end_date(self):
        """Test constraint: appointment_end should not be before appointment_date"""
        with self.assertRaises(ValidationError):
            self.env['appointment.appointment'].create({
                'patient_id': self.patient.id,
                'physician': 'Dr. John',
                'speciality': 'ENT',
                'appointment_date': datetime.now(),
                'appointment_end': datetime.now() - timedelta(hours=1),
            })

    def test_invalid_physician_name(self):
        """Test constraint: invalid physician name format"""
        with self.assertRaises(ValidationError):
            self.env['appointment.appointment'].create({
                'patient_id': self.patient.id,
                'physician': '1234Dr. John',
                'speciality': 'Cardiology',
                'appointment_date': datetime.now(),
                'appointment_end': datetime.now() + timedelta(hours=1),
            })

    def test_invalid_speciality(self):
        """Test constraint: invalid speciality format"""
        with self.assertRaises(ValidationError):
            self.env['appointment.appointment'].create({
                'patient_id': self.patient.id,
                'physician': 'Dr. John',
                'speciality': '123Cardio',
                'appointment_date': datetime.now(),
                'appointment_end': datetime.now() + timedelta(hours=1),
            })

    def test_action_open_invoice_wizard(self):
        """Test that action_open_invoice_wizard returns a proper action dict"""
        appointment = self.env['appointment.appointment'].create({
            'patient_id': self.patient.id,
            'appointment_date': datetime.now(),
            'appointment_end': datetime.now() + timedelta(hours=1),
        })
        action = appointment.action_open_invoice_wizard()
        self.assertEqual(action['type'], 'ir.actions.act_window')
        self.assertEqual(action['res_model'], 'invoice.confirmation.wizard')
        self.assertEqual(action['context']['default_appointment_id'], appointment.id)
