import flask
from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html') 


@app.route('/home')
def home():
    return render_template('index.html') 

@app.route('/newMeeting')
def newMeeting():
    return render_template('newMeeting.html') 



@app.route('/form_action', methods=['POST'])
def form_action():
	date = request.form.get('date')
	print(date);
	return flask.redirect(flask.url_for("home"))
