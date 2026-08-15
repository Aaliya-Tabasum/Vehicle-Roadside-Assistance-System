from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import mysql.connector as mq
from mysql.connector import Error
from markupsafe import Markup
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from flask import request, jsonify
import math
import re
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

def dbconnection():
    con = mq.connect(host='localhost', database='mech',user='root',password='root')
    return con

@app.route('/')
def home():
    return render_template('index.html', title='home')

@app.route('/loginpage')
def loginpage():
    return render_template('login.html',title='login')

@app.route('/userregisterpage')
def registerpage():
    return render_template('userregister.html',title='register')

@app.route('/addtravelpage')
def addtravelpage():
    return render_template('addtravel.html',title='travel')

@app.route('/service_request')
def service_request():

    conn = dbconnection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
        id,
        name,
        phone,
        carnum,
        bikenum,
        policenum
        FROM users
        WHERE id=%s
    """,(session['uid'],))

    user = cur.fetchone()

    cur.execute("""
        SELECT id,name,sname
        FROM mechanic
        WHERE status='Accepted'
    """)

    mechanics = cur.fetchall()

    conn.close()

    return render_template(
        "service_request.html",
        user=user,
        mechanics=mechanics
    )

@app.route('/forgotpass')
def forgotpass():
    return render_template('forgot.html',title='forgot')

@app.route('/userregister', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']
        address = request.form['address']
        carnum = request.form['carnum']
        bikenum = request.form['bikenum']
        policenum = request.form['policenum']
        
        password = request.form['password']

        if not re.match(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$',
            password
        ):
            flash("Password must contain at least 8 characters, one uppercase letter, one lowercase letter, one number and one special character.")
            return redirect(url_for('registerpage'))

        uploaded_file = request.files['dlimage']
        onlyfilename = ""

        if uploaded_file.filename != "":
            onlyfilename = uploaded_file.filename
            filename = "static/uploads/usersdl/" + onlyfilename
            uploaded_file.save(filename)

        con = dbconnection()
        cursor = con.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        res = cursor.fetchall()

        if res == []:

            cursor.execute("""
                INSERT INTO users
                (
                    name,
                    email,
                    phone,
                    gender,
                    address,
                    carnum,
                    bikenum,
                    policenum,
                    dlimage,
                    pass
                )
                VALUES
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                name,
                email,
                phone,
                gender,
                address,
                carnum,
                bikenum,
                policenum,
                onlyfilename,
                password
            ))
            con.commit()
            con.close()

            flash("Registration Success")
            return redirect(url_for('loginpage'))
        else:
            con.close()
            flash("Email already exists")
            return redirect(url_for('registerpage'))

@app.route('/mechregisterpage')
def mechregisterpage():
    return render_template('mechregister.html',title='register')

