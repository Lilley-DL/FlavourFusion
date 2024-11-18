from flask import Flask,render_template,url_for,request,jsonify,redirect

from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,SubmitField,PasswordField
from wtforms.validators import DataRequired,Email

from dotenv import load_dotenv
import csv , json, os, hashlib
import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('CSRF_SECRET_KEY')

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





#database thingssssss
#should allow for development using a dev database
if app.debug:
    DATABASE_URL = os.environ.get('DEV_DATABASE_URL')
else:
    DATABASE_URL = os.environ.get('DATABASE_URL')


def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn



#routes 
@app.route("/")
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM  users")
    rows = cur.fetchall()
    cur.close()
    conn.close()
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

        #hash the password
        #hash the password 
        hashed = hashlib.sha256(password.encode())

        #get db connection 
        conn = get_db_connection()
        cur = conn.cursor()
        #check availability of username and email
        
        ##if available then try to entr them into the database
        try:
            sql = "INSERT INTO users (username,email,hash) VALUES (%s,%s,%s)"
            values = (username,email,hashed.hexdigest(),)
            cur.execute(sql,values)
            #close DB conection 
            conn.commit()
            cur.close()
            conn.close()
        except (Exception, psycopg2.Error) as error:
            app.logger.error("Error while inserting data",error)

        return redirect('/login')

    if request.method == 'GET':
        return render_template("signup.html",username=username,email=email,password=password,form=form)

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
    