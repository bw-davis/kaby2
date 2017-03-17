"""
Authors: Andrew Hill, Alex Owen, and Yubo Zhang

This module contains all the logic for the Flask sever. This module is split into the 4 following sections:
1. Routing functions: Used to render html and jinja2 files, and set up the urls for each page
2. Post methods: Gets all user input from the website using post method. These function then can call various helper or MySQL query functions
3. Helper functions: Helper functions called by post methods used to send emails, set up server connection, and parse/handle data from the database
4. MySQL query functions: Helper function called by post methods to get data from, add data to, or delete data from the MySQL database.
"""

import flask
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flaskext.mysql import MySQL
from flask_mail import Mail, Message
import re
from datetime import timedelta
from datetime import datetime
import uuid
import os
import re
import operator


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
past_meetings=[]
email_list=[]
uuid_url="";
response_meeting="";





######
# Routing Functions
######


'''
Flask routing function used to change icon in browser tab.
------------------------------------------------------------------------------------------------------------
    arguments:
        None
    
    side affects:
        None

    return:
        None
'''
@app.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')





'''
Routing function used to check if a user has is logged in or not any time a user tires to load a new page
-----------------------------------------------------------------------------------------------------------------------
    arguments:
        None

    side affects:
        Checks if a user is logged in or not, of if a users login time has expired. If a user is not logged in or 
        have been in active for longer then 10 minutes, they are redirected to the login page. Other wise they can
        navigate the site freely

    return:
        None
'''

@app.before_request
def before_action():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=10)
    if request.path.find('.png')==-1:
        if not request.path=='/login' and  not request.path=='/login_action' and not re.search("respond", request.path)!=None and not re.search("thanks", request.path)!=None:
            if not 'username' in session:
                session['newurl']=request.path
                return flask.redirect(flask.url_for("login"))
            else:
                print('in session!!')


'''
Routing function used to render the long.html file when some successful logs in
-----------------------------------------------------------------------------------------------------------------------
    arguments:
        None

    side affects:
        Renders the login.html file and sets the url for this page

    return:
        None
'''
@app.route('/')
@app.route('/login')
def login():
    #print("login")
    return render_template('login.html') 



'''
Routing function used to handle logout button and redirect user to login page
-----------------------------------------------------------------------------------------------------------------------
    arguments:
        None

    side affects:
        Logs user out of the session, and redirects them to the login page

    return:
        None
'''
@app.route('/logout')	
def logout():
    session.clear() 
    return flask.redirect(flask.url_for("login"))


'''
Routing function used to render the index.html file
-----------------------------------------------------------------------------------------------------------------------
    arguments:
        None

    side affects:
        Renders the index.html file and sets the url for this page

    return:
        None
'''
@app.route('/home')
def home():
    get_upcoming_meetings()
    get_past_meetings()
    return render_template('index.html', meetings=meetings, past_meetings=past_meetings) 



'''
Routing function used to render the newMeeting.html file
-----------------------------------------------------------------------------------------------------------------------
    arguments:
        None

    side affects:
        Renders the newMeeting.html file and sets the url for this page

    return:
        None
'''
@app.route('/newMeeting')
def newMeeting():
	get_group_leaders()
	return render_template('newMeeting.html',  leaders=group_leaders)


'''
Routing function used to render the newContact.html file
-----------------------------------------------------------------------------------------------------------------------
    arguments:
        None

    side affects:
        Renders the newContact.html file and sets the url for this page

    return:
        None
'''
@app.route('/newContact')
def newContact():
    conn1 =  mysql.connect()
    cur1 = conn1.cursor()
    query_string1 = "SELECT group_leader_email FROM kaby.group_leader;"
    cur1.execute(query_string1)
    rows1 = cur1.fetchall()
    for row1 in rows1:
            print("******");
            print(row1)
    conn1.close()
    conn2 =  mysql.connect()
    cur2 = conn2.cursor()
    query_string2 = "SELECT group_name FROM kaby.group_leader;"
    cur2.execute(query_string2)
    rows2 = cur2.fetchall()
    for row2 in rows2:
            print("******");
            print(row2)
    conn2.close()

    return render_template('newContact.html', emaillist=rows1,namelist=rows2) 


