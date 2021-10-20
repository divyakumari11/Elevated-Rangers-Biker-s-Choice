from riders_pkg import db,app, login_manager
from flask_login import UserMixin    #used for login_user

@login_manager.user_loader          #used for login_user,takes id and returns user info
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(15), unique=True, nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    password=db.Column(db.String(60),nullable=False)
    cart = db.relationship('ordered', backref='user', lazy=True)
    
    # def __repr__(self):
    #     return f"user('{self.username}','{self.email}','{self.id}')"

class cycles(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    cname = db.Column(db.String(25),nullable=False)
    ccat = db.Column(db.String,nullable=False)
    cdes = db.Column(db.Text, nullable=False)
    cprice = db.Column(db.Float,nullable=False)
    img = db.Column(db.String(31),nullable=False)
    cart1 = db.relationship('ordered', backref='cart', lazy=True)
    
    
class ordered(db.Model, UserMixin):        #ordered.id, user.id, cycle.id
    id=db.Column(db.Integer,primary_key=True)
    user_id =db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cycle_id =db.Column(db.Integer, db.ForeignKey('cycles.id'), nullable=False)