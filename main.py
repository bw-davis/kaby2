import flask
from flask import Flask, render_template, request
from flaskext.mysql import MySQL
from flask_mail import Mail, Message

app = Flask(__name__)

mail = Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'kabymeetingplanner@gmail.com'
app.config['MAIL_PASSWORD'] = 'kabykabykaby'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


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

group_leaders = []
dates = []
num_dates=0;
cur_meeting_id=0;
length_min=0

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
    return render_template('login.html') 
	


@app.route('/home')
def home():
    return render_template('index.html') 

@app.route('/newMeeting')
def newMeeting():
	get_group_leaders()
	return render_template('newMeeting.html',  leaders=group_leaders)


@app.route('/newContact')
def newContact():
    return render_template('newContact.html') 


@app.route('/timePage')
def timePage():
    return render_template('time_picker.html') 

@app.route("/view_meeting/<meeting_id>")
def view_meeting(meeting_id):
    app.logger.debug("Entering view_meeting")

    print(meeting_id)  
    return render_template('view_meeting.html')


@app.route('/form_action', methods=['POST'])
def form_action():
    global dates
    global num_dates
    global cur_meeting_id;
    global length_min
    date = request.form.get('date')
    dates = date.split(",");
    num_dates = len(dates)
    print("num dates entered: {}".format(num_dates))
    for d in dates:
        print ("date:{}".format(d))
    name = request.form.get('mName')
    desc = request.form.get('desc')
    loc= request.form.get('loc')
    length_min= request.form.get('meeting_len')
    print("length : {}".format(length_min));
    conn =  mysql.connect()
    cur = conn.cursor()
    query_string = "insert into meetings (meeting_id, location, description) values ({}, '{}', '{}')".format("Null",loc, desc)
    cur.execute(query_string)
    cur_meeting_id = cur.lastrowid
    print ("row id : {}".format(cur_meeting_id));
    conn.commit()
    conn.close()
    return render_template('time_picker.html', dates=dates) 


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

@app.route('/contact_action', methods=['POST'])
def contact_action():
	group_name = request.form.get('group_name')
	email_address = request.form.get('email_address')
	print("group_name");
	print(group_name);
	print("email_address:");
	print(email_address);
	conn =  mysql.connect()
	cur = conn.cursor()
	query_string = "INSERT INTO `kaby`.`group_leader` (`group_leader_email`, `group_name`) VALUES ('{}', '{}');".format(email_address,group_name)
	print(query_string)
	cur.execute(query_string)
	conn.commit()
	conn.close()
	return flask.redirect(flask.url_for("home"))

@app.route('/newmeeting_action', methods=['POST'])
def newmeeting_action():
    cntr=0;
    global num_dates;
    global length_min
    global cur_meeting_id
    global dates
    conn =  mysql.connect()
    cur = conn.cursor()
    for i in range(num_dates):
        print("global dates[i]={}".format(dates[i]))
        name = "t{}".format(i+1);
        day, month, year = dates[i].split("/");
        sql_date='{}-{}-{}'.format(year, month,day);
        time = request.form.get(name)
        sql_time='{}:00:00'.format(time)
        print (sql_time) 
        query_string = "insert into meetings_times_dates (issue_ID, meeting_id, start_time, date, length) values ({}, {}, '{}', '{}', {});".format("NULL", cur_meeting_id, sql_time, sql_date, int(length_min));
        cur.execute(query_string)
        print ("row id : {}".format(cur_meeting_id))
        conn.commit()
    conn.close()
    return flask.redirect(flask.url_for("home"))




#################
#
# Helper functions to be used by Flask 
#
#################


def send_message(title, body, receivers):
    '''
    Send a message using the Kaby Meeting Planner email 

    Args:
        title: str, the title of the email
        body:  str, the body of the email
        receivers: list of str, the emails of recipients. Example: ["owen@uoregon.edu", "andy@gmail.com"]
    Returns:
        Nothing
    '''
    with app.app_context():
        msg = Message(title, sender=('Kaby Meeting Planner','kabymeetingplanner@gmail.com'), recipients=receivers)
        msg.body = body
        mail.send(msg)

#send_message("Hello", "World", ['yuboz@uoregon.edu'])

#################
#
# Favicon function rendering
#
#################

  


"""
>>>>>>> 77b94e94855271545388c3d8efe253aabd1214d5
@app.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
"""