'''
Routing function used to render the time_picker.html file
-----------------------------------------------------------------------------------------------------------------------
    arguments:
        None

    side affects:
        Renders the time_picker.html file and sets the url for this page

    return:
        None
'''
@app.route('/timePage')
def timePage():
    return render_template('time_picker.html') 


'''
Routing function used to render the view_meeting.html file
-----------------------------------------------------------------------------------------------------------------------
    arguments:
        None

    side affects:
        Renders the view_meeting.html file and sets the url for this page

    return:
        None
'''
@app.route("/view_meeting/<meeting_id>")
def view_meeting(meeting_id):
    global cur_meeting_id
    resp={};
    respond=[];
    app.logger.debug("Entering view_meeting")
    meeting_info = get_meeting_info(meeting_id)
    m_id=uuid_to_meeting_id(meeting_id); #meeting_id here is uuid_url, shoudl change.
    cur_meeting_id=m_id;
    not_resp = get_not_responded(m_id)
    resp = get_responded(m_id)
    resp_list=[]
    for name, times in resp.iteritems():
        sorted_time = sorted(times, key=operator.itemgetter(1))
        sorted_time = sorted(sorted_time, key=operator.itemgetter(0))
        temp=[name, sorted_time]
        resp_list.append(temp);
    return render_template('view_meeting.html', title=meeting_info[1],desc=meeting_info[2],
                            location=meeting_info[0], not_responders=not_resp,
                            responders=resp_list, dt_id=m_id)



'''
Routing function used to render the respond.html file
-----------------------------------------------------------------------------------------------------------------------
    arguments:
        None

    side affects:
        Renders the respond.html file and sets the url for this page

    return:
        None
'''
@app.route("/respond/<meeting_id>")
def respond(meeting_id):
    global response_meeting;
    print(meeting_id)  
    dates=get_dts(meeting_id)
    response_meeting=meeting_id;
    print("\n\nresp id1 {}\n\n".format(response_meeting))
    print("dates ={}", dates)
    return render_template('respond.html', names=get_leaders_for_meetingID(meeting_id),
            dts=dates)



'''
Routing function used to render the thanks.html file
-----------------------------------------------------------------------------------------------------------------------
    arguments:
        None

    side affects:
        Renders the thanks.html file and sets the url for this page

    return:
        None
'''
@app.route("/thanks")
def thanks():
    return render_template('thanks.html')


#########
## POST METHODS
#########


'''
Post method used to get all user input from the log in screen and check the database to log in a user or not
-----------------------------------------------------------------------------------------------------------------------
    arguments:
        None

    side affects:
        Gets all user input from screen, calls a MySQL query to check if users input email and password match. If they match
        user is redirected to the home page, if they do not match then user is prompted to enter this info again.

    return:
        None
'''
@app.route('/login_action', methods=['POST'])
def login_action():
    #print("I'm in login_action")
    email = request.form.get('user_name').replace("'", "")
    passwd = "{}".format(request.form.get('password'))
    conn =  mysql.connect()
    cur = conn.cursor()
    query_string = "SELECT password from user where email='{}'".format(email)
    cur.execute(query_string)
    rows = cur.fetchall()
    print("\n\n\n  rows={}".format(rows))
    for row in rows:
        print("\n\n\n  password={}".format(row[0]))
        if (row[0]==passwd):
            print("matches")
            session['username'] = email 
            conn.close()
            return flask.redirect(flask.url_for("home"))
        else:
            print("row{} does not equal password{}".format(row, passwd))
    conn.close()
    return flask.redirect(flask.url_for("login"))


'''
Post method used to get all user input from the new contact page add this to the database
-----------------------------------------------------------------------------------------------------------------------
    arguments:
        None

    side affects:
        Gets all user input from screen, calls a MySQL query to create a new user instance for this user and stores all user info.
        Javascript checking is done on the HTML page to ensure this user does not already exist in the database.

    return:
        None
'''
@app.route('/contact_action', methods=['POST'])
def contact_action():
    group_name = request.form.get('group_name').replace("'", "")
    email_address = request.form.get('email_address').replace("'", "")
    conn =  mysql.connect()
    cur = conn.cursor()
    query_string = "INSERT INTO `kaby`.`group_leader` (`group_leader_email`, `group_name`) VALUES ('{}', '{}');".format(email_address,group_name)
    cur.execute(query_string)
    conn.commit()
    conn.close()
    return flask.redirect(flask.url_for("home"))


