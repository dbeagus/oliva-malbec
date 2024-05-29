from app import db
from app.models.user import User
from app.models.student import Student
from app.models.course import Course
from app.models.grade import Grade

class Admin(User):
    __tablename__ = "admin"
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key = True)

    __mapper_args__ = {
        "polymorphic_identity" : "admin",
    }

    def register_student(self, username, email, first_name, last_name, dni, phone, address, password):
        student = Student(
            username = username,
            email = email,
            first_name = first_name,
            last_name = last_name,
            dni = dni,
            phone = phone,
            address = address
        )
        student.set_password(password)
        db.session.add(student)
        db.session.commit()
        return student
    
    def delete_student(self, student_id):
        student = Student.query.get(student_id)
        if student:
            db.session.delete(student)
            db.session.commit()
        return student
    
    def assign_course_to_student(self, student_id, course_id):
        student = Student.query.get(student_id)
        course = Course.query.get(course_id)
        if student and course:
            student.courses.append(course)
            db.session.commit()
        return student, course
    
    def load_grade(self, student_id, course_id, grade):
        grade = Grade(student_id = student_id, course_id = course_id, grade = grade)
        db.session.add(grade)
        db.session.commit()
        return grade