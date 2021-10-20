from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config['SECRET_KEY']= 'qwertyuioplkjhgfd123sa'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)

bcrypt =Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category='info' 

# admin = Admin(app)

from riders_pkg.models import User
# admin.add_view(ModelView(User, db.session))


from riders_pkg import routes