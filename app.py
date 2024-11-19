from flask import Flask,render_template,url_for,request,jsonify,redirect

from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,SubmitField,PasswordField
from wtforms.validators import DataRequired,Email
import flask_login
from dotenv import load_dotenv
import csv , json, os, hashlib

from Database import get_db_connection,Database


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('CSRF_SECRET_KEY')

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


#database thingssssss
#should allow for development using a dev database
if app.debug:
    DATABASE_URL = os.environ.get('DEV_DATABASE_URL')
else:
    DATABASE_URL = os.environ.get('DATABASE_URL')

#database object instance 
db = Database(DATABASE_URL)




#
class SignupForm(FlaskForm):
    username = StringField('Username: ',validators=[DataRequired()])
    email = EmailField('Email: ',validators=[DataRequired()])
    password = PasswordField('Password: ',validators=[DataRequired()])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    username = StringField('Username: ',validators=[DataRequired()])
    email = EmailField('Email: ',validators=[Email()])
    password = PasswordField('Password: ',validators=[DataRequired()])
    submit = SubmitField("Submit")

##USER MANAGEMENT
class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(id):
    #conn = db.getConnection()
    # cur = conn.cursor()

    sql = "SELECT EXISTS(SELECT 1 FROM users WHERE user_id = %s)"
    values = (id,)
    result,rows = db.get(sql,values)
    user_exists = rows

    if user_exists[0] == 1:

        sql = "SELECT * FROM users WHERE user_id = ?"
        values = (id,)
        result,rows = db.get(sql,values)
        info = rows

        user = User()
        user.id = info['user_id']
        user.username = info['username']
        user.email = info['email']
        return user
    else:
        return None

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    # con = get_db()
    # cur = con.cursor()

    sql = "SELECT EXISTS(SELECT 1 FROM users WHERE email = %s)"
    values = (email,)
    result,rows = db.get(sql,values)
    user_exists = rows

    if user_exists[0] == 1:

        sql = "SELECT * FROM users WHERE email = ?"
        values = (email,)
        result,rows = db.get(sql,values)
        info = rows

        user = User()
        user.id = info['user_id']
        user.username = info['username']
        user.email = info['email']
        return user
    else:
        return None


#                               ROUTES 
@app.route("/")
def index():
    
    result,rows = db.get("SELECT * FROM  users")

    #testing 
    sql = "SELECT username,email FROM users WHERE user_id = %s"
    values = (6,)
    result,rows2 = db.get(sql,values)
    email = rows2[0]["email"]
    app.logger.info(f"ROWS {email}")

    #end of testing 

    return render_template("index.html",users=rows)

##signup route 

@app.route('/signup',methods=['GET','POST'])
def signup():
    #this is where a class would be useful lol 
    username = None
    email = None
    password = None

    form = SignupForm()

    if form.validate_on_submit():
        username = form.username.data
        form.username.data = ''

        email = form.email.data
        form.email.data = ''

        password = form.password.data # might need to hash it here
        form.password.data = ''

        #password salt
        salt = os.urandom(32)

        hashed = hashlib.pbkdf2_hmac('sha256',password.encode('utf-8'),salt,1000) #iterations was 100,000 but i chose 1000

        sql = "INSERT INTO users (username,email,hash,salt) VALUES (%s,%s,%s,%s)"
        # values = (username,email,hashed,salt,)
        values = (username,email,hashed,salt)

        result, message = db.insert(sql,values)

        if result:
            return redirect('/login')
        else:
            return redirect(url_for('signup',errors=f'{message}'))

    if request.method == 'GET':
        #look for error messag in the url 
        errors = request.args.get('errors')
        return render_template("signup.html",username=username,email=email,password=password,form=form,errors=errors)

##LOGIN

@app.route('/login',methods=['GET','POST'])
def login():
    username = None
    email = None
    password = None

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        form.username.data = ''

        email = form.email.data
        form.email.data = ''

        password = form.password.data # might need to hash it here
        form.password.data = ''




    return render_template("login.html",form=form)

##for render to run 
if __name__ == "__main__":
    app.run()
    