'''
Post method used to get all user input from the new meeting page add this to the database
-----------------------------------------------------------------------------------------------------------------------
    arguments:
        None

    side affects:
        Gets all user input from screen, calls a mysql query to create a new meeting instance for this user and stores all user info.
        Javascript checking is done on the html page to ensure all needed data has been entered and is of the right type and format.

    return:
        None
'''
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
    for d in dates:
        print ("date:{}".format(d))
    name = request.form.get('mName').replace("'","")
    desc = request.form.get('desc').replace("'","")
    loc= request.form.get('loc').replace("'", "")
    length_min= request.form.get('meeting_len')
    print("length : {}".format(length_min));
    uuid_url = get_uuid()
    insert_meeting(loc, desc, length_min, uuid_url, name, session['username'])
    leaders_to_meet = request.form.getlist('dd2');
    for l in leaders_to_meet:
        #print("email {}".format(l));
        email_list.append(l);
        set_response(l);
    print("im here!!!!!!!!!!");
    dates.sort();
    return render_template('time_picker.html', dates=dates,length_min0=length_min) 



'''
Post method used to get all user input from the timepicker page add this to the database
-----------------------------------------------------------------------------------------------------------------------
    arguments:
        None

    side affects:
        Gets all user input from screen, calls a mysql query to create a new time date object for all possible time dates
        on the given date with the given length. Javascript checking is done on the html page to ensure all needed data has 
        been entered and is of the right type and format.

    return:
        None
'''
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
        #print("global dates[i]={}".format(dates[i]))
        name = "t{}".format(i+1)
        month, day, year = dates[i].split("/")
        sql_date='{}-{}-{}'.format(year, month,day)
        time = request.form.get(name)
        #sql_time='{}:00:00'.format(time)
        time_ranges = time.split(',')
        for t in time_ranges:
            start_time, end_time = t.split('-')
            #print("start {} end {}".format(start_time, end_time)) 
            start_hour = start_time[0:2]
            start_mins = start_time[2:]
            end_hour   = end_time[0:2]
            end_mins   = end_time[2:]
            sql_start_time = '{}:{}:00'.format(start_hour, start_mins)
            sql_end_time = '{}:{}:00'.format(end_hour, end_mins) 
            result = split_into_intervals(sql_date, sql_start_time, sql_end_time, int(length_min))
            #print(result)
            for d, s, e in result:
                query_string = "INSERT INTO dates_times (dt_id, meeting_id, start_time, end_time, meeting_date) VALUES ({}, {}, '{}', '{}', '{}');".format("NULL", cur_meeting_id, s, e , d)
                cur.execute(query_string)
                conn.commit()
    conn.close()
    link = "http://ix.cs.uoregon.edu:5951/respond/" + uuid_url
    #link = "http://127.0.0.1:5000/respond/" + uuid_url
    send_message("You've been invited", link, email_list)
    get_upcoming_meetings()
    get_past_meetings()
    return render_template('index.html', meetings=meetings, past_meetings=past_meetings) 


'''
Post method used to get all user input from the respond page add this to the database
-----------------------------------------------------------------------------------------------------------------------
    arguments:
        None

    side affects:
        Gets all user input from screen, calls a mysql query to create a new response instance for each possible 
        meeting time and date the contact responds to. Javascript checking is done on the html page to ensure all needed data has 
        been entered and is of the right type and format.

    return:
        None
'''
@app.route('/respond_meeting', methods=['POST'])
def respond_meeting():
    global response_meeting
    user_name = request.form.get('user_name')
    available_times = request.form.getlist('available_times')
    if (not available_times):
        available_times=['0000-00-00-00:00:00-00:00:00']
    else:
        available_times = [x.encode('ascii','ignore') for x in available_times] #convert from unicode to str
    print("\n\n")
    print(available_times)
    user_id= group_leader_email_to_id(user_name)
    insert_user_response(user_id ,response_meeting, available_times)
    m_id=uuid_to_meeting_id(response_meeting); #meeting_id here is uuid_url, shoudl change.
    num_not_resp = get_num_non_responded(m_id)
    email=get_creator_email(response_meeting);
    email_list=[email]
    link="http://ix.cs.uoregon.edu:5951/view_meeting/" + response_meeting
    #link="http://127.0.0.1:5000/view_meeting/" + response_meetingh
    #print("\n\n number not responded = {} \n\n").format(num_not_resp);
    if(num_not_resp == 0):
        #print("email prfessor")
        send_message("All groups have responded", link, email_list);
    else:
        print("dont email yet")
    return flask.redirect(flask.url_for("thanks"))


