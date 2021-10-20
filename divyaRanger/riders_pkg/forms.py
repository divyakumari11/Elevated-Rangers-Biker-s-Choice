from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField ,BooleanField ,TextAreaField,FloatField,SelectField#to add stings datatype...
from wtforms.validators import DataRequired ,Length,Email,Regexp,EqualTo,ValidationError #to enable empty and validate length
from flask_login import current_user
from flask_wtf.file import FileField,FileAllowed #for image
from riders_pkg.models import User,cycles


class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=5,max=15),Regexp(r'^[^\s]+$',message='Spaces not allowed')]) #username is our variable
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=8), Regexp(r'^[^\s]+$')])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit= SubmitField('Sign me Up Now!') #submit button
    
    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("User name already present,Use a different one!")
        
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already present,Use a different one!")
    
class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=8), Regexp(r'^[^\s]+$')])
    remember = BooleanField('Remember me')
    submit= SubmitField('Let me In!')
    
class adminadd(FlaskForm):  #add cards
    cname = StringField('Enter Cycle Name',validators=[DataRequired()])
    ccat =  SelectField('Cycle Category',choices=[('',''),('Mountain', 'Mountain Bike'), ('Road', 'Road Bike'), ('City', 'City Cycle'), ('Bmx', 'Bmx') ], validators=[DataRequired()])
    cdes = StringField('Enter Cycle Description',validators=[DataRequired(),Length(max=25)])
    cprice = FloatField('Enter the Cycle price',validators=[DataRequired()])
    img = FileField('Upload Cycle Picture', validators=[FileAllowed(['jpg','png','jfif','jpeg'])])
    submit= SubmitField('Add Product!')
    
    def validate_cname(self,cname):
        cycle=cycles.query.filter_by(cname=cname.data).first()  #to be filled after creating admin table
        if cycle:
            raise ValidationError("User name already present,Use a different one!")
        
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=5,max=15),Regexp(r'^[^\s]+$',message='Spaces not allowed')]) #username is our variable
    email = StringField('Email',validators=[DataRequired(), Email()])
    submit= SubmitField('Update Info!') #submit button
    
    def validate_username(self,username):
        if username.data != current_user.username:
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("User name already present,Use a different one!")
        
    def validate_email(self,email):
        if email.data != current_user.email:
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Email already present,Use a different one!")
    
    