from flask import Flask,render_template,url_for,request,jsonify

from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,SubmitField,PasswordField
from wtforms.validators import DataRequired,Email

from dotenv import load_dotenv
import csv , json, os
import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('CSRF_SECRET_KEY')

#
class SignupForm(FlaskForm):
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

#signup route 
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

    if request.method == 'GET':
        return render_template("signup.html",username=username,email=email,password=password,form=form)



##for render to run 
if __name__ == "__main__":
    app.run()
    