'''
Post method used to get all user input from the view_meeting page add this to the database
-----------------------------------------------------------------------------------------------------------------------
    arguments:
        None

    side affects:
        Gets all user input from screen, calls a mysql query to to update the checked property for each response the user check.

    return:
        None
'''
@app.route('/viewmeeting_action', methods=['POST'])
def viewmeeting_action():
    global cur_meeting_id;
    print("\n\n\n hello there \n\n\n")
    sel_times = request.form.getlist('sel_times')
    print("\n\n sel_times = {}".format(sel_times));
    reset_all_response_check(cur_meeting_id)
    check_meetings(sel_times)
    return flask.redirect(flask.url_for("home"))

#################
## Helper functions to be used by Flask 
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

def split_into_intervals(date, st, et, meeting_len):
    """
    Takes a SQL-format date, start time, and end time, and splits it into
    chucks of length 'meeting_len'

    Args:
        date:        str, of the form "yyyy-mm-dd"
        st:          str, of the form "hh:mm:ss"
        et:          str, of the form "hh:mm:ss"
        meeting_len: int, length of meeting in minutes

    Returns:
        list of tuples, where tuple of the form (date, st, et)
    """
    result = []
    st_fmt = "{} {}".format(date, st)
    et_fmt = "{} {}".format(date, et)
    print("st_fmt: ", st_fmt)
    print("et_fmt: ", et_fmt)
    st_dt = datetime.strptime(st_fmt, "%Y-%m-%d %H:%M:%S")
    et_dt = datetime.strptime(et_fmt, "%Y-%m-%d %H:%M:%S")
    delta = timedelta(0, meeting_len*60)  #timedelta takes seconds
    while st_dt + delta <= et_dt:
        start = st_dt
        end   = st_dt + delta
        tup = (str(start).split()[0], str(start).split()[1], str(end).split()[1])
        result.append(tup)
        st_dt += delta
    return result



#################
## MySQL query functions
################


'''
Mysql helper gets all the contacts
------------------------------------------------------------------------------------------------------------
    arguments:
        None

    side affects:
        populates the group leaders global array with all the contacts stored in the database

    return:
        None
'''
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


'''
Mysql helper: converts a group_leader_email to a group_leader_id an passes that id to the add_to_respond_meeting function 
-----------------------------------------------------------------------------------------------------------------------
    arguments:
        leader_id: unique group leader id
        meeting_id: unique meeting id

    side affects:
        inserts this group leader id meeting id into the respond_meeting table

    return:
        None
'''
def add_to_respond_meeting(leader_id, meeting_id):
	#print("adding to respond_meeting table")
	query_add_respond = "insert into respond_meeting (issue_ID, group_id) values ({},{})".format(meeting_id, leader_id);
	conn = mysql.connect()
	cur = conn.cursor()
	cur.execute(query_add_respond);
	conn.commit()
	conn.close()


'''
Mysql helper: converts a group_leader_email to a group_leader_id an passes that id to the add_to_respond_meeting function 
-----------------------------------------------------------------------------------------------------------------------
    arguments:
        leader: group leader of contacts email

    side affects:
        gets the unique group_leader_id for this user and calls add_to_respond_meeting

    return:
        None
'''
def set_response(leader):
    conn2 =  mysql.connect()
    cur2 = conn2.cursor()
    query_string_userID = "SELECT * FROM group_leader where group_leader_email='{}'".format(leader);
    cur2.execute(query_string_userID)
    p = cur2.fetchone()
    leader_to_add = p[0];
    #print("\n\n just got {} \n\n".format(leader_to_add));
    conn2.close();
    add_to_respond_meeting( leader_to_add,cur_meeting_id);


