import flask
from flask import Flask, render_template, request, redirect, url_for, session
from flaskext.mysql import MySQL
from flask_mail import Mail, Message

from datetime import timedelta
import uuid
import os
import re


app = Flask(__name__)

# Mail configurations
app.config['SECRET_KEY'] = 'filesystem'
app.config.update(SECRET_KEY='123456')  
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'kabymeetingplanner@gmail.com'
app.config['MAIL_PASSWORD'] = 'kabykabykaby'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


# MySQL configurations
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'guest'
app.config['MYSQL_DATABASE_PASSWORD'] = 'guest'
app.config['MYSQL_DATABASE_DB'] = 'kaby'
app.config['MYSQL_DATABASE_HOST'] = 'ix.cs.uoregon.edu'
app.config['MYSQL_DATABASE_PORT'] = 3225
mysql.init_app(app)

#Global variables
group_leaders = []
dates = []
num_dates=0;
cur_meeting_id=0;
length_min=0
meetings = []
email_list=[]
uuid_url="";
response_meeting=0;

def get_meetings():
	global meetings
	conn = mysql.connect()
	cur = conn.cursor()
	query_string="select * from meetings;"
	cur.execute(query_string)
	rows= cur.fetchall()
	for row in rows:
		if (row[2] != ""): 
			meetings.append((row[2], row[4]))
	conn.close()

def get_group_leaders():
	global group_leaders 
	group_leaders=[]
	conn = mysql.connect()
	cur = conn.cursor()
	query_string="select group_leader_email from group_leader;"
	cur.execute(query_string)
	rows = cur.fetchall()
	for row in rows:
		group_leaders.append(row[0]);
	conn.close()

@app.before_request
def before_action():
    print (request.path)
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=10)
    if request.path.find('.png')==-1:
        if not request.path=='/login' and  not request.path=='/login_action' and not re.search("respond", request.path)!=None and not re.search("thanks", request.path)!=None:
            if not 'username' in session:
                print('not in session!!')
                session['newurl']=request.path
            #        if not 'username' in session and not 'password' in session:
            #            print(session['username'])
            #            print('*****')
            #            print(session['username'])
            #            session['newurl']=request.path
                print('you should go to login')
                return flask.redirect(flask.url_for("login"))
            #    return
            else:
                print('in session!!')

@app.route('/')
@app.route('/login')
def login():
    print("login")
    return render_template('login.html') 

@app.route('/logout')	
def logout():
    print('im in logout')
    session.clear() 
    return flask.redirect(flask.url_for("login"))

@app.route('/home')
def home():
    return render_template('index.html', meetings=meetings) 

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
    #print("leader {}".format(get_leaders_for_meetingID(meeting_id)))
    ''' # Dummy info for development
    return render_template('view_meeting.html', title="CIS 422 Debugging Meeting",
                            location="Deschutes 100", not_responders=["Alex", "Andrew"],
                            responders = [("Don", [("02/22", "07:00", "07:30"),
                                                   ("02/23", "12:00", "12:30")]),
                                          ("Yubo", [("02/24", "13:00", "13:30")])])
    '''
    print("dts {}".format(get_dts(meeting_id)))
    return render_template('view_meeting.html')

@app.route("/respond/<meeting_id>")
def respond(meeting_id):
    global response_meeting;
    print(meeting_id)  
    #return render_template('respond.html')
    #This is dummy information for testing purposes
    dates=get_dts(meeting_id)
    response_meeting=meeting_id;
    return render_template('respond.html', names=get_leaders_for_meetingID(meeting_id),
            dts=dates)

@app.route("/thanks")
def thanks():
    return render_template('thanks.html')


#########
## POST METHODS
#########

@app.route('/form_action', methods=['POST'])
def form_action():
    global dates
    global num_dates
    global cur_meeting_id;
    global length_min
    global email_list
    global uuid_url
    email_list=[]
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
    uuid_url = get_uuid()
    insert_meeting(loc, desc, length_min, uuid_url)
    print ("row id : {}".format(cur_meeting_id));
    leaders_to_meet = request.form.getlist('dd2');
    for l in leaders_to_meet:
        print("email {}".format(l));
        email_list.append(l);
        set_response(l);
    return render_template('time_picker.html', dates=dates) 


@app.route('/login_action', methods=['POST'])
def login_action():
    print("I'm in login_action")
    name = request.form.get('user_name')
    passwd = "{}".format(request.form.get('password'))
    conn =  mysql.connect()
    cur = conn.cursor()
    query_string = "SELECT password from user where fname='{}'".format(name)
    cur.execute(query_string)
    rows = cur.fetchall()
    for row in rows:
        if (row[0]==passwd):
            print("passowords Match")
            print(request.form.get('user_name'))
            print('name')
            session['username'] = name
            conn.close()
            get_meetings()
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
    global email_list
    global uuid_url
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
        #query_string = "insert into meetings_times_dates (issue_ID, meeting_id, start_time, date, length) values ({}, {}, '{}', '{}', {});".format("NULL", cur_meeting_id, sql_time, sql_date, int(length_min));
        time_ranges = time.split(',');
        for t in time_ranges:
            start_time, end_time = t.split('-');
            print("start {} end {}".format(start_time, end_time)) 
            sql_start_time = '{}:00:00'.format(start_time) 
            sql_end_time= '{}:00:00'.format(end_time) 
            query_string = "INSERT INTO `kaby`.`dates_times` (`dt_id`, `meeting_id`, `start_time`, `end_time`, `meeting_date`) VALUES ({}, {}, '{}', '{}', '{}');".format("NULL", cur_meeting_id, sql_start_time.strip('0'), sql_end_time , sql_date);
            cur.execute(query_string)
            print ("row id : {}".format(cur_meeting_id))
            conn.commit()
    conn.close()
    link = "ix.cs.uoregon.edu:5951/respond/" + uuid_url
    send_message("You've been invited", link, email_list);
    return flask.redirect(flask.url_for("home"))


