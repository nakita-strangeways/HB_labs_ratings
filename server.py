"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template('homepage.html')


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("users.html", users=users)


@app.route("/register",methods = ["GET"])
def display_register_form():

    return render_template("register_form.html")


@app.route("/register",methods = ["POST"])
def register_form():

    user_email = request.form.get("email")
    user_password = request.form.get("password")

    session['s_user_email'] = user_email
    session['s_user_password'] = user_password
    # print('got the things {} {}'.format(user_email, user_password))

    sql = "SELECT email FROM users WHERE email = :email"

    cursor = db.session.execute(sql, {'email': user_email})

    user_result = cursor.fetchone()

    if user_result == None:
        sql = """INSERT INTO users (email, password) 
                VALUES (:email, :password) 
                """
        db.session.execute(sql, {'email': user_email, 'password': user_password})

    db.session.commit()

    print(user_result)

    return redirect("/")



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
