
from flask import Blueprint,request,session,redirect,render_template,url_for
from extensions import manager

auth_bp = Blueprint("auth",__name__)

@auth_bp.route("/logout")
def logout():
    '''log out'''
    session.clear()
    return redirect(url_for("landing"))

@auth_bp.route("/register", methods = ["GET","POST"])
def register():
    '''Fungsi register user baru'''
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["confirm_password"]

        if manager.register(username,password):
            return redirect(url_for("auth.login"))
    return render_template("auth/register.html")

@auth_bp.route("/login",methods = ["GET","POST"])
def login():
    '''Fungsi login user'''
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = manager.login(username,password) # aunthentication

        if user:
            session["user_id"] = user.id # session management
            session["role"] = user.role
            return redirect(url_for("task.view"))
    return render_template("auth/login.html")