'''
Mysql helper: inserts a meeting into the databse
------------------------------------------------------------------------------------------------------------
    arguments:
        loc: string storing the location of a meeting
        desc: string storing the description of a meetin 
        lenght_min: int specifying the length of a meeting
        uuid_url: string storing the unique url for a meeting
        creator_email: string storing the email of the user who created the email

    side affects:
        Inserts a new meeting into the database

    return:
        None
'''
def insert_meeting(loc, desc, length_min, uuid_url, meeting_name, creator_email):
	global cur_meeting_id 
	query_string = "insert into meetings (meeting_id, location, description, length, uuid, meeting_name, creator_email) values ({}, '{}', '{}', '{}', '{}', '{}', '{}')".format("Null",loc, desc, length_min, uuid_url, meeting_name, creator_email)
	conn =  mysql.connect()
	cur = conn.cursor()
	cur.execute(query_string)
	cur_meeting_id = cur.lastrowid
	conn.commit()
	conn.close()


'''
Mysql helper: returns an array of all group leader info for all group leaders attending a meeting
------------------------------------------------------------------------------------------------------------
    arguments:
        meeting_id: a unique id for a meeting

    side affects:
        None

    return:
        all_attendess: array of tuples of all group leader info, for all contacts invited to a meeting.
'''
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


'''
Mysql helper: returns an array of all group leader ids of all group leaders attending a meeting
------------------------------------------------------------------------------------------------------------
    arguments:
        meeting_id: a unique id for a meeting

    side affects:
        None

    return:
        all_attendess: array of group_leader_ids for all contacts invited to a meeting.
'''
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


'''
Mysql helper: gets all information of a group_leader by their unique group_leader_id
------------------------------------------------------------------------------------------------------------
    arguments:
        group_leader_id: a unique id for a group leader
    
    side affects:
        None
    return:
        Tuple of all data about this group leader( id, email, fname, lname, group name);
'''
def get_contacts_for_meeting(group_leader_id):
    query_string = "select * from group_leader where group_leader_id={};".format(group_leader_id)
    conn =  mysql.connect()
    cur = conn.cursor()
    cur.execute(query_string)
    attendees = cur.fetchone()
    #print(attendees[1]);
    conn.close()
    return attendees[1];

'''
Mysql helper: returns all datetime possibilities for a meeting
------------------------------------------------------------------------------------------------------------
    arguments:
        meeting_id: a unique id for a meeting
    
    side affects:
        None
    return:
        all_dts: a list of datetime objects representing all possible date time combinations for a given meeting
'''
def get_dts(meeting_id):
    query = "select * from dates_times JOIN meetings using(meeting_id) where uuid ='{}'".format(meeting_id)
    conn =  mysql.connect()
    cur = conn.cursor()
    cur.execute(query)
    all_dts=[]
    dts = cur.fetchall()
    for i in dts:
        st = str(i[2])
        shour, smin, ssec = st.split(":")
        stime="{}:{}".format(shour, smin)
        print("\n\n\n stime {}\n\n\n".format(stime))
        et = str(i[3])
        ehour, emin, esec = et.split(":")
        etime="{}:{}".format(ehour, emin)
        print("\n\n\netime {}\n\n\n".format(etime))
        dt = i[4] 
        #print("dt {}, stime {}, etime {}".format(dt, stime, etime))
        all_dts.append((dt, stime, etime))
    conn.close()
    return all_dts;


'''
Mysql helper: converts a group_leader_email to their unique id
------------------------------------------------------------------------------------------------------------
    arguments:
        group_leader_email: The group leaders email you want the group leader id for
    
    side affects:
        Adds all contacts available times to the database

    return:
        None
'''
def group_leader_email_to_id(group_leader_email):
    query_string = "select * from group_leader where group_leader_email='{}';".format(group_leader_email)
    conn =  mysql.connect()
    cur = conn.cursor()
    cur.execute(query_string)
    leader = cur.fetchone()
    conn.close()
    return leader[0];