@app.route('/respond_meeting', methods=['POST'])
def respond_meeting():
    global response_meeting
    user_name = request.form.get('user_name')
    available_times = request.form.getlist('available_times')
    available_times = [x.encode('ascii','ignore') for x in available_times] #convert from unicode to str

    print("Username: " + user_name)
    print("Available times: ", available_times)
    user_id= group_leader_email_to_id(user_name);
    print("\n\n user name {} to user id {}".format(user_name, user_id))
    print("resp id {}".format(response_meeting))

    insert_user_response(user_id ,response_meeting, available_times)
    return flask.redirect(flask.url_for("thanks"))


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

def get_uuid():
    """
    Creates a unique identifier 

    Returns:
        str, a unique identifier of the form '32187f9c-9dd3-4ffe-b919-c80ddf90e717'
    """
    return str(uuid.uuid4())




#################
# MySQL Helper functions
################

def add_to_respond_meeting(leader_id, meeting_id):
	print("adding to respond table")
	query_add_respond = "insert into respond_meeting (issue_ID, group_id) values ({},{})".format(meeting_id, leader_id);
	conn = mysql.connect()
	cur = conn.cursor()
	cur.execute(query_add_respond);
	conn.commit()
	conn.close()

def set_response(leader):
    conn2 =  mysql.connect()
    cur2 = conn2.cursor()
    query_string_userID = "SELECT * FROM group_leader where group_leader_email='{}'".format(leader);
    cur2.execute(query_string_userID)
    p = cur2.fetchone()
    leader_to_add = p[0];
    print("\n\n just got {} \n\n".format(leader_to_add));
    conn2.close();
    add_to_respond_meeting( leader_to_add,cur_meeting_id);


def insert_meeting(loc, desc, length_min, uuid_url):
	global cur_meeting_id 
	query_string = "insert into meetings (meeting_id, location, description, length, uuid) values ({}, '{}', '{}', '{}', '{}')".format("Null",loc, desc, length_min, uuid_url)
	conn =  mysql.connect()
	cur = conn.cursor()
	cur.execute(query_string)
	cur_meeting_id = cur.lastrowid
	conn.commit()
	conn.close()


def get_leaders_for_meetingID(uuid_url):
    #uuid_url to meeeting id
    query_string = "select * from meetings where uuid='{}'".format(uuid_url)
    conn =  mysql.connect()
    cur = conn.cursor()
    all_attendees=[]
    cur.execute(query_string)
    meeting = cur.fetchone()
    meeting_id = meeting[0];
    #print(meeting_id)
    all_attendees = all_contacts_id_for_meeting(meeting_id)
    conn.close()
    return all_attendees

def all_contacts_id_for_meeting(meeting_id):
    query_string = "select * from respond_meeting where issue_ID={}".format(meeting_id)
    all_attendees=[];
    conn =  mysql.connect()
    cur = conn.cursor()
    cur.execute(query_string)
    attendees = cur.fetchall()
    #print("attendees")
    for a in attendees:
    #    print(a);
        all_attendees.append(get_contacts_for_meeting(a[1]))
        
    conn.close()
    return all_attendees


def get_contacts_for_meeting(group_leader_id):
    query_string = "select * from group_leader where group_leader_id={};".format(group_leader_id)
    conn =  mysql.connect()
    cur = conn.cursor()
    cur.execute(query_string)
    attendees = cur.fetchone()
    #print(attendees[1]);
    conn.close()
    return attendees[1];


def get_dts(meeting_id):
    query = "select * from dates_times JOIN meetings using(meeting_id) where uuid ='{}'".format(meeting_id)
    conn =  mysql.connect()
    cur = conn.cursor()
    cur.execute(query)
    all_dts=[]
    dts = cur.fetchall()
    for i in dts:
        dt, stime, etime = i[4], i[2], i[3]
        #print("dt {}, stime {}, etime {}".format(dt, stime, etime))
        all_dts.append((dt, stime, etime))
    conn.close()
    return all_dts;


def group_leader_email_to_id(group_leader_email):
    query_string = "select * from group_leader where group_leader_email='{}';".format(group_leader_email)
    conn =  mysql.connect()
    cur = conn.cursor()
    cur.execute(query_string)
    leader = cur.fetchone()
    conn.close()
    return leader[0];

def get_dt_id(meeting_id, meeting_date):
    print("id {} date {}".format(meeting_id, meeting_date));
    query_string = "select * from dates_times where meeting_date='{}' and meeting_id={};".format(meeting_date, meeting_id)
    conn =  mysql.connect()
    cur = conn.cursor()
    cur.execute(query_string)
    leader = cur.fetchone()
    conn.close()
    return leader;

def insert_user_response(group_leader_id, meeting_id, available_times):
    for a in available_times:
        year, day, month, stime, etime = a.split("-")
        m_date = '{}-{}-{}'.format(year,day,month)
        print("date {} stime {} etime{}".format(m_date, stime, etime))
        print("dt_id{} => ".format(get_dt_id(meeting_id,m_date)))
	#query_string = "insert into response (dt_id, start_time, end_time, group_leader_id) values ({},{},{},{});",format(meeting_id, stime, etime, grop_leader_id))
	#conn =  mysql.connect()
	#cur = conn.cursor()
	#cur.execute(query_string)
	#cur_meeting_id = cur.lastrowid
	#conn.commit()
	#conn.close()



#################
#
# Favicon function rendering
#
#################

@app.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
