from flask import Flask, redirect, url_for, render_template, request
import requests

#from zoautil_py import datasets
app = Flask(__name__)
@app.route('/')
def hello():
    return "Hello World!"

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method=="POST":
        user=request.form["nm"]
        data=user
#        url = "https://204.90.115.200:10443/zosmf/restfiles/ds/Z30658.JCLLIB/member"
        url = "https://204.90.115.200:10443/zosmf/restfiles/ds/Z30658.ZOWEPS"
#        data='ch payal'
        headers = {
                   "X-CSRF-ZOSMF-HEADER": "dummy",
                   "Accept": "application/json",
                   "Content-Type": "text/plain"
                  }
        auth = ("Z30658", "qazwsx32")
#        res = requests.get(url, headers=headers, auth=auth, verify=False)
        res = requests.put(url, data=data, headers=headers, auth=auth, verify=False) 
#        data = res.json()
        data = res.text        
        rc=res.status_code
        rc1=res.reason
        usr=rc1
        return redirect(url_for("user", usr=rc1, data1=rc))
#      datasets.write("Z30658.ZOWEPS", user)
#      return redirect(url_for("user", usr=user))
    else:
       return render_template("login.html")

@app.route("/<usr>/<data1>")
def user(usr, data1):
    return f"<h3>{data1}</h3>"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    
