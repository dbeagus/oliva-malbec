import unittest
from app import create_app, db
from app.models.student import Student
from app.models.course import Course

class TestStudentModel(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        #Test Student
        self.student = Student(
            username = "student",
            email = "student@test.com",
            first_name = "Pepito",
            last_name = "Grillo",
            dni = "123456789",
            phone = "001122334455",
            address = "123 test st"
        )
        self.student.set_password("password")
        db.session.add(self.student)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_create_student(self):
        student = Student.query.filter_by(username = "student").first()
        self.assertIsNotNone(student)
        self.assertEqual(student.first_name, "Pepito")
        self.assertEqual(student.last_name, "Grillo")
        self.assertEqual(student.dni, "123456789")
        self.assertEqual(student.phone, "001122334455")
        self.assertEqual(student.address, "123 test st")

    def test_check_password(self):
        student = Student.query.filter_by(username = "student").first()
        self.assertTrue(student.check_password("password"))
        self.assertFalse(student.check_password("wrongpassword"))
    
    def test_student_courses_relationship(self):
        course = Course(name = "Reposteria")
        db.session.add(course)
        db.session.commit()

        student = Student.query.filter_by(username = "student").first()
        student.courses.append(course)
        db.session.commit()

        self.assertIn(course, student.courses)
        self.assertIn(student, course.students)

if __name__ == "__main__":
    unittest.main()