from app import db

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable = False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable = False)
    grade = db.Column(db.Integer, nullable = False)