from flask import Flask, redirect, url_for, render_template, request, flash,session
import os
from db_init import initialize
from psycopg2 import extensions
from forms import RegistrationForm, LoginForm

import queries

adds = []

extensions.register_type(extensions.UNICODE)
extensions.register_type(extensions.UNICODEARRAY)

app = Flask (__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'




HEROKU = True

if(not HEROKU):
    os.environ['DATABASE_URL'] = "dbname='postgres' user='postgres' host='localhost' password='1234'"
    initialize(os.environ.get("DATABASE_URL"))


@app.route("/appointment/<id>",methods = ["GET","POST"])
def appointment_page(id=0,type=0):
    active = queries.run("""SELECT current_user""")
    if active[0][0] == None:
        active.pop(0)
    active_num = (len(active))
    psychologistt = queries.select("name","psychologist",asDict = True)
    patientt = queries.select("name","patient",asDict = True)
    total_user = len(psychologistt) + len(patientt)
    print("W"*30)
    print(list(request.form.items()))
    psychologist = queries.select("id,name,mail","psychologist",asDict=True)
    if(request.method == "GET"):
        return render_template("appointment.html",session_id = (session["id"]),session_type = session["type"],active_num = active_num,total_user=total_user,psychologist = psychologist,id=id)

    psychologist = queries.select("id,name","psychologist",asDict=True)
    print("?-"*26)
    print("request:",dict(list(request.form.items())))
    requests = dict(list(request.form.items()))
    psy = queries.select("id","psychologist","mail = '{}'".format(requests["mail"]),asDict=True)
    print(psy)
    queries.insert("appointment","psychologist_id,patient_id,day,time","{},{},{},{}".format(psy["id"],session["id"],requests["day"],requests["time"]))
    return render_template("appointment.html",session_id = (session["id"]),session_type = session["type"],active_num = active_num,total_user=total_user,psychologist = psychologist,id=id)


@app.route("/patient_page/<id>",methods = ["GET","POST"])
def patient_page(id):
    active = queries.run("""SELECT current_user""")
    if active[0][0] == None:
        active.pop(0)
    active_num = (len(active))
    psychologistt = queries.select("name","psychologist",asDict = True)
    patientt = queries.select("name","patient",asDict = True)
    total_user = len(psychologistt) + len(patientt)
    if(request.method == "POST"):
        requests = dict(list(request.form.items()))
        delete_one = list(requests.keys())[0]
        queries.delete("appointment","appointment.id={}".format(delete_one))
    patients = queries.select("id,name,mail","patient","id={}".format(id),asDict=True)
    appointments = queries.select("id,day,time,patient_id,psychologist_id","appointment","appointment.patient_id={}".format(id),asDict = True)
    psychologist = queries.select("id,name","psychologist",asDict=True)
    
    if isinstance(appointments,dict):
        appointments = [appointments]
    return render_template("patient_page.html",active_num = active_num,total_user=total_user,psychologist = psychologist, appointments = appointments,patients = patients,asDict = True,page_id = int(id), session_id = (session["id"]),session_type = session["type"])


@app.route("/")
def home_page():
    active = queries.run("""SELECT current_user""")
    if active[0][0] == None:
        active.pop(0)
    active_num = (len(active))
    psychologistt = queries.select("name","psychologist",asDict = True)
    patientt = queries.select("name","patient",asDict = True)
    total_user = len(psychologistt) + len(patientt)
    print(session)
    sql = "SELECT appointment.id, appointment.day,appointment.time, patient.name,psychologist.name,psychologist.id FROM patient INNER JOIN appointment ON patient.id = appointment.patient_id INNER JOIN psychologist ON appointment.psychologist_id = psychologist.id;"
    joined = queries.run(sql)
    print("\|/"*15)
    print(joined)
    appointment = queries.select("id,psychologist_id,patient_id,day,time","appointment",asDict = True)
    patients = queries.select("name,id","patient",asDict=True)
    psychologist = queries.select("id,name","psychologist",asDict=True)

    return render_template("home_page.html",session_id = (session["id"]),session_type = session["type"],joined = joined,active_num = active_num,total_user=total_user,id = 10, appointment = appointment,patients = patients,psychologist=psychologist)


@app.route("/psychologist_page/<id>",methods = ["GET","POST"])
def psychologist_page(id):
    print("AA"*23,request.form)
    global adds
    active = queries.run("""SELECT current_user""")
    if active[0][0] == None:
        active.pop(0)
    active_num = (len(active))
    psychologistt = queries.select("name","psychologist",asDict = True)
    patientt = queries.select("name","patient",asDict = True)
    total_user = len(psychologistt) + len(patientt)
    if(request.method == "POST"):
        if("comment" in request.form):
            requests = dict(list(request.form.items()))
            queries.insert("comment","patient_id,psychologist_id,comment","'{}','{}','{}'".format(session["id"],id,requests["comment_content"]))
        elif("point" in request.form):
            requests = dict(list(request.form.items()))
            selected = queries.select("id","point","patient_id = {} AND psychologist_id = {}".format(session["id"],id))
            print("SEEEELELLLLLLLEEEECCCCCTTEEEEEDDDDDDDD")
            print(selected)
            if(len(selected) == 0):
                queries.insert("point","point,patient_id,psychologist_id","'{}','{}','{}'".format(requests["point"],session["id"],id))
            else:
                print("UPDATINGGGGG")
                queries.update("point","point = {}".format(requests["point"]),"patient_id = {} AND psychologist_id = {}".format(session["id"],id))
        elif("give_Add" in request.form):
            adds.append(id)
        elif(list(request.form.items())[0][1]=="delete"):
            com_id = list(request.form.items())[0][0]
            queries.delete("comment","comment.id = {}".format(com_id))
        elif("Cancel" in list(request.form.items())[0]):
            requests = dict(list(request.form.items()))
            delete_one = list(requests.keys())[0]
            queries.delete("appointment","appointment.id={}".format(delete_one))    
        else:
            print("HA"*30,list(request.form.items()))
            queries.update("comment","comment = '{}'".format(list(request.form.items())[0][1]),"id = {}".format(list(request.form.items())[1][0]) )
            queries.update("comment","comment = '{}'".format(list(request.form.items())[1][1]),"id = {}".format(list(request.form.items())[0][0]) )
        
    psychologist = queries.select("id,name,mail,address","psychologist","id={}".format(id),asDict=True)
    point = queries.select("point","point","psychologist_id = {}".format(id),asDict = False)
    sum_ = 0
    for i in range(len(point)):
        sum_ += point[i][0]
    if(len(point) != 0):
        sum_ = sum_/float(len(point))
    point = sum_
    appointments = queries.select("id,day,time,patient_id,psychologist_id","appointment","appointment.psychologist_id={}".format(id),asDict = True)
    patients = queries.select("name,id","patient",asDict=True)
    if isinstance(appointments,dict):
        appointments = [appointments]
    comments = queries.select("id,patient_id,psychologist_id,comment","comment","comment.psychologist_id = {}".format(psychologist["id"]),asDict = True)
    if isinstance(comments,dict):
        comments = [comments]
    sql = "SELECT appointment.id, appointment.day,appointment.time, patient.name,psychologist.name,psychologist.id FROM patient INNER JOIN appointment ON patient.id = appointment.patient_id INNER JOIN psychologist ON appointment.psychologist_id = psychologist.id WHERE psychologist.id = {};".format(id)
    joined = queries.run(sql)
    return render_template("psychologist_page.html",joined = joined,active_num = active_num,total_user=total_user,point = point, comments=comments,psychologist = psychologist, appointments = appointments,patients = patients, session_id = session["id"],session_type = session["type"],asDict = True)

@app.route("/psychologist_page_all")
def psychologist_page_all():
    global adds
    active = queries.run("""SELECT current_user""")
    if active[0][0] == None:
        active.pop(0)
    active_num = (len(active))
    psychologistt = queries.select("name","psychologist",asDict = True)
    patientt = queries.select("name","patient",asDict = True)
    total_user = len(psychologistt) + len(patientt)
    psys = queries.select("id,name,mail, address","psychologist",asDict = True)
    point_id_dict = {}
    for psy in psys:
        point = queries.select("point","point","psychologist_id = {}".format(psy["id"]),asDict = False)
        sum_ = 0
        for i in range(len(point)):
            sum_ += point[i][0]
        if(len(point) != 0):
            sum_ = sum_ /float(len(point))
        point_id_dict[psy["id"]] = sum_
    print("||||"*20)
    print (point_id_dict)

    for psy in psys:
        psy["point"] = point_id_dict[psy["id"]]
    print(psys)
    psys = sorted(psys, key=lambda k: k['point'],reverse = True) 
    print(psys)
    for i in range(0, len(adds)): 
        adds[i] = int(adds[i]) 
    for i in range(len(psys)):
        if(psys[-i]["id"] in adds):
            temp = psys[-i]
            psys.pop(-i)
            psys.insert(0,temp)
    print(psys)

    return render_template("psychologist_page_all.html",session_id = (session["id"]),session_type = session["type"],active_num = active_num,psys = psys, point_id_dict = point_id_dict,total_user=total_user)

@app.route("/login",methods = ["GET","POST"])
def login_page():
    active = queries.run("""SELECT current_user""")
    if active[0][0] == None:
        active.pop(0)
    active_num = (len(active))
    psychologistt = queries.select("name","psychologist",asDict = True)
    patientt = queries.select("name","patient",asDict = True)
    total_user = len(psychologistt) + len(patientt)
    form = LoginForm()
    session["id"] = None
    session["type"] = None

    if form.validate_on_submit():
        user = queries.select("id,name,mail,password", "patient", where="mail = '{}'".format(form.mail.data),asDict = True)
        if(user):
            if(user["mail"] == form.mail.data and user["password"] == form.password.data):
                session["id"] = user["id"]
                session["name"] = user["name"]
                session["type"] = "patient"
                session["address"] = "NULL"
                session["mail"] = user["mail"]
                return redirect(url_for('patient_page',id = user["id"]))
        user = queries.select("id,name,mail,address,password", "psychologist", where="mail = '{}'".format(form.mail.data),asDict = True)
        if(len(user) != 0):
            if(user["mail"] == form.mail.data and user["password"] == form.password.data):
                session["id"] = user["id"]
                session["type"] = "psychologist"
                session["name"] = user["name"]
                session["mail"] = user["mail"]
                session["address"] = user["address"]
                return redirect(url_for('psychologist_page',id=user["id"]))
        flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html',session_id = (session["id"]),session_type = session["type"],active_num = active_num, title='Login', form=form,total_user=total_user)


@app.route('/forgot_page', methods=['GET', 'POST'])
def forgot_page():
    active = queries.run("""SELECT current_user""")
    if active[0][0] == None:
        active.pop(0)
    form = LoginForm()
    
    active_num = (len(active))
    psychologistt = queries.select("name","psychologist",asDict = True)
    patientt = queries.select("name","patient",asDict = True)
    total_user = len(psychologistt) + len(patientt)
    
    if form.validate_on_submit():
        queries.update("patient", "password = {}".format(form.password.data), where="mail = '{}'".format(form.mail.data))

    return render_template('forgot_page.html',session_id = (session["id"]),session_type = session["type"],form = form,active_num = active_num,total_user=total_user)



@app.route('/sign_out')
def sign_out():
    active = queries.run("""SELECT current_user""")
    if active[0][0] == None:
        active.pop(0)
    active_num = (len(active))
    psychologistt = queries.select("name","psychologist",asDict = True)
    patientt = queries.select("name","patient",asDict = True)
    total_user = len(psychologistt) + len(patientt)

    session["id"] = None 
    session["name"] = None 
    print("||"*33)
    return redirect(url_for('login_page'))


@app.route('/sign_out_delete')
def sign_out_delete():
    active = queries.run("""SELECT current_user""")
    if active[0][0] == None:
        active.pop(0)
    active_num = (len(active))
    psychologistt = queries.select("name","psychologist",asDict = True)
    patientt = queries.select("name","patient",asDict = True)
    total_user = len(psychologistt) + len(patientt)

    if(session["type"] == "patient"):
        queries.delete("patient","id = {}".format(session["id"]))
    else:
        queries.delete("psychologist","id = {}".format(session["id"]))
    session["id"] = None 
    session["name"] = None 
    return redirect(url_for('login_page'))



@app.route("/register", methods=['GET', 'POST'])
def register():
    active = queries.run("""SELECT current_user""")
    if active[0][0] == None:
        active.pop(0)
    active_num = (len(active))
    psychologistt = queries.select("name","psychologist",asDict = True)
    patientt = queries.select("name","patient",asDict = True)
    total_user = len(psychologistt) + len(patientt)
    form = RegistrationForm()
    if form.validate_on_submit():
        string = 'Account created for ' + form.name.data
        requests = dict(list(request.form.items()))
        print("AB"*30)
        print(requests)
        if requests["user_type"] == "psychologist":
            string = "'{}' , '{}' , '{}', '{}'".format(requests["name"],requests["address"],requests["mail"],requests["password"])
    
            success = queries.insert(requests["user_type"],"name,address,mail,password",string)
            if (success[-1] == -1 ):
                string = "you could not signed up due to " + str(success[0])
                flash(string, "error")
        else:
            string = "'{}' , '{}' , '{}'".format(requests["name"],requests["mail"], requests["password"])
            
            success = queries.insert(requests["user_type"],"name,mail,password",string)
            if (success[-1] == -1 ):
                string = "you could not signed up due to " + str(success[0])
                flash(string, "error")
                return render_template('register.html',session_id = (session["id"]),session_type = session["type"],active_num = active_num, title='Register', form=form)

        flash("you have signed up", "success")
        
        return redirect("/login")

    return render_template('register.html',session_id = (session["id"]),session_type = session["type"],active_num = active_num, title='Register', form=form,total_user=total_user)


if __name__ == "__main__":
    if(not HEROKU):
        app.run(debug = True)
    else: 
        app.run()