'''
Mysql helper: gets the unique dt_id(date time id) for a specific date and time
------------------------------------------------------------------------------------------------------------
    arguments:
        meeting_date: datetime object used to represent one specific date and time for a meeting
        meeting_id: unique id for meeting the user has responded to
    
    side affects:
        Adds all contacts available times to the database

    return:
        Returns the leaders who can meet at this time.
'''
def get_dt_id(meeting_id, meeting_date):
    #print("id {} date {}".format(meeting_id, meeting_date));
    query_string = "select * from meetings join dates_times using (meeting_id) where uuid='{}'".format(meeting_id)
    conn =  mysql.connect()
    cur = conn.cursor()
    cur.execute(query_string)
    leader = cur.fetchone()
    conn.close()
    #print("\n\n leader = {} \n\n".format(leader))
    if (not leader):
        return None
    return leader[0];


'''
Mysql helper: used to check or selected property of a response
------------------------------------------------------------------------------------------------------------
    arguments:
        group_leader_id: unique id for the leader whos responses are being entered
        meeting_id: unique id for meeting the user has responded to
        available times: an array of data time objects, that represents when this contact can meet and is to
                          be inserted into the database.
    
    side affects:
        Adds all contacts available times to the database

    return:
        None
'''
def reset_all_response_check(dt_id):
    query_allow_update ="SET SQL_SAFE_UPDATES = 0;"
    query_disallow_update ="SET SQL_SAFE_UPDATES = 1;"
    conn =  mysql.connect()
    cur = conn.cursor()
    cur.execute(query_allow_update)
    query_string="update response set checked=0 where dt_id={};".format(dt_id)
    cur = conn.cursor()
    cur.execute(query_string)
    conn.commit()
    cur = conn.cursor()
    cur.execute(query_disallow_update)
    conn.close()



'''
Mysql helper: that stores which which responses were selected on the view_meeting page
------------------------------------------------------------------------------------------------------------
    arguments:
       sel_times: this is an array of all the selected times to be stored in the database
    
    side affects:
        Adds all selected boxes to database

    return:
        None
'''
def check_meetings(sel_times):
    query_allow_update ="SET SQL_SAFE_UPDATES = 0;"
    query_disallow_update ="SET SQL_SAFE_UPDATES = 1;"
    conn =  mysql.connect()
    cur = conn.cursor()
    cur.execute(query_allow_update)
    print("\n\n\n sel_time = {}".format(sel_times))
    for meeting in sel_times:
        dt_id, name, meeting_date, start_time, end_time = meeting.split(",")
        query_string="update response set checked=1 where dt_id={} and start_time='{}' and end_time='{}' and group_leader_id = (select  group_leader_id from group_leader where group_name='{}' limit 1) and meeting_date='{}';".format(dt_id, start_time, end_time, name, meeting_date)
        print(query_string); 
        cur.execute(query_string)
        conn.commit()

    cur = conn.cursor()
    cur.execute(query_disallow_update)
    conn.close()



'''
Mysql helper: used delete all of a contacts responses to a specific meeting
------------------------------------------------------------------------------------------------------------
    arguments:
        group_leader_id: unique id for the leader whos responses are being entered
        meeting_id: unique id for meeting the user has responded to
        available times: an array of data time objects, that represents when this contact can meet and is to
                          be inserted into the database.
    
    side affects:
        Deletes all entires for the specified contact from the resonse table for the specified meeting.

    return:
        None
'''

def delete_prevous_response(available_times, meeting_id, group_leader_id):
    query_allow_update ="SET SQL_SAFE_UPDATES = 0;"
    query_disallow_update ="SET SQL_SAFE_UPDATES = 1;"
    conn =  mysql.connect()
    cur = conn.cursor()
    cur.execute(query_allow_update)
    for d in available_times:
        cur = conn.cursor()
        year, day, month, stime, etime = d.split("-")
        m_date = '{}-{}-{}'.format(year,day,month)
        #print("date {} stime {} etime{}".format(m_date, stime, etime))
        dt_id = get_dt_id(meeting_id,m_date)
        if(not dt_id):
            conn.close()
            return
        query_string = "delete from response Where group_leader_id={}  and dt_id={};".format(group_leader_id, dt_id)
        cur.execute(query_string)
        conn.commit()

    cur = conn.cursor()
    cur.execute(query_disallow_update)
    conn.close()
    

