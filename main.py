from flask import Flask, render_template, request, redirect, url_for, make_response, Response
from models import User, db

app = Flask(__name__)
db.create_all()  #create new tables in database

@app.route("/")
def index():
    email_address = request.cookies.get("email")

    if email_address:
    # get user from the database based on email address
        user = db.query(User).filter_by(email=email_address).first()
    else:
        user = None

    return render_template("index.html", user=user)

@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user-name")
    email = request.form.get("user-email")

    #create a User object and save it into the database
    user = User(name=name, email=email)
    user.save()

    #save user's email into a cookie
    response = make_response(redirect(url_for("index")))
    response.set_cookie("email", email)

    return response

#cookie gets erased from local storage after pressing "celar" button
@app.route("/login-clear", methods=["POST"])
def clear():
    resp = make_response(render_template("index.html"))
    resp.set_cookie("email", expires=0)
    return resp

if __name__=="__main__":
    app.run(port=8888)

    