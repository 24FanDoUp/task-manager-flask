'''Authentication'''
from functools import wraps
from flask import session, redirect , url_for
from database.models import User, Task
from extensions import manager

# decorator -----------------------------
def role_required(*roles):
    '''Cek role user'''
    def decorator(f):
        @wraps(f)
        def wrapper(*args,**kwargs):
            user_id = session.get("user_id")

            user = manager.db.query(User).filter_by(id=user_id).first()

            if not user:
                return redirect(url_for("auth.login"))

            if user.role not in roles:
                return "Forbiden",403
            return f(*args,**kwargs)
        return wrapper
    return decorator

def owner_required(model=Task,param="id_",user_field="user_id"):
    '''Cek kepemilikan task'''
    def decorator(f):
        @wraps(f)
        def wrapper(*args,**kwargs):
            user_id = session.get("user_id")
            obj_id = kwargs.get(param)

            if obj_id is None:
                return "Bad request",400

            obj = manager.db.query(model).filter(
                getattr(model,"id") == obj_id,
                getattr(model, user_field) == user_id
            ).first()

            kwargs.pop(param)

            if not obj:
                return "Unauthorized", 403
            return f(task=obj,*args,**kwargs)

        return wrapper
    return decorator

def login_required(f):
    '''Cek user sudah login/session managament'''
    @wraps(f)
    def wrapper(*args,**kwargs):
        user_id = session.get("user_id") # session management

        if not user_id:
            return redirect(url_for("auth.login"))

        user = manager.db.query(User).filter_by(id=user_id).first()

        if not user:
            session.clear()
            return redirect(url_for("auth.login"))

        return f(*args,**kwargs)
    return wrapper
# decorator end ---------------------------------
