from flask import Flask, redirect, url_for, render_template, request, json, flash, session
import requests
from flask import redirect
import time
import uuid
import datetime
import pytz
import base64


app = Flask(__name__)

# def generate_unique_token():
    # return str(uuid.uuid4())

def calculate_time_difference(input_date, input_time):
    """Calculates the time difference from current time in seconds.

    Args:
        input_date: The input date in YYYY-MM-DD format.
        input_time: The input time in HH:MM format.

    Returns:
        The time difference in seconds. If the input time is in the past, returns -1.
    """
    # Parse the input date and time into datetime objects without timezone first
    input_datetime = datetime.datetime.strptime(f"{input_date} {input_time}", "%Y-%m-%d %H:%M")
        # Set the CST timezone for the input datetime
    cst_timezone = pytz.timezone('America/Chicago')
    input_datetime = cst_timezone.localize(input_datetime)

    # Get the current time in CST
    current_time = datetime.datetime.now(tz=cst_timezone)
    print(current_time)

    # Calculate the time difference in seconds
    time_difference = (input_datetime - current_time).total_seconds()

    # Check if the input time is in the past
    if time_difference < 0:
        return -1

    return time_difference
    
app.config['SECRET_KEY'] = 'Satya#507'

@app.route('/')
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["POST", "GET"])
def login():
    err=None
    if request.method=="POST":
        user=request.form["user"]
        pwd=request.form["pwd"]
        session['pwd'] = pwd
        session['user'] = user
        url = "https://204.90.115.200:10443//zosmf/services/authenticate"
        headers = {
                    "X-CSRF-ZOSMF-HEADER": "dummy",
                    "Accept": "application/json",
                    "Authorization": f"Basic {base64.b64encode(f'{user}:{pwd}'.encode('utf-8')).decode('utf-8')}",
                    "Content-Type": "application/x-www-form-urlencoded"
                }
        response = requests.post(url, headers=headers, verify=False)
        if response.status_code != 200:
            err="INVALID USER/PASSWORD!"
            err1=""
            err=err+"<br>"+err1
            flash(err, category="danger")
            return render_template("login.html", user=user, pwd='', error=err)
        else:
           return redirect(url_for("mytools"))       
    else:
       return render_template("login.html")

@app.route("/mytools", methods=["POST", "GET"])
def mytools():
    err=None
    user = session.get('user')
    pwd = session.get('pwd')
    if request.method=="POST":
        tool=request.form["nm"]
        if tool.strip()=="":
            err="INVALID SELECTION!"
            err1="PLEASE SELECT A TOOL"
            err=err+"<br>"+err1
            flash(err, category="danger")
            return render_template("mytools.html", op=tool, error=err)
        if tool.strip()=="autosvp":
            return redirect(url_for("svprstinfo"))
        else:
            return redirect(url_for("pftp"))
    else:
        jid=request.args.get("jid")
        jnm=request.args.get("jnm")
        fd=request.args.get("fd")
        if jid!=None and jnm!=None:
            err=fd
            err1=""
            err=err+"<br>"+err1
            if err[7:13]=="ERROR:":
               flash(err, category="danger")
            else:
               flash(err, category="success") 
            return redirect(url_for("mytools"))
        return render_template("mytools.html")
    
@app.route("/svprstinfo", methods=["GET", "POST"])
def svprstinfo():
#    pwd=request.args.get("pwd")
    user = session.get('user')
    pwd = session.get('pwd')
    err=None
    if request.method=="POST":
       rst=request.form["rst"]
       if rst=='y':
          fu=request.form["fu"]
       if rst.strip()=="":
           err="INVALID SELECTION!"
           err1=""
           err=err+"<br>"+err1
           flash(err)
           return render_template("svprstinfo.html", error=err)
       if rst=="y":
           return redirect(url_for("svprst", fu=fu))
       else:
           return redirect(url_for("svppnl"))
    else:
        return render_template("svprstinfo.html")
