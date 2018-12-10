from marksU import db, login_manager
from flask_login import UserMixin


#to load a user
@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))


#DATBASE
class User(db.Model, UserMixin):
	__tablename__ = 'User'
	id 			= db.Column(db.Integer, primary_key=True)
	user_type 	= db.Column(db.Integer, nullable=False) #user_type 0 for student and 1 for faculty
	password 	= db.Column(db.String(20), nullable=False)
	email 		= db.Column(db.String(150), unique=True, nullable=False)

	def get_id(self):
		return (self.id)

	def __repr__(self):
		return '<user %r>' % self.email


class Faculty(db.Model):
	__tablename__ = 'Faculty'
	id 				= db.Column(db.Integer, primary_key=True)
	name 			= db.Column(db.String(50), nullable=False)
	email 			= db.Column(db.String(150), unique=True, nullable=False)
	phone 			= db.Column(db.Integer, unique=True, nullable=True)
	address 		= db.Column(db.String(200), nullable=False)
	city 			= db.Column(db.String(20), nullable=False)
	pincode 		= db.Column(db.Integer, nullable=False)
	country 		= db.Column(db.String(10), nullable=False)
	department 		= db.Column(db.String(20), nullable=False)
	dateofbirth 	= db.Column(db.String(20), nullable=False)
	dateofjoining 	= db.Column(db.String(20), nullable=False)

	def __repr__(self):
		return '<%r>' % self.name

class Student(db.Model):
	__tablename__ = 'Student'
	id 				= db.Column(db.Integer, nullable=False, primary_key=True)
	name 			= db.Column(db.String(50), nullable=False)
	email 			= db.Column(db.String(150), unique=True, nullable=False)
	phone 			= db.Column(db.Integer, unique=True, nullable=True)
	address 		= db.Column(db.String(200), nullable=False)
	city 			= db.Column(db.String(20), nullable=False)
	course 			= db.Column(db.String(10), nullable=False)
	semester	 	= db.Column(db.Integer, nullable=False)
	batch 			= db.Column(db.String(10), nullable=False)
	pincode 		= db.Column(db.Integer, nullable=False)
	country 		= db.Column(db.String(10), nullable=False)
	department 		= db.Column(db.String(20), nullable=False)
	dateofbirth 	= db.Column(db.String(20), nullable=False)
	dateofjoining 	= db.Column(db.String(20), nullable=False)

	def __repr__(self):
		return '<%r>' % self.name

class Department(db.Model):
	__tablename__ = 'Department'
	id 		= db.Column(db.Integer, primary_key=True)
	name 	= db.Column(db.String(50), nullable=False)
	hod_id 	= db.Column(db.Integer, db.ForeignKey('Faculty.id'), unique=True)
	hod 	= db.relationship('Faculty', uselist=False, backref='hod')

	def __repr__(self):
		return '<%r>' % self.name

class Subjects(db.Model):
	__tablename__ = 'Subjects'
	id 						= db.Column(db.Integer, primary_key=True)
	name 					= db.Column(db.String(50), nullable=False)
	semester 				= db.Column(db.Integer, nullable=False)
	department_id 			= db.Column(db.Integer, db.ForeignKey("Department.id"))
	faculty_id 				= db.Column(db.Integer, db.ForeignKey("Faculty.id"))
	taught_by_department 	= db.relationship('Department')
	taught_by_faculty 		= db.relationship('Faculty')

	def __repr__(self):
		return '<%r>' % self.name

class Marks(db.Model):
	__tablename__ = 'Marks'
	id 			= db.Column(db.Integer, primary_key=True)
	marks 		= db.Column(db.Integer, nullable=True)
	semester 	= db.Column(db.Integer, nullable=False)
	student_id 	= db.Column(db.Integer, db.ForeignKey("Student.id"))
	sub_code 	= db.Column(db.String(50), db.ForeignKey("Subjects.id"))
	obtained_by = db.relationship('Student')
	obtained_in = db.relationship('Subjects')

	def __repr__(self):
		return '<%r>' % self.sub_code
