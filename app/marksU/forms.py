from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo


class StudentRegistrationForm(FlaskForm):
	name = StringField('Name', validators = [DataRequired(), Length(min=2)])
	phone = IntegerField('Phone', [validators.NumberRange(10)])
	email = StringField('Email', validators = [DataRequired(), Email()])
	current_semester = IntegerField('Current Semester', validators = [DataRequired()])
	address = StringField('Address', validators = [DataRequired()])
	city = StringField('City', validators = [DataRequired()])
	pincode = IntegerField('Pincode', [validators.NumberRange(6)])
	country = StringField('Country', validators = [DataRequired()])
	course = StringField('Course', validators = [DataRequired()])
	enrollid = IntegerField('Enroll Id', [validators.NumberRange(min=9)])
	department = StringField('Department', validators = [DataRequired()])
	dateofbirth = StringField('Date of Birth', validators = [DataRequired()])
	dateofjoining = StringField('Date of Joining', validators = [DataRequired()])
	password = PasswordField('Password', validators = [DataRequired()])
	confirm_password = PasswordField('Retype Password', validators = [DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

class FacultyRegistrationForm(FlaskForm):
	name = StringField('Name', validators = [DataRequired(), Length(min=2)])
	phone = IntegerField('Phone', [validators.NumberRange(10)])
	email = StringField('Email', validators = [DataRequired(), Email()])
	address = StringField('Address', validators = [DataRequired()])
	city = StringField('City', validators = [DataRequired()])
	pincode = IntegerField('Pincode', [validators.NumberRange(6)])
	country = StringField('Country', validators = [DataRequired()])
	faculty_id = IntegerField('Enroll Id', [validators.NumberRange(min=9)])
	department = StringField('Department', validators = [DataRequired()])
	dateofbirth = StringField('Date of Birth', validators = [DataRequired()])
	dateofjoining = StringField('Date of Joining', validators = [DataRequired()])
	password = PasswordField('Password', validators = [DataRequired()])
	confirm_password = PasswordField('Retype Password', validators = [DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

class coeLoginForm(FlaskForm):
	password = PasswordField('registerpassword', validators = [DataRequired()])
	submit = SubmitField('Login')

class LoginForm(FlaskForm):
	email = StringField('registeremail', validators = [DataRequired(), Email()])
	password = PasswordField('registerpassword', validators = [DataRequired()])
	#remember = BooleanField('Remember Me')
	submit = SubmitField('Login')
