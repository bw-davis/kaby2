import flask
from flask import Flask
from flask import render_template
from flask import request
from flaskext.mysql import MySQL
app = Flask(__name__)


mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'guest'
app.config['MYSQL_DATABASE_PASSWORD'] = 'guest'
app.config['MYSQL_DATABASE_DB'] = 'kaby'
app.config['MYSQL_DATABASE_HOST'] = 'ix.cs.uoregon.edu'
app.config['MYSQL_DATABASE_PORT'] = 3225
mysql.init_app(app)

conn = mysql.connect()

@app.route('/')
@app.route('/login')
def login():
    cur = conn.cursor()
    cur.execute("SELECT * from user")

    rows = cur.fetchall()
    conn.close()

    for row in rows:
		print row
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