'''
Mysql helper: used to all users responses of availability into the database
------------------------------------------------------------------------------------------------------------
    arguments:
        group_leader_id: unique id for the leader who's responses are being entered
        meeting_id: unique id for meeting the user has responded to
        available times: an array of data time objects, that represents when this contact can meet and is to
                          be inserted into the database.
    
    side affects:
        Adds all contacts available times to the database

    return:
        None
'''
def insert_user_response(group_leader_id, meeting_id, available_times):
    conn =  mysql.connect()
    delete_prevous_response(available_times, meeting_id, group_leader_id)
    try:
        for a in available_times:
            year, day, month, stime, etime = a.split("-")
            m_date = '{}-{}-{}'.format(year,day,month)
            print("\n\nm_date {}| stime ={} | etime={}".format(m_date, stime, etime))
            #print("date {} stime {} etime{}".format(m_date, stime, etime))
            dt_id = get_dt_id(meeting_id,m_date)
            query_string = "insert into response (dt_id, start_time, end_time, group_leader_id, checked, meeting_date) values ({},'{}','{}',{}, 0, '{}');".format(dt_id, stime, etime, group_leader_id, m_date)
            #print("query string = {}".format(query_string))
            cur = conn.cursor()
            try:
                print("\n\n queyr = {}".format(query_string))
                cur.execute(query_string)
                cur_meeting_id = cur.lastrowid
                conn.commit()
            except:
                print("caught error")


    finally:
        conn.close()


'''
Mysql helper: function that gets all the upcoming meetings
------------------------------------------------------------------------------------------------------------
    arguments:
        None
    
    side affects:
        Populates the array(meetings) which used to populate the upcoming meetings table on the home page

    return:
        None
'''

def get_upcoming_meetings():
    query_string ="select * from dates_times join meetings using(meeting_id) where meeting_date >= cast(now() as date) group by (meeting_id);"
    global meetings 
    meetings=[]
    conn =  mysql.connect()
    cur = conn.cursor()
    cur.execute(query_string)
    rows= cur.fetchall()
    for row in rows:
        if (row[2] != ""): 
            meetings.append((row[9], row[8]))
    conn.close();



'''
Mysql helper: function that gets all the past meetings
------------------------------------------------------------------------------------------------------------
    arguments:
        None
    
    side affects:
        Populates the array(pst_meetings) which used to populate the past meetings table on the home page

    return:
        None
'''
def get_past_meetings():
    query_string ="select * from dates_times join meetings using( meeting_id) where meeting_date < cast(now() as date) group by (meeting_id);"
    global past_meetings 
    past_meetings=[]
    conn =  mysql.connect()
    cur = conn.cursor()
    cur.execute(query_string)
    rows= cur.fetchall()
    for row in rows:
        #print("\n\n row {} \n\n".format(row));
        if (row[2] != ""): 
            past_meetings.append((row[6], row[8]))
    conn.close();


'''
Mysql helper: function that takes a meetings unique uuid_url and converts it to that meetings primary key(meeting_id)
------------------------------------------------------------------------------------------------------------
    arguments:
        meeting_uuid: A meetings unique uuid created url
    
    side affects:
        None

    return:
        cur_meeting_id: An int, the unique primary key id for the corresponding uuid_url
'''
def uuid_to_meeting_id(meeting_uuid):
    query_string = "select meeting_id from meetings where uuid='{}'".format(meeting_uuid)
    conn =  mysql.connect()
    cur = conn.cursor()
    cur.execute(query_string)
    cur_meeting_id = cur.fetchone()
    conn.close()
    return cur_meeting_id[0]


'''
Mysql helper function that gets the list of all contacts who have NOT responded to the meeting request yet.
------------------------------------------------------------------------------------------------------------
    arguments:
        meeting_uuid: A meetings unique uuid created url
    
    side affects:
        None

    return:
        not_respnded: Array of strings, represents the list of 0 or more group leaders who have not responded to the meeting request.
'''
def get_not_responded(meeting_uuid):
    not_responded=[];
    query_string = "Select group_name from respond_meeting join group_leader on(group_id=group_leader_id) where issue_ID={} and group_id not in (select group_leader_id from response where dt_id={});".format(meeting_uuid, meeting_uuid);
    conn =  mysql.connect()
    cur = conn.cursor()
    num_not_respond=0;
    cur.execute(query_string)
    non_respond = cur.fetchall()
    for i in non_respond:
        num_not_respond= num_not_respond + 1
        #print("not resp {}".format(i))
        not_responded.append(i[0])
    conn.close()
    return not_responded 