@app.route("/svppnl", methods=["GET", "POST"])
def svppnl():
    headers1 = {
                  "X-CSRF-ZOSMF-HEADER": "dummy",
                  "Accept": "application/json",
                  "Content-Type": "text/plain"
                 }
    headers2 = {
       "X-CSRF-ZOSMF-HEADER": "dummy",
       "Accept": "application/json",
        "Content-Type": "application/json"
              }
    user = session.get('user')
    pwd = session.get('pwd')
    auth = (user, pwd)
    err=None
    if request.method=="POST":
       cyl=request.form["cyl"]
       db=request.form["db"]
       email=request.form["email"]
       req=request.form["req"]
       conf=request.form["conf"]
       pcalin=request.form["pcalin"]
       calin=request.form["calin"]
       cloin=request.form["cloin"]
       if cyl.strip()=="":
           err="PLEASE SELECT CYCLE"
           err1=""
           err=err+"<br>"+err1
           flash(err)
           return render_template("svppnl.html", op1=cyl, op2=db, email=email, req=req, conf=conf, pcalin=pcalin, calin=calin, cloin=cloin, error=err)
       if db.strip()=="":
           err="PLEASE SELECT DB"
           err1=""
           err=err+"<br>"+err1
           flash(err)
           return render_template("svppnl.html", op1=cyl, op2=db, email=email, req=req, conf=conf, pcalin=pcalin, calin=calin, cloin=cloin, error=err)
       fpcalin=pcalin[5:7]
       fpcalin1=pcalin[8:10]
       fpcalin=fpcalin+fpcalin1
       if calin.strip()!="":
        if  cloin.strip() =="":
            err="ERROR: PLEASE ENTER TIME TO SCHEDULE"
            err1=''
            err=err+"<br>"+err1
            flash(err)
            return render_template("svppnl.html", op1=cyl, op2=db, email=email, req=req, conf=conf, pcalin=pcalin, calin=calin, cloin=cloin, error=err)
       if cloin.strip()!="":
        if  calin.strip() =="":
            err="ERROR: PLEASE ENTER DATE TO SCHEDULE"
            err1=''
            err=err+"<br>"+err1
            flash(err)
            return render_template("svppnl.html", op1=cyl, op2=db, email=email, req=req, conf=conf, pcalin=pcalin, calin=calin, cloin=cloin, error=err)
       if calin.strip()!="" and cloin.strip() !="":
          time_diff = calculate_time_difference(calin, cloin)
          if time_diff == -1:
             err="ERROR: THE SCHEDULED DATE/TIME IN PAST"
             err1=''
             err=err+"<br>"+err1
             flash(err)
             return render_template("svppnl.html", op1=cyl, op2=db, email=email, req=req, conf=conf, pcalin=pcalin, calin=calin, cloin=cloin, error=err)
       else:
           time_diff="0"
       indata=cyl+db+conf+fpcalin+str(time_diff)+email
       indata=indata.upper()
       burl = "https://204.90.115.200:10443/zosmf"
       iurl="/restfiles/ds/"+user+".SVPIN"
       url=burl+iurl
       res = requests.put(url, data=indata, headers=headers1, auth=auth, verify=False)
       if res.status_code > 204:
           jnm=res.reason
           jid=res.status_code
           fd=f"SVPPNL ERROR: REASON: {jnm} WITH RETURN-CODE: {jid}"
           return redirect(url_for("mytools", jnm=jnm, jid=jid, fd=fd))
       iurl = "/restjobs/jobs"
       url=burl+iurl
       indd="//'"+user+".JCLLIB(SVPJCL)'"
       data = {
          "file": f"{indd}"
       }
       res1 = requests.put(url, json=data, headers=headers2, auth=auth, verify=False)
       if res1.status_code > 204:
          jnm=res1.reason
          jid=res1.status_code
          fd=f"SVPPNL ERROR: REASON: {jnm} WITH RETURN-CODE: {jid}"
          return redirect(url_for("mytools", jnm=jnm, jid=jid, fd=fd))
       time.sleep(10)
       iurl = "/restjobs/jobs?owner="f"{user}""&prefix=PLSV*"
       url=burl+iurl
       res2 = requests.get(url, headers=headers2, auth=auth, verify=False)
       if res2.status_code > 204:
          jnm=res2.reason
          jid=res2.status_code
          fd=f"SVPPNL ERROR: REASON: {jnm} WITH RETURN-CODE: {jid}"
          return redirect(url_for("mytools", jnm=jnm, jid=jid, fd=fd))
       rd=res2.json()
       job_data=rd[0]
       jid = job_data["jobid"]
       jnm = job_data["jobname"]
       fd=f"THE SVP SUBMITTED SUCESSFULY WITH DETAILS AS {jnm}({jid})"
       return redirect(url_for("mytools", jnm=jnm, jid=jid, fd=fd))
    else:
       return render_template("svppnl.html")

