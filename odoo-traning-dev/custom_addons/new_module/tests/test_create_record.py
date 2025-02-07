from odoo.tests import TransactionCase

class TestCreateRecord(TransactionCase):

    def setUp(self):
        super(TestCreateRecord, self).setUp()

        student = self.env['student.student'].create({
            'name': 'Anuj',
            'age': 22,
            'email': 'anuj@example.com',
            'student_id': '12345',
            'college_name': 'XYZ College',
            'branch': 'cse',
        })

        self.student_details = student.create_record(
            name='Anuj',
            age=22,
            email='anuj@example.com',
            student_id='12345',
            college_name='XYZ College',
            branch='cse'
        )

    def test_create_record(self):
        self.assertEqual(self.student_details.name, 'Anuj')

    def test_create_record_2(self):
        self.assertNotEqual(self.student_details.age, 20)

    def test_create_record_3(self):
        self.assertIsNot(self.student_details.name, self.student_details.age)
