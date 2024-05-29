import unittest
from app import create_app, db
from app.models.admin import Admin
from app.models.student import Student
from app.models.course import Course
from app.models.grade import Grade

class TestAdminModel(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        #Test Admin
        self.admin = Admin(username = "admin", email = "admin@test.com")
        self.admin.set_password("adminpassword")
        db.session.add(self.admin)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_student(self):
        student = self.admin.register_student(
            username = "student",
            email = "student@test.com",
            first_name = "Gabriel",
            last_name = "Grillo",
            dni = "123456789",
            phone = "001122334455",
            address = "123 test st",
            password = "studentpassword"
        )
        self.assertIsNotNone(Student.query.filter_by(username = "student").first())
    
    def test_delete_student(self):
       student = self.admin.register_student(
            username = "student2",
            email = "student2@test.com",
            first_name = "Franco",
            last_name = "Gaviota",
            dni = "12345678",
            phone = "001122334455",
            address = "123 test st",
            password = "studentpassword"
        )
       deleted_student = self.admin.delete_student(student.id)
       self.assertIsNone(Student.query.filter_by(username = "student2").first())

    def test_assign_course_to_student(self):
        student = self.admin.register_student(
            username = "student3",
            email = "student3@test.com",
            first_name = "Jesus",
            last_name = "Lagarto",
            dni = "1234567",
            phone = "001122334455",
            address = "123 test st",
            password = "studentpassword"
        )
        
        course = Course(name = "Pasteleria")
        db.session.add(course)
        db.session.commit()

        self.admin.assign_course_to_student(student.id, course.id)
        self.assertIn(course, student.courses)

    def test_load_grades(self):
        student = self.admin.register_student(
            username = "student4",
            email = "student4@test.com",
            first_name = "Bautista",
            last_name = "Alpaca",
            dni = "123456",
            phone = "001122334455",
            address = "123 test st",
            password = "studentpassword"
        )
        
        course = Course(name = "Reposteria")
        db.session.add(course)
        db.session.commit()

        grade = self.admin.load_grade(student.id, course.id, 95)
        self.assertEqual(grade.grade, 95)

if __name__ == "__main__":
    unittest.main()