@app.route("/svprst", methods=["GET", "POST"])
def svprst():
    headers1 = {
                "X-CSRF-ZOSMF-HEADER": "dummy",
                "Accept": "application/json",
                "Content-Type": "text/plain"
                }
    headers2 = {
                "X-CSRF-ZOSMF-HEADER": "dummy",
                "Accept": "application/json",
                "Content-Type": "application/json"
                }
    user = session.get('user')
    pwd = session.get('pwd')
    fu=request.args.get("fu")
    auth = (user, pwd)
    err=None
    if request.method=="POST":
       cyl=request.form["cyl"]
       db=request.form["db"]
       email=request.form["email"]
       rd=request.form["rd"]
       if cyl.strip()=="":
           err="PLEASE SELECT CYCLE"
           err1=""
           err=err+"<br>"+err1
           flash(err)
           return render_template("svprst.html", op3=cyl, op4=db, email=email, rd=rd, error=err)
       if db.strip()=="":
            err="PLEASE SELECT DB"
            err1=""
            err=err+"<br>"+err1
            flash(err)
            return render_template("svprst.html", op3=cyl, op4=db, email=email, rd=rd, error=err)
       burl = "https://204.90.115.200:10443/zosmf"
       iurl="/restfiles/ds/"+user+".SVPRST"
       url=burl+iurl
       indata=fu+cyl+db+rd+email
       indata=indata.upper()
       res = requests.put(url, data=indata, headers=headers1, auth=auth, verify=False)
       if res.status_code > 204:
          jnm=res.reason
          jid=res.status_code
          fd=f"SVPRST ERROR: REASON: {jnm} WITH RETURN-CODE: {jid}"
          return redirect(url_for("mytools", jnm=jnm, jid=jid, fd=fd))
       iurl = "/restjobs/jobs"
       url=burl+iurl
       indd="//'"+user+".JCLLIB(SVPFRST)'"
       data = {
                "file": f"{indd}"
            }
       res1 = requests.put(url, json=data, headers=headers2, auth=auth, verify=False)
       if res1.status_code > 204:
          jnm=res1.reason
          jid=res1.status_code
          fd=f"SVPRST ERROR: REASON: {jnm} WITH RETURN-CODE: {jid}"
          return redirect(url_for("mytools", jnm=jnm, jid=jid, fd=fd))
       time.sleep(10)
       iurl = "/restjobs/jobs?owner="f"{user}""&prefix=PLRS*"
       url=burl+iurl
       res2 = requests.get(url, headers=headers2, auth=auth, verify=False)
       if res2.status_code > 204:
          jnm=res2.reason
          jid=res2.status_code
          fd=f"SVPRST ERROR: REASON: {jnm} WITH RETURN-CODE: {jid}"
          return redirect(url_for("mytools", jnm=jnm, jid=jid, fd=fd))
       rd=res2.json()
       job_data=rd[0]
       jid = job_data["jobid"]
       jnm = job_data["jobname"]
       fd=f"THE SVP RESTARTED SUCESSFULY WITH DETAILS AS {jnm}({jid})"
       return redirect(url_for("mytools", jnm=jnm, jid=jid, fd=fd))
    else:
        burl = "https://204.90.115.200:10443/zosmf"
        iurl="/restfiles/ds/"+user+".SVPJOB"
        url=burl+iurl
        fu=fu.upper()
        res = requests.put(url, data=fu, headers=headers1, auth=auth, verify=False)
        if res.status_code > 204:
          jnm=res.reason
          jid=res.status_code
          fd=f"SVPRST ERROR: REASON: {jnm} WITH RETURN-CODE: {jid}"
          return redirect(url_for("mytools", jnm=jnm, jid=jid, fd=fd))
        iurl = "/restjobs/jobs"
        url=burl+iurl
        indd="//'"+user+".JCLLIB(SVPGTJOB)'"
        data = {
                    "file": f"{indd}"
                }
        res1 = requests.put(url, json=data, headers=headers2, auth=auth, verify=False)
        if res1.status_code > 204:
          jnm=res1.reason
          jid=res1.status_code
          fd=f"SVPRST ERROR: REASON: {jnm} WITH RETURN-CODE: {jid}"
          return redirect(url_for("mytools", jnm=jnm, jid=jid, fd=fd))
        time.sleep(10)
        iurl="/restfiles/ds/"+user+".SVPOUT"
        url=burl+iurl
        res2 = requests.get(url, headers=headers1, auth=auth, verify=False)
        if res2.status_code > 204:
          jnm=res2.reason
          jid=res2.status_code
          fd=f"SVPRST ERROR: REASON: {jnm} WITH RETURN-CODE: {jid}"
          return redirect(url_for("mytools", jnm=jnm, jid=jid, fd=fd))
        rd=res2.text
        rd=rd.upper()
        return render_template("svprst.html", op3='', op4='', email='', rd=rd, error=None)

