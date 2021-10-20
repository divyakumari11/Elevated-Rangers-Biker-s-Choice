from flask import render_template,redirect,flash,url_for,request
from riders_pkg import app,bcrypt,db
from riders_pkg.forms import RegistrationForm,LoginForm,adminadd,UpdateAccountForm
from riders_pkg.models import User,cycles,ordered
from flask_login import login_user,current_user,logout_user,login_required #after validation we need to login the user so.
import secrets,os
from PIL import Image

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/account",methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Account details updated sucessfully","success")
        return redirect(url_for('account'))
    elif request.method == 'GET':                           #to display the details when loaded
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form_html=form)
    
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/layout")
def layout():
    form=LoginForm()
    return render_template('layout.html',form_html=form)

@app.route("/loggedin")
@login_required
def loggedin():
    return render_template('loggedin.html')


def save_picture(form_picture):
    random_hex = secrets.token_hex(8) #gives a token
    _, f_ext = os.path.splitext(form_picture.filename)  #fetch the pic name n split into 2
    picture_fn = random_hex + f_ext                        #new name
    picture_path = os.path.join(app.root_path, 'static/img', picture_fn)
    op_size = (500 , 500)
    img = Image.open(form_picture)
    img.thumbnail(op_size)
    img.save(picture_path)
    return picture_fn

@app.route("/admin",methods=['GET','POST'])
# @login_required
def admin():
    form=adminadd()    
    if form.validate_on_submit():
        print(form.img.data)
        pic=save_picture(form.img.data)
        current_user.img_file = pic
        current_user.cname = form.cname.data
        current_user.cdes = form.cdes.data
        current_user.cprice = form.cprice.data        
        card=cycles(cname=form.cname.data,ccat=form.ccat.data,cdes=form.cdes.data,cprice=form.cprice.data,img=pic)
        db.session.add(card)
        db.session.commit()
        flash("Product details updated sucessfully","success")
    return render_template('admin.html',title='Admin Login',form_html=form)
    

@app.route("/login", methods=['GET','POST'])
def login():
    url= request.args.get('user',type=str)
    print(url)
    form=LoginForm()
    
    if current_user.is_authenticated:
        return redirect(url_for('loggedin')) #if the user is logged in,all cards should be shown        
    
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if not user:
            flash('Login Credentials unavaliable,Please Register','warning')
            return render_template('login.html',title='LoG IN',form_html=form)
            
        if user.email =="admin@blog.com" and user.password =="$2b$12$Q8x0VxpEyZjBhq1FUCLak.wtilM6FFh8lWsvMNdXxGqTXaTvjWyHy":   #admin login
            # flash('ADMIN LOGGED IN!','success')
            return redirect(url_for('adminhome'))
        
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next') #the url has a paramenter,next
            print(next_page)
            # flash('You have loggedin successfuly!','success')
            return redirect(next_page) if next_page else redirect(url_for('loggedin')) #need to change
        else:
            flash('Login Unsuccessful,Please check email and password','warning')
    return render_template('login.html',title=url,form_html=form)  #layout.html to be changed


@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created!, Please Login to Continue', 'success')  
        return redirect(url_for('login'))
    return render_template('register.html', form_html=form)



@app.route("/mountainbike")
def mountainbike():
    id=None
    url= request.args.get('id',type=int)
    us=cycles.query.filter_by(ccat="Mountain Bike").all()
    id=cycles.query.filter_by(id=url).first()
    return render_template('mountainbike.html',cycle=us,title='Mountain Bikes',id=id)



@app.route("/roadbike")
def roadbike():
    id=None
    url= request.args.get('id',type=int)
    us=cycles.query.filter_by(ccat="Road Bike").all()
    id=cycles.query.filter_by(id=url).first()
    return render_template('roadbike.html',cycle=us,title='Road Bike',id=id)  

@app.route("/citybike")
def citybike():
    id=None
    url= request.args.get('id',type=int)
    us=cycles.query.filter_by(ccat="City Cycle").all()
    id=cycles.query.filter_by(id=url).first()
    return render_template('citybike.html',cycle=us,title='City Bikes',id=id)  

