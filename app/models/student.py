from app import db
from app.models.user import User

association_table = db.Table("association",
    db.Column("student_id", db.Integer, db.ForeignKey("student.id")),
    db.Column("course_id", db.Integer, db.ForeignKey("course.id"))
    )

class Student(User):
    __tablename__ = "student"
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key = True)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    dni = db.Column(db.String(20), nullable = False, unique = True)
    phone = db.Column(db.String(20), nullable = False)
    address = db.Column(db.String(100), nullable = False)

    __mapper_args__ = {
        "polymorphic_identity" : "student",
    }

    courses = db.relationship("Course", secondary = association_table, backref = "students")