@app.route('/mechregister', methods=['GET', 'POST'])
def mechregister():

    if request.method == 'POST':

        name = request.form['name']
        phone = request.form['phone']
        sname = request.form['sname']
        saddress = request.form['saddress']
        altphone = request.form['altphone']
        
        password = request.form['password']

        # Password validation
        if not re.match(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$',
            password
        ):
            flash("Password must contain at least 8 characters, one uppercase letter, one lowercase letter, one number and one special character.")
            return redirect(url_for('mechregisterpage'))

        status = "Pending"

        # Upload mechanic image
        uploaded_file1 = request.files['mimage']
        onlyfilename1 = ""

        if uploaded_file1.filename != "":
            onlyfilename1 = uploaded_file1.filename
            filename = "static/uploads/mechimage/" + onlyfilename1
            uploaded_file1.save(filename)

        # Upload certificate
        uploaded_file2 = request.files['certi']
        onlyfilename2 = ""

        if uploaded_file2.filename != "":
            onlyfilename2 = uploaded_file2.filename
            filename = "static/uploads/certificates/" + onlyfilename2
            uploaded_file2.save(filename)

        con = dbconnection()
        cursor = con.cursor()

        cursor.execute(
            "SELECT * FROM mechanic WHERE phone=%s",
            (phone,)
        )

        res = cursor.fetchall()

        if res == []:

            cursor.execute("""
                INSERT INTO mechanic
                (
                    name,
                    phone,
                    sname,
                    saddress,
                    altphone,
                    mimage,
                    certi,
                    pass,
                    status
                )
                VALUES
                (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                name,
                phone,
                sname,
                saddress,
                altphone,
                onlyfilename1,
                onlyfilename2,
                password,
                status
            ))

            con.commit()
            con.close()

            flash("Registration Success")
            return redirect(url_for('loginpage'))

        else:

            con.close()

            flash("Mechanic Phone Number already exists")
            return redirect(url_for('mechregisterpage'))
        
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        ltype = request.form['ltype']
        if ltype=='admin':
            con = dbconnection()
            cursor = con.cursor()
            cursor.execute("select * from admin where email='{}' and pass='{}'".format(email,password))
            res = cursor.fetchall()
            if res==[]:
                message = Markup("<h3>Failed! Invalid Email or Password</h3>")
                flash(message)
                return redirect(url_for('loginpage'))
            else:
               return redirect(url_for('admindashboard'))
        elif ltype=='mechanic':
            con = dbconnection()
            cursor = con.cursor()
            cursor.execute("select * from mechanic where phone='{}' and pass='{}'".format(email,password))
            res = cursor.fetchall()
            if res==[]:
                message = Markup("<h3>Failed! Invalid Phone number or Password</h3>")
                flash(message)
                return redirect(url_for('loginpage'))
            else:
                session['mid']=res[0][0]
                return redirect(url_for('viewuserrequestspage'))
        elif ltype=='user':
            con = dbconnection()
            cursor = con.cursor()
            cursor.execute("select * from users where email='{}' and pass='{}'".format(email,password))
            res = cursor.fetchall()
            if res==[]:
                message = Markup("<h3>Failed! Invalid Email or Password</h3>")
                flash(message)
                return redirect(url_for('loginpage'))
            else:
                session['uid']=res[0][0]
                return redirect(url_for('addtravelpage'))

@app.route('/aviewmechanicspage')
def aviewmechanicspage():

    con = dbconnection()          # ✅ Correct function name
    cursor = con.cursor()

    cursor.execute("SELECT * FROM mechanic ORDER BY id DESC")

    mechanics = cursor.fetchall()

    print(mechanics)
    print("Total Mechanics:", len(mechanics))

    con.close()

    return render_template(
        "aviewmechanics.html",
        mechanics=mechanics
    )


@app.route('/acceptmech')
def acceptmech():
    id =request.args.get('id')
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute(
    "UPDATE mechanic SET status='Accepted', availability='Available' WHERE id=%s",
    (id,)
)
    con.commit()
    con.close()
    message = Markup("<h3>Success! Mechanic Added</h3>")
    flash(message)
    return redirect(url_for('aviewmechanicspage'))

@app.route('/updatelocationpage')
def updatelocationpage():
    return render_template('updatelocation.html')

@app.route('/updatelocation', methods=['POST'])
def updatelocation():

    data = request.get_json()

    lat = data['lat']
    lon = data['lon']

    mid = session['mid']

    con = dbconnection()
    cursor = con.cursor()

    cursor.execute(
        "UPDATE mechanic SET latitude=%s, longitude=%s WHERE id=%s",
        (lat, lon, mid)
    )

    con.commit()
    con.close()

    return jsonify({
        "message":"Location Updated Successfully"
    })

@app.route('/rejectmech')
def rejectmech():
    id =request.args.get('id')
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("update mechanic set status='{}' where id={}".format("Rejected",int(id)))
    con.commit()
    con.close()
    message = Markup("<h3>Mechanic Rejected</h3>")
    flash(message)
    return redirect(url_for('aviewmechanicspage'))
    
           
@app.route('/savetravel', methods=['GET', 'POST'])
def savetravel():
    if request.method == 'POST':
        source = request.form['source']
        dest = request.form['dest']
        tdate = request.form['tdate']
        ttime = request.form['ttime']
        #current_datetime = datetime.now()
        #current_datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        con = dbconnection()
        cursor = con.cursor()
        cursor.execute("insert into travels(source,dest,tdate,ttime,uid)values('{}','{}','{}','{}',{})".format(source,dest,tdate,ttime,int(session['uid'])))
        con.commit()
        con.close()
        message = Markup("<h3>Success! Details added</h3>")
        flash(message)
        return redirect(url_for('addtravelpage'))

@app.route('/uviewmytravelspage')
def uviewmytravelspage():
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from travels where uid={} order by tdate desc".format(int(session['uid'])))
    res = cursor.fetchall()
    if res==[]:
        message = Markup("<h3>Failed! No Data found</h3>")
        flash(message)
        return render_template('uviewtravels.html', title='travels')
    else:
        return render_template('uviewtravels.html', title='travels',res=res)

@app.route('/uviewmechanicspage')
def uviewmechanicspage():

    travel_id = request.args.get("id", default=None, type=str)
    retry_id = request.args.get("retry", default=None, type=str)

    # Journey request
    if travel_id is not None and travel_id != "" and travel_id != "0":

        session.pop("direct_request", None)

        session["mode"] = "journey"
        session["travel_id"] = int(travel_id)

    # Retry request
    if retry_id is not None and retry_id != "":

        session["retry_request_id"] = int(retry_id)

    con = dbconnection()
    cur = con.cursor()

    cur.execute("""
        SELECT *
        FROM mechanic
        WHERE status='Accepted'
    """)

    res = cur.fetchall()

    con.close()

    return render_template(
        "uviewmechanics.html",
        res=res
    )


@app.route('/feedbackpage')
def feedbackpage():
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from mechanic where status='{}'".format("Accepted"))
    res = cursor.fetchall()
    if res==[]:
        message = Markup("<h3>Failed! No Mechanics found</h3>")
        flash(message)
        return render_template('ugivefeedback.html', title='mechanics')
    else:
        return render_template('ugivefeedback.html', title='mechanics',res=res)

@app.route('/savefeedback', methods=['GET', 'POST'])
def savefeedback():
    if request.method == 'POST':
        mid = request.form['mid']
        star = request.form['star']
        print(star)
        description = request.form['description']
        con = dbconnection()
        cursor = con.cursor()
        cursor.execute("select * from feedbacks where mid={} and uid={}".format(int(mid),int(session['uid'])))
        res = cursor.fetchall()
        if res==[]:
            cursor.execute("insert into feedbacks(rating,description,uid,mid)values('{}','{}',{},{})".format(int(star),description,int(session['uid']),int(mid)))
            con.commit()
            con.close()
            message = Markup("<h3>Success! Feedback sent</h3>")
            flash(message)
            return redirect(url_for('feedbackpage'))
        else:
            message = Markup("<h3>Feedback already given to this Mechanic</h3>")
            flash(message)
            return redirect(url_for('feedbackpage'))
        
@app.route('/mechanics', methods=['POST'])
def mechanics():
    # Get the search query parameter from the request
    search_query  = request.json.get('searchTerm')

    # Connect to the MySQL database
    connection = dbconnection()
    cursor = connection.cursor()

    # Query to fetch mechanics' data based on the search query
    query = """
SELECT
name,
phone,
sname,
saddress,
altphone,
haddress,
id,
availability
FROM mechanic
WHERE saddress LIKE %s
AND status=%s
"""
    cursor.execute(query, ('%' + search_query + '%',"Accepted"))
    mechanics_data = cursor.fetchall()

    # Close the database connection
    cursor.close()
    connection.close()

    # Render the template with the filtered mechanics' data
    return jsonify(mechanics_data)

@app.route('/viewmechprofile')
def viewmechprofile():
    id =request.args.get('id')
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from mechanic where id={}".format(int(id)))
    res = cursor.fetchall()
    return render_template('uviewmechanicprofile.html', title='mechanics',res=res)

@app.route('/myrequests')
def myrequests():

    uid = session['uid']
    print("Logged in user id:", uid)

    con = dbconnection()
    cursor = con.cursor()

    cursor.execute("""
SELECT

a.id,
a.uid,
a.mid,
a.tid,
a.status,
a.vehicle,
a.problem,
a.location,
a.model,
a.ptype,

t.source,
t.dest,
t.tdate,
t.ttime,

m.name,
m.phone,
m.sname,
m.saddress,
m.altphone,
m.latitude,
m.longitude,
u.name

FROM assirequests a

LEFT JOIN travels t
ON a.tid=t.id

INNER JOIN mechanic m
ON a.mid=m.id

INNER JOIN users u
ON a.uid=u.id

WHERE a.uid=%s

ORDER BY a.id DESC

""", (uid,))
    res = cursor.fetchall()
    print(res)

    return render_template("myrequests.html",res=res)

@app.route('/requestagain/<int:reqid>')
def requestagain(reqid):
    session['retry_request_id']=reqid
    return redirect(url_for('uviewmechanicspage',retry=reqid))



@app.route('/reqassi')
def reqassi():
    mid=request.args.get('id')
    uid=session['uid']

    con=dbconnection()
    cur=con.cursor()

    retry=session.pop('retry_request_id',None)

    if retry:
        cur.execute("""
        SELECT tid,vehicle,problem,location,model,ptype
        FROM assirequests
        WHERE id=%s
        """,(retry,))
        old=cur.fetchone()

        if old[0] is None:
            cur.execute("""
            INSERT INTO assirequests
            (uid,mid,tid,status,vehicle,problem,location,model,ptype)
            VALUES(%s,%s,NULL,'Pending',%s,%s,%s,%s,%s)
            """,(uid,mid,old[1],old[2],old[3],old[4],old[5]))
        else:
            cur.execute("""
            INSERT INTO assirequests
            (uid,mid,tid,status)
            VALUES(%s,%s,%s,'Pending')
            """,(uid,mid,old[0]))

    elif 'direct_request' in session:
        d=session.pop('direct_request')
        cur.execute("""
        INSERT INTO assirequests
        (uid,mid,tid,status,vehicle,problem,location,model,ptype)
        VALUES(%s,%s,NULL,'Pending',%s,%s,%s,%s,%s)
        """,(uid,mid,d['vehicle'],d['problem'],d['location'],d['model'],d['ptype']))
    else:
        tid=session.get('travel_id')
        if not tid:
            flash('Travel not found')
            return redirect(url_for('uviewmytravelspage'))
        cur.execute("""
        INSERT INTO assirequests(uid,mid,tid,status)
        VALUES(%s,%s,%s,'Pending')
        """,(uid,mid,tid))

    con.commit()
    session.pop("travel_id", None)
    session.pop("direct_request", None)
    session.pop("retry_request_id", None)
    session.pop("mode", None)
    con.close()
    flash('Request Raised Successfully')
    return redirect(url_for('myrequests'))

@app.route('/savedirectrequest', methods=['POST'])
def savedirectrequest():

    # Remove old journey data
    session.pop("travel_id", None)
    session.pop("mode", None)
    session.pop("retry_request_id", None)

    session['direct_request'] = {
        "vehicle": request.form['vehicle'],
        "model": request.form['model'],
        "ptype": request.form['ptype'],
        "problem": request.form['problem'],
        "location": request.form['location'],
        "latitude": request.form['latitude'],
        "longitude": request.form['longitude']
    }

    return redirect(url_for("uviewmechanicspage"))

@app.route('/viewuserrequestspage')
def viewuserrequestspage():
    mid = session['mid']
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("""
SELECT

a.id,
a.uid,
a.mid,
a.tid,
a.status,
a.vehicle,
a.problem,
a.location,

t.source,
t.dest,
t.tdate,
t.ttime,

u.name,
u.email,
u.phone,
u.carnum,
u.bikenum

FROM assirequests a

LEFT JOIN travels t
ON a.tid = t.id

INNER JOIN users u
ON a.uid = u.id

WHERE a.mid=%s

ORDER BY a.id DESC

""", (mid,))
    res = cursor.fetchall()
    return render_template('mviewrequests.html', title='requests',res=res)

@app.route('/acceptassi')
def acceptassi():
    id =request.args.get('id')
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute(
"update assirequests set status='Accepted' where id={}"
.format(int(id)))

    cursor.execute("""
UPDATE mechanic
SET availability='Busy'
WHERE id=%s
""", (session['mid'],))
    con.commit()
    con.close()
    message = Markup("<h3>Job Accepted</h3>")
    flash(message)
    return redirect(url_for('viewuserrequestspage'))

@app.route('/rejectassi')
def rejectassi():
    id =request.args.get('id')
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("update assirequests set status='{}' where id={}".format("Rejected",int(id)))
    con.commit()
    con.close()
    message = Markup("<h3>Job Rejected</h3>")
    flash(message)
    return redirect(url_for('viewuserrequestspage'))

@app.route('/completedassi')
def completedassi():
    id =request.args.get('id')
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute(
"update assirequests set status='Completed' where id={}"
.format(int(id)))

    cursor.execute("""
UPDATE mechanic
SET availability='Available'
WHERE id=%s
""", (session['mid'],))
    con.commit()
    con.close()
    message = Markup("<h3>Job Completed</h3>")
    flash(message)
    return redirect(url_for('viewuserrequestspage'))

@app.route('/allfeedbacks')
def allfeedbacks():
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from feedbacks left join users on feedbacks.uid=users.id left join mechanic on feedbacks.mid=mechanic.id order by feedbacks.id desc")
    res = cursor.fetchall()
    return render_template('allfeedbacks.html', title='feedbacks',res=res)

@app.route('/getmypass', methods=['GET', 'POST'])
def getmypass():
    if request.method == 'POST':
        ltype = request.form['ltype']
        email = request.form['email']
        if ltype=='admin':
            con = dbconnection()
            cursor = con.cursor()
            cursor.execute("select * from admin where email='{}'".format(email))
            res = cursor.fetchall()
            if res==[]:
                message = Markup("<h3>Failed! Invalid Email</h3>")
                flash(message)
            else:
                message = Markup("<h3>YOUR PASSWORD IS : </h3>"+res[0][2])
                flash(message)
                return redirect(url_for('forgotpass'))
        elif ltype=='mechanic':
            con = dbconnection()
            cursor = con.cursor()
            cursor.execute("select * from mechanic where phone='{}'".format(email))
            res = cursor.fetchall()
            if res==[]:
                message = Markup("<h3>Failed! Invalid Phone number</h3>")
                flash(message)
                return redirect(url_for('forgotpass'))
            else:
                message = Markup("<h3>YOUR PASSWORD IS : </h3>"+res[0][9])
                flash(message)
                return redirect(url_for('forgotpass'))
        elif ltype=='user':
            con = dbconnection()
            cursor = con.cursor()
            cursor.execute("select * from users where email='{}'".format(email))
            res = cursor.fetchall()
            if res==[]:
                message = Markup("<h3>Failed! Invalid Email</h3>")
                flash(message)
                return redirect(url_for('forgotpass'))
            else:
                message = Markup("<h3>YOUR PASSWORD IS : </h3>"+res[0][11])
                flash(message)
                return redirect(url_for('forgotpass'))
            
@app.route('/emergency')
def emergency():

    con = dbconnection()

    cursor = con.cursor()

    cursor.execute("""

        SELECT
        service_name,
        contact_number,
        description

        FROM emergency_contacts

        WHERE status='Active'

        ORDER BY id

    """)

    contacts = cursor.fetchall()

    con.close()

    return render_template(
        "emergency.html",
        contacts=contacts
    )

@app.route('/adminemergencypage')
def adminemergencypage():

    con = dbconnection()
    cursor = con.cursor()

    cursor.execute("""
        SELECT *
        FROM emergency_contacts
        ORDER BY id DESC
    """)

    contacts = cursor.fetchall()

    con.close()

    return render_template(
        "admin_emergency.html",
        contacts=contacts
    )

@app.route('/saveemergency', methods=['POST'])
def saveemergency():

    service_name = request.form['service_name']
    contact_number = request.form['contact_number']
    description = request.form['description']
    status = request.form['status']

    con = dbconnection()
    cursor = con.cursor()

    cursor.execute("""
        INSERT INTO emergency_contacts
        (
            service_name,
            contact_number,
            description,
            status
        )

        VALUES(%s,%s,%s,%s)

    """,
    (
        service_name,
        contact_number,
        description,
        status
    ))

    con.commit()
    con.close()

    #flash("Emergency Contact Added Successfully", "emergency")

    return redirect(url_for("adminemergencypage"))

@app.route('/deleteemergency')
def deleteemergency():

    id = request.args.get("id")

    con = dbconnection()
    cursor = con.cursor()

    cursor.execute(
        "DELETE FROM emergency_contacts WHERE id=%s",
        (id,)
    )

    con.commit()
    con.close()

    #flash("Emergency Contact Deleted Successfully", "emergency")

    return redirect(url_for("adminemergencypage"))


@app.route("/addtroubleshootpage")
def addtroubleshootpage():
    return render_template("add_troubleshoot.html")

@app.route("/viewtroubleshoot")
def viewtroubleshoot():

    conn = dbconnection()

    cur = conn.cursor()

    cur.execute("SELECT * FROM troubleshoot")

    res = cur.fetchall()

    conn.close()

    return render_template("view_troubleshoot.html",
                           res=res)

@app.route("/deletetroubleshoot")
def deletetroubleshoot():

    id = request.args.get("id")

    conn = dbconnection()

    cur = conn.cursor()

    cur.execute("DELETE FROM troubleshoot WHERE id=%s", (id,))

    conn.commit()

    conn.close()

    flash("Solution Deleted Successfully")

    return redirect("viewtroubleshoot")

@app.route("/savetroubleshoot", methods=["POST"])
def savetroubleshoot():

    vehicle_type = request.form["vehicle_type"]
    category = request.form["category"]
    problem = request.form["problem"]
    solution = request.form["solution"]
    tools_required = request.form["tools_required"]
    difficulty = request.form["difficulty"]
    warning = request.form["warning"]

    conn = dbconnection()

    cur = conn.cursor()

    cur.execute("""
        INSERT INTO troubleshoot
        (vehicle_type, category, problem, solution, tools_required, difficulty, warning)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (
        vehicle_type,
        category,
        problem,
        solution,
        tools_required,
        difficulty,
        warning
    ))

    conn.commit()
    conn.close()

    #flash("Troubleshoot solution added successfully!", "troubleshoot")

    return redirect("/viewtroubleshoot")

