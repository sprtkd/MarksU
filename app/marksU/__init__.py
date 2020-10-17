from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView



#initialize the app
app = Flask(__name__)

#secret key protects against modifying the cookies
#a secret key is a randomly generated set of characters
#generated using python secrets library
app.config['SECRET_KEY'] = '04c3637ff41c86b66471df0157678dcb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#initialize database instance
db = SQLAlchemy(app)

#initialize bcrypt instance
bcrypt = Bcrypt(app)


#initialize login manager instance
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from marksU import routes