'''
Mysql helper function that gets the number of all contacts who have NOT responded to the meeting request yet.
------------------------------------------------------------------------------------------------------------
    arguments:
        meeting_uuid: A meetings unique uuid created url
    
    side affects:
        None

    return:
        non_respond: An int, the number of contacts who have not responded yet.
'''
def get_num_non_responded(meeting_uuid):
    not_responded=[];
    query_string = "Select count(*) from respond_meeting join group_leader on(group_id=group_leader_id) where issue_ID={} and group_id not in (select group_leader_id from response where dt_id={});".format(meeting_uuid, meeting_uuid);
    conn =  mysql.connect()
    cur = conn.cursor()
    num_not_respond=0;
    cur.execute(query_string)
    non_respond = cur.fetchone()
    conn.close()
    #print("num not resp={}".format(non_respond[0]));
    return non_respond[0] 


'''
Mysql helper: function that get all the meeting info property for a specific meeting
------------------------------------------------------------------------------------------------------------
    arguments:
        meeting_uuid: A meetings unique uuid created url
    
    side affects:
        None

    return:
        returns a tuple of strings (location, meeting name, description), stores all the info about the requested meeting
'''
def get_meeting_info(meeting_uuid):
    query_string="select location, meeting_name, description from meetings where uuid='{}';".format(meeting_uuid)
    conn =  mysql.connect()
    cur = conn.cursor()
    cur.execute(query_string)
    cur_meeting = cur.fetchone()
    conn.close()
    return (cur_meeting[0], cur_meeting[1], cur_meeting[2])



'''
Mysql helper: function that gets the all the contacts, and their available times, for a meeting specified by meeting_id
-----------------------------------------------------------------------------------------------------------------------
    arguments:
        meeting_uuid: A meetings unique uuid created url
    
    side affects:
        Converts python datetime.timedelta object for start time and end time to a string of form HH:MM

    return:
        resp: an array of tuples (date, start_time, end_time) for each respondent
'''
def get_responded(meeting_id):
    resp={} #list of who's responded
    date_time=[]
    query_string="select meeting_date, start_time, end_time, group_name, checked from (select meeting_date, start_time, end_time, group_name, checked, dt_id from response r join group_leader gl using (group_leader_id)  where dt_id={} order by (start_time)) t2 order by (meeting_date);".format(meeting_id)
    conn =  mysql.connect()
    cur = conn.cursor()
    cur.execute(query_string)
    name=""
    respond = cur.fetchall()
    for i in respond:
        if i[3] in resp: #If the date is already in the dict
            st = str(i[1])
            shour, smin, ssec = st.split(":")
            stime="{}:{}".format(shour, smin)
            print("\n\n\n stime {}\n\n\n".format(stime))
            et = str(i[2])
            ehour, emin, esec = et.split(":")
            etime="{}:{}".format(ehour, emin)
            print("\n\n\netime {}\n\n\n".format(etime))
            resp[i[3]].append((i[0], stime, etime, i[4]));
        else: # if date is not in dict
            st = str(i[1])
            shour, smin, ssec = st.split(":")
            stime="{}:{}".format(shour, smin)
            print("\n\n\n stime {}\n\n\n".format(stime))
            et = str(i[2])
            ehour, emin, esec = et.split(":")
            etime="{}:{}".format(ehour, emin)
            print("\n\n\netime {}\n\n\n".format(etime))
            resp[i[3]] = [(i[0], stime, etime, i[4])];
    conn.close()
    return resp 




'''
Mysql helper: function that gets the email of the user that created the the meeting specified by the unique meeting_uuid
------------------------------------------------------------------------------------------------------------
    arguments:
        meeting_uuid: A meetings unique uuid created url
    
    side affects:
        None

    return:
        email: A string for the email address of the user that created a specific meeting
'''
def get_creator_email(meeting_uuid):
    query_string="select creator_email from meetings where uuid='{}';".format(meeting_uuid)
    conn =  mysql.connect()
    cur = conn.cursor()
    cur.execute(query_string)
    meeting= cur.fetchone()
    conn.close()
    email=meeting[0]
    return email