@app.route("/selftroubleshoot")
def selftroubleshoot():

    conn = dbconnection()

    cur = conn.cursor()

    cur.execute("SELECT * FROM troubleshoot ORDER BY vehicle_type, category")

    res = cur.fetchall()

    conn.close()

    return render_template("self_troubleshoot.html", res=res)

@app.route('/aviewuserspage')
def aviewuserspage():

    con = dbconnection()
    cursor = con.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        ORDER BY id DESC
    """)

    res = cursor.fetchall()

    return render_template("aviewusers.html", users=res)


@app.route('/deleteuser')
def deleteuser():

    id = request.args.get('id')

    con = dbconnection()
    cursor = con.cursor()

    # Delete feedback
    cursor.execute(
        "DELETE FROM feedbacks WHERE uid=%s",
        (id,)
    )

    # Delete assistance requests
    cursor.execute(
        "DELETE FROM assirequests WHERE uid=%s",
        (id,)
    )

    # Delete travel records
    cursor.execute(
        "DELETE FROM travels WHERE uid=%s",
        (id,)
    )

    # Delete direct service requests
    cursor.execute(
        "DELETE FROM direct_service_requests WHERE user_id=%s",
        (id,)
    )

    # Finally delete user
    cursor.execute(
        "DELETE FROM users WHERE id=%s",
        (id,)
    )

    con.commit()

    cursor.close()
    con.close()

    flash("User deleted successfully!")

    return redirect(url_for('aviewuserspage'))


@app.route('/aviewrequestspage')
def aviewrequestspage():

    con = dbconnection()
    cursor = con.cursor()

    cursor.execute("""

    SELECT

    a.id,
    a.status,
    a.vehicle,
    a.problem,
    a.location,
    a.model,
    a.ptype,

    u.name,
    u.phone,

    m.name,
    m.phone,

    t.source,
    t.dest,
    t.tdate,
    t.ttime

    FROM assirequests a

    LEFT JOIN users u
    ON a.uid=u.id

    LEFT JOIN mechanic m
    ON a.mid=m.id

    LEFT JOIN travels t
    ON a.tid=t.id

    ORDER BY a.id DESC

    """)

    res = cursor.fetchall()

    return render_template("aviewrequests.html", requests=res)

@app.route('/viewfeedbackpage')
def viewfeedbackpage():

    con = dbconnection()
    cursor = con.cursor()

    cursor.execute("""

    SELECT

    f.id,
    f.rating,
    f.description,

    u.name,
    u.email,

    m.name,
    m.sname

    FROM feedbacks f

    INNER JOIN users u
    ON f.uid=u.id

    INNER JOIN mechanic m
    ON f.mid=m.id

    ORDER BY f.id DESC

    """)

    res = cursor.fetchall()

    return render_template("viewfeedback.html", feedbacks=res)

@app.route('/admindashboard')
def admindashboard():

    con = dbconnection()
    cursor = con.cursor()

    # Dashboard Counts
    cursor.execute("SELECT COUNT(*) FROM users")
    users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM mechanic")
    mechanics = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM assirequests")
    requests = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM feedbacks")
    feedbacks = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM assirequests WHERE status='Pending'")
    pending = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM assirequests WHERE status='Accepted'")
    accepted = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM assirequests WHERE status='Completed'")
    completed = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM assirequests WHERE status='Rejected'")
    rejected = cursor.fetchone()[0]

    # Latest 5 Requests
    cursor.execute("""

    SELECT

    u.name,
    m.name,
    a.vehicle,
    a.problem,
    a.status

    FROM assirequests a

    JOIN users u
    ON a.uid=u.id

    JOIN mechanic m
    ON a.mid=m.id

    ORDER BY a.id DESC

    LIMIT 5

    """)

    latest_requests = cursor.fetchall()

    con.close()

    return render_template(
        "admindashboard.html",
        users=users,
        mechanics=mechanics,
        requests=requests,
        feedbacks=feedbacks,
        pending=pending,
        accepted=accepted,
        completed=completed,
        rejected=rejected,
        latest_requests=latest_requests
    )

@app.route('/mechprofilepage')
def mechprofilepage():

    con = dbconnection()
    cursor = con.cursor()

    cursor.execute("""
        SELECT *
        FROM mechanic
        WHERE id=%s
    """,(session['mid'],))

    mech = cursor.fetchone()

    con.close()

    return render_template(
        "mechprofile.html",
        mech=mech
    )

@app.route('/editmechanicpage')
def editmechanicpage():

    con = dbconnection()
    cursor = con.cursor()

    cursor.execute(
        "SELECT * FROM mechanic WHERE id=%s",
        (session['mid'],)
    )

    mech = cursor.fetchone()

    con.close()

    return render_template(
        "editmechanic.html",
        mech=mech
    )

@app.route('/updatemechanic', methods=['POST'])
def updatemechanic():

    name = request.form['name']
    phone = request.form['phone']
    password = request.form['pass']
    sname = request.form['sname']
    saddress = request.form['saddress']
    altphone = request.form['altphone']
    

    con = dbconnection()
    cursor = con.cursor()

    cursor.execute("""
    UPDATE mechanic
    SET
        name=%s,
        phone=%s,
        pass=%s,
        sname=%s,
        saddress=%s,
        altphone=%s
    WHERE id=%s
