'''Main app'''
from flask import Flask,render_template
from flask_wtf import CSRFProtect

from database.db import engine, Base
from routes import admin_bp,auth_bp,task_bp
from utils.auth_context import inject_user
from config.constants import UI_FEATURE
from config.settings import SECRET_KEY


app = Flask(__name__)
app.secret_key = SECRET_KEY

Base.metadata.create_all(bind=engine)
csrf = CSRFProtect(app)

app.register_blueprint(task_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.context_processor(inject_user)

@app.route("/")
def landing():
    '''Landing Page'''
    return render_template("landing.html",ft = UI_FEATURE)


if __name__ == "__main__":
    app.run(debug=True)