@app.route("/bmx")
def bmx():
    id=None
    url= request.args.get('id',type=int)
    us=cycles.query.filter_by(ccat="Bmx").all()
    id=cycles.query.filter_by(id=url).first()
    return render_template('bmx.html',cycle=us,title='Bmx',id=id) 


@app.route("/productdetail")
def productdetail():
    id=None
    url= request.args.get('id',type=int)
    id=cycles.query.filter_by(id=url).first()
    return render_template('productdetail.html',id=id)      
    
@app.route("/addtocart") 
@login_required
def addtocart():
    url= request.args.get('id',type=int)
    add=ordered(user_id=current_user.id,cycle_id=url)
    db.session.add(add)
    db.session.commit()
    id=ordered.query.filter_by(user_id=current_user.id).all()
    a=[]
    for i in id:
        a.append(cycles.query.filter_by(id=i.cycle_id).first())
    p=0
    for i in a:
        p=p+i.cprice
    return render_template('emptycart.html',current_cycle_id=id,existing_cycles=set(a),len=len(set(a)),price=p)     

@app.route("/cart")
def cart():
    id=ordered.query.filter_by(user_id=current_user.id).all()
    a=[]
    for i in id:
        a.append(cycles.query.filter_by(id=i.cycle_id).first())
    print(a)
    p=0
    for i in a:
        p=p+i.cprice
    print(p)  
    return render_template('emptycart.html',existing_cycles=set(a),length=len(a),price=p) 

    
    
@login_required
@app.route("/delete")
def delete():
    url= request.args.get('id',type=int)
    id=ordered.query.filter_by(cycle_id=url).first()
    db.session.delete(id)
    db.session.commit()
    flash("Your Cycle has been deleted","warning")
    return redirect(url_for('cart'))  

@login_required
@app.route("/admindelete")
def admindelete():
    url= request.args.get('id',type=int)
    id=cycles.query.filter_by(id=url).first()
    db.session.delete(id)
    db.session.commit()
    flash("Your Cycle has been deleted","warning")
    return redirect(url_for('adminproduct')) 


@app.route("/order")
def order():
    return render_template('order.html')  

@app.route("/adminlogin")
def adminlogin():
    return render_template('adminlogin.html')    


@app.route("/pro/<string:category>",methods=['GET','POST'])
def pro(category):
    cycle=cycles.query.filter_by(ccat=category).all()
    print(cycle)
    return render_template('category.html',cycles=cycle,category=category)

@app.route("/practice/<int:id>",methods=['GET','POST'])
def practice(id):
    cyc=cycles.query.get_or_404(id)
    return render_template('practice.html',cycle=cyc,id=id)        

@app.route("/adminproduct")
def adminproduct():
    cyc=cycles.query.filter_by().all()
    # print(cyc)
    # for i in cyc:
    #     print(type(i))
    return render_template('adminproduct.html',cycles=cyc,title="Admin Products")  


@app.route("/buynow")
def buynow():
    return render_template('ordered.html')  

@app.route("/adminhome")
def adminhome():
    # flash('ADMIN LOGGED IN!','success')
    return render_template('adminhome.html')  

@app.route("/orderrecord")
def orderrecord():
    orders=ordered.query.filter_by().all()
    for o in orders:
        print(o.user_id,o.cart.cdes)
    return render_template('orderrecord.html',title="Order Records",orders=orders) 


# @login_required
# @app.route("/adminedit",methods=['GET','POST'])
# def adminedit():
#     form = adminadd()
#     id= request.args.get('id',type=int)
#     if form.validate_on_submit():
#         cycle=cycles.query.get(id)
#         # z 
#         cycle.ccat=form.ccat.data 
#         cycle.cdes=form.cdes.data
#         cycle.cprice=form.cprice.data
#         db.session.commit()
#         flash("Account details updated sucessfully","success")
#         return redirect(url_for('account'))
#     elif request.method == 'GET':                           #to display the details when loaded
#         cycle=cycles.query.get(id)
#         print(cycle)
#         form.cname.data = cycle.cname
#         form.ccat.data = cycle.ccat
#         form.cdes.data=cycle.cdes
#         form.cprice.data=cycle.cprice
#         form.img.data=cycle.img
#     return render_template('admin.html', title='Edit Product', form_html=form)