""",
(
    name,
    phone,
    password,
    sname,
    saddress,
    altphone,
    session['mid']
))

    con.commit()
    con.close()

    flash("Profile Updated Successfully","success")

    return redirect(url_for("mechprofilepage"))

@app.route('/deletemechanic')
def deletemechanic():

    con=dbconnection()

    cursor=con.cursor()

    cursor.execute(
        "DELETE FROM mechanic WHERE id=%s",
        (session['mid'],)
    )

    con.commit()

    con.close()

    session.clear()

    #flash("Account Deleted Successfully")

    return redirect(url_for("home"))

@app.route('/editemergencypage')
def editemergencypage():

    id = request.args.get("id")

    con = dbconnection()
    cursor = con.cursor()

    cursor.execute(
        "SELECT * FROM emergency_contacts WHERE id=%s",
        (id,)
    )

    contact = cursor.fetchone()

    con.close()

    return render_template(
        "edit_emergency.html",
        contact=contact
    )

@app.route('/updateemergency', methods=['POST'])
def updateemergency():

    id = request.form["id"]
    service_name = request.form["service_name"]
    contact_number = request.form["contact_number"]
    description = request.form["description"]
    status = request.form["status"]

    con = dbconnection()
    cursor = con.cursor()

    cursor.execute("""
        UPDATE emergency_contacts
        SET
            service_name=%s,
            contact_number=%s,
            description=%s,
            status=%s
        WHERE id=%s
    """,
    (
        service_name,
        contact_number,
        description,
        status,
        id
    ))

    con.commit()
    con.close()

    #flash("Emergency Contact Updated Successfully", "emergency")

    return redirect(url_for("adminemergencypage"))

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
