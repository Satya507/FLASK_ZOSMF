from flask import Flask, redirect, url_for, render_template, request
#from zoautil_py import datasets
app = Flask(__name__)
@app.route('/')
def hello():
    return "Hello World!"

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method=="POST":
       user=request.form["nm"]
       return redirect("https://204.90.115.200:10443/zosmf/LogOnPanel.jsp")
#      datasets.write("Z30658.ZOWEPS", user)
#      return redirect(url_for("user", usr=user))
    else:
       return render_template("login.html")

@app.route("/<usr>")
def user(usr):
    return f"<h3>{usr}</h3>"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
