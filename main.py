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

"""
conn = mysql.connect()
cur = conn.cursor()
cur.execute("SELECT * from user")
rows = cur.fetchall()
conn.close()

"""

group_leaders = [1,2,3]

def get_group_leaders():
	group_leaders 
	conn = mysql.connect()
	cur = conn.cursor()
	query_string="select group_leader_email from group_leader;"
	cur.execute(query_string)
	rows = cur.fetchall()
	for row in rows:
		group_leaders.append(row[0]);
	conn.close()

@app.route('/')
@app.route('/login')
def login():
	
    #for row in rows:
		#print row
    return render_template('login.html') 
	


@app.route('/home')
def home():
    return render_template('index.html') 

@app.route('/newMeeting')
def newMeeting():
	get_group_leaders()
	for o in group_leaders:
		print o
	return render_template('newMeeting.html') 


@app.route('/newContact')
def newContact():
    return render_template('newContact.html') 

@app.route('/form_action', methods=['POST'])
def form_action():
	date = request.form.get('date')
	print(date);
	return flask.redirect(flask.url_for("home"))


@app.route('/login_action', methods=['POST'])
def login_action():
	name = request.form.get('user_name')
	passwd = "{}".format(request.form.get('password'))
	conn =  mysql.connect()
	cur = conn.cursor()
	query_string = "SELECT password from user where fname='{}'".format(name)
	cur.execute(query_string)
	rows = cur.fetchall()
	for row in rows:
		if (row[0] == passwd): 
			print("passowords Match")
			conn.close()
			return flask.redirect(flask.url_for("home"))
		else:
			print("row{} does not equal password{}".format(row, passwd))
	conn.close()
	return flask.redirect(flask.url_for("login"))



@app.route('/newMeeting')
def a():
    print("HELLO")
    return render_template('newMeeting.html') 


#################
#
# Favicon function rendering
#
#################
"""
@app.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
"""