@app.route("/pftp", methods=["GET", "POST"])
def pftp():
    headers1 = {
              "X-CSRF-ZOSMF-HEADER": "dummy",
              "Accept": "application/json",
              "Content-Type": "text/plain"
            }
    headers2 = {
                 "X-CSRF-ZOSMF-HEADER": "dummy",
                 "Accept": "application/json",
                 "Content-Type": "application/json"
            }
    user = session.get('user')
    pwd = session.get('pwd')
    auth = (user, pwd)
    err=None
    if request.method=="POST":
       file = request.files['file']
       md=request.form["md"]
       md=md.upper()
       mdl = request.form.get("mdl").strip()
       mdl=int(mdl)
       if file.filename[-4:] != '.txt':
           err="INVALID FILE TYPE, ONLY .txt TYPE SUPPORTED!"
           err1=""
           err=err+"<br>"+err1
           flash(err)
           return render_template("ftp.html", md=md, mdl=mdl, error=err)
       if mdl==0:
           err="THE LENGTH CAN'T BE 0"
           err1=""
           err=err+"<br>"+err1
           flash(err)
           return render_template("ftp.html", md=md, mdl=mdl, error=err)
       data={"dsorg":"PS","alcunit":"CYL","primary":100,
            "secondary":50,"avgblk":500,"recfm":"FB","blksize":0,"lrecl":mdl}
       burl = "https://204.90.115.200:10443/zosmf"
       iurl="/restfiles/ds/"+md
       url=burl+iurl
       res = requests.post(url, json=data, headers=headers2, auth=auth, verify=False)
       if res.status_code > 204:
           jnm=res.reason
           jid=res.status_code
           fd=f"FTP  ERROR: REASON: {jnm} WITH RETURN-CODE: {jid}"
           return redirect(url_for("mytools", jnm=jnm, jid=jid, fd=fd))
       time.sleep(5)
       iurl="/restfiles/ds/"+md
       url=burl+iurl
       file_data = file.read().decode('utf-8')
       res1 = requests.put(url, data=file_data, headers=headers1, auth=auth, verify=False)
       if res1.status_code > 204:
          jnm=res1.reason
          jid=res1.status_code
          fd=f"FTP  ERROR: REASON: {jnm} WITH RETURN-CODE: {jid}"
          return redirect(url_for("mytools", jnm=jnm, jid=jid, fd=fd))
       
       fd= f"FTP DONE SUCCESFULLY TO {md}"
       return redirect(url_for("mytools", jnm='', jid='', fd=fd))
    else:
       return render_template("ftp.html")
       

# @app.route("/finalmsg")
# def finalmsg():
    # jid=request.args.get("jid")
    # jnm=request.args.get("jnm")
    # fd=f"THE SVP JOB SUBMITTED SUCESSFULY WITH DETAILS AS {jnm}({jid})"
    # return f"<h3>{fd}</h3>"
    # time.sleep(5)
    # return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
