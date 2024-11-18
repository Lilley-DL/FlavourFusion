from flask import Flask,render_template,url_for,request,jsonify
from dotenv import load_dotenv
import csv , json, os
import psycopg2

app = Flask(__name__)

#database thingssssss
DATABASE_URL = os.environ.get('DATABASE_URL')

#should allow for development using a dev database
if app.debug:
    DATABASE_URL = os.environ.get('DEV_DATABASE_URL')


def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

#routes 


##for render to run 
if __name__ == "__main__":
    app.run()
    