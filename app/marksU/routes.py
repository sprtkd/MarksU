from flask import render_template, url_for, flash, redirect, request
from marksU.models import Student, Faculty, User, Department, Subjects, Marks
from marksU import app, db, bcrypt, Admin, ModelView, AdminIndexView
import datetime
from marksU.forms import StudentRegistrationForm, FacultyRegistrationForm, LoginForm, coeLoginForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_admin.menu import MenuLink

COE_KEY = "coe123"
COE_LOGIN = False
COE_IP=None
STUDENT_USER_FLAG = 0

def coe_login_checker():
	curr_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
	if COE_LOGIN==True and COE_IP==curr_ip:
		return True
	else:
		return False

@app.route("/")
@app.route("/home")
@app.route("/index.html")
def home():
	return render_template("index.html", is_coe_loggedIn=coe_login_checker())


@app.route("/upload.html")
def uploadExample():
	return render_template("upload.html")

@app.route("/upload", methods=['GET', 'POST'])
def uploadProcessor():
	try:
		file = request.files['inputFile']
		flash(str(file.filename), 'success')
	except:
		flash(f'No Proper File Selected', 'danger')
	return redirect(url_for('home'))

@app.route("/login.html", methods=['GET', 'POST'])
def login():
	if coe_login_checker() or current_user.is_active:
		flash(f'Logout First to Login', 'danger')
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=True)
			flash(f'Login Successful!', 'success')
			return redirect(url_for('home'))
		else:
			flash(f'invalid credentials', 'danger')
	return render_template("login.html", form=form)


@app.route("/choose_registration.html")
def register():
	if current_user.is_active:
		flash(f'Logout First to register', 'danger')
		return redirect(url_for('home'))
	return render_template("choose_registration.html", is_coe_loggedIn=coe_login_checker())


@app.route("/faculty_registration.html", methods=['GET', 'POST'])
def faculty_registration():
	if current_user.is_active:
		flash(f'Logout First to register', 'danger')
		return redirect(url_for('home'))
	form = FacultyRegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		new_user = User(user_type=1, password=hashed_password, email=form.email.data)
		email_exists = User.query.filter_by(email=form.email.data).first()
		if email_exists:
			flash(f'Already Registered!', 'danger')
			return redirect(url_for('home'))
		else:
			new_faculty_user = Faculty(id=form.faculty_id.data, name=form.name.data, phone=form.phone.data, address=form.address.data,
									   city=form.city.data, pincode=form.pincode.data, country=form.country.data, department=form.department.data,
									   dateofbirth=form.dateofbirth.data, dateofjoining=form.dateofjoining.data, email=form.email.data)
			db.session.add(new_user)
			db.session.add(new_faculty_user)
			db.session.commit()
			flash(f'Registration Successful!', 'success')
			return redirect(url_for('login'))

	return render_template("faculty_registration.html", form=form, is_coe_loggedIn=coe_login_checker())


@app.route("/student_registration.html", methods=['GET', 'POST'])
def student_registration():
	if current_user.is_active:
		flash(f'Logout First to register', 'danger')
		return redirect(url_for('home'))
	form = StudentRegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		new_user = User(user_type=0, password=hashed_password, email=form.email.data)
		email_exists = User.query.filter_by(email=form.email.data).first()
		if email_exists:
			flash(f'Already Registered!', 'warning')
			return redirect(url_for('home'))
		else:
			now = datetime.datetime.now()
			batch = 'batch'+str(now.year)
			new_student_user = Student(id=form.enrollid.data, name=form.name.data, phone=form.phone.data, address=form.address.data,
									   city=form.city.data, pincode=form.pincode.data, country=form.country.data, course=form.course.data,
									   department=form.department.data, semester=form.current_semester.data, dateofbirth=form.dateofbirth.data,
									   dateofjoining=form.dateofjoining.data, batch=batch, email=form.email.data)
			db.session.add(new_user)
			db.session.add(new_student_user)
			db.session.commit()
			flash(f'Registration Successful!', 'success')
			return redirect(url_for('login'))
	return render_template("student_registration.html", form=form, is_coe_loggedIn=coe_login_checker())


@app.route("/coe_login.html", methods=['GET','POST'])
def coe_login():
	global COE_LOGIN, COE_IP
	if coe_login_checker() or current_user.is_active:
		flash(f'Logout First to Login', 'danger')
		return redirect(url_for('home'))
	form = coeLoginForm()
	if form.validate_on_submit():
		if form.password.data == COE_KEY:
			## there should be a route for coe profile
			if COE_LOGIN==True:
				flash(f'You were logged out as Admin from previous computer!', 'warning')
			COE_LOGIN = True
			COE_IP = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
			flash(f'Successfully Logged in as Admin!', 'success')
			return redirect(url_for('coe_profile'))
		else:
			flash(f'Invalid password!', 'danger')
			return redirect(url_for('coe_login'))
	return render_template('coe_login.html', form=form)


@app.route("/profile_coe.html")
def coe_profile():
	if coe_login_checker()==False:
		flash(f'You are not Logged in as Admin!', 'danger')
		return redirect(url_for('coe_login'))
	return render_template('profile_coe.html')


@app.route("/logout")
#@login_required
def logout():
	global COE_LOGIN
	if COE_LOGIN==True:
		COE_LOGIN=False
	else:
		logout_user()
	flash(f'Log out Successful!', 'success')
	return redirect(url_for('home'))


@app.route("/profile_redirect")
def redirect_to_profile():
	if coe_login_checker()==True:
		return render_template('profile_coe.html')
	elif current_user.is_active:
		if current_user.user_type==STUDENT_USER_FLAG:
			return redirect(url_for('student_profile'))
		else:
			return redirect(url_for('faculty_profile'))
	else:
		flash(f'You are Not Logged In', 'danger')
		return redirect(url_for('home'))



@app.route("/profile_student.html")
def student_profile():
	if current_user.is_active and current_user.user_type==STUDENT_USER_FLAG:
		user = Student.query.filter_by(email=current_user.email).first()
		return render_template('profile_student.html', user=user)
	else:
		flash(f'You are Not Logged In as Student', 'danger')
		return redirect(url_for('home'))


@app.route("/profile_faculty.html")
def faculty_profile():
	if current_user.is_active and current_user.user_type!=STUDENT_USER_FLAG:
		user = Faculty.query.filter_by(email=current_user.email).first()
		return render_template('profile_faculty.html', user=user)
	else:
		flash(f'You are Not Logged In as Faculty', 'danger')
		return redirect(url_for('home'))


################################################################################################################
'''
	Admin section
'''


#initialize admin instance
class AdminHomeView(AdminIndexView):
	def is_accessible(self):
		return coe_login_checker()
	def inaccessible_callback(self,name,**kwargs):
		flash(f'You are Not Logged In as Admin', 'danger')
		return redirect(url_for('home'))

admin = Admin(app, name='Admin Panel',index_view =AdminHomeView(),template_mode='bootstrap3' )
admin.add_link(MenuLink(name='Back to Admin Dashboard', category='', url='/profile_coe.html'))

class AdminDepartmentView(ModelView):
	column_display_pk = True
	def is_accessible(self):
		return coe_login_checker()

class AdminMarksView(ModelView):
	column_display_pk = True
	def is_accessible(self):
		return coe_login_checker()


class AdminSubjectsView(ModelView):
	column_display_pk = True
	def is_accessible(self):
		return coe_login_checker()


admin.add_view(AdminDepartmentView(Department, db.session))
admin.add_view(AdminSubjectsView(Subjects, db.session))
admin.add_view(AdminMarksView(Marks, db.session))
################################################################################################################
