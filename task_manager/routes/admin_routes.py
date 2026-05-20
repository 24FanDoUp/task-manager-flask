'''admin'''
from flask import Blueprint,request,redirect,render_template,flash,url_for,session

from extensions import manager
from database.models import Task,User
from decorators.auth import login_required,role_required

admin_bp = Blueprint("admin",__name__)

@admin_bp.route("/admin")
@login_required
@role_required("admin")
def dashboard():
    users = manager.db.query(User).all()
    tasks = manager.db.query(Task).all()

    total_users = len(users)
    total_tasks = len(tasks)

    pending_tasks = manager.db.query(Task).filter_by(statue="Pending").count()
    completed_tasks = manager.db.query(Task).filter_by(statue="Done").count()

    return render_template(
        "admin/dashboard1.html",
        users=users,
        total_users=total_users,
        total_tasks=total_tasks,
        pending_tasks=pending_tasks,
        completed_tasks=completed_tasks
    )


@admin_bp.route("/admin")
@login_required
@role_required("admin")
def admin_dashbord():
    tasks = manager.db.query(Task).all()
    users = manager.db.query(User).all()
    page_user = int(request.args.get("page_user",1,type=int))
    page_task = int(request.args.get("page_task",1,type=int))

    user_per_page = 2
    task_per_page = 4
    total_user = len(users)
    total_task = len(tasks)
    total_pages_user = (total_user + user_per_page - 1) // user_per_page
    total_pages_task = (total_task + task_per_page - 1) // task_per_page

    task_paginate = manager.paginate(tasks,page_task,task_per_page)
    user_paginate = manager.paginate(users,page_user,user_per_page)

    return render_template("/admin/dashbord.html",
                           page_user = page_user,
                           page_task = page_task,
                           task_per_page = task_per_page,
                           user_per_page = user_per_page,
                           total_pages_user = total_pages_user,
                           total_pages_task = total_pages_task,
                           tasks = task_paginate,
                           users = user_paginate
                           )

@admin_bp.route("/admin/task/delete/<int:id_>",methods=["POST"])
@login_required
@role_required("admin")
def admin_delete_task(id_):
    task = manager.db.query(Task).filter_by(id=id_).first()

    if not task:
        return "Not found",404

    manager.delete_task(task)
    return redirect("/admin")

@admin_bp.route("/admin/user/role/<int:user_id>",methods=["POST"])
@login_required
@role_required("admin")
def change_role(user_id):

    if user_id == 1:
        flash("Role admin utama tidak boleh diganti","error")
        return redirect(url_for("admin.admin_dashbord"))

    user = manager.db.query(User).filter_by(id=user_id).first()

    if not user:
        flash("User_tidak ditemukan","error")
        return redirect(url_for("admin.admin_dashbord"))

    user.role = "admin" if user.role == "user" else "user"
    manager.db.commit()
    flash("Role berhasil diubah","success")
    return redirect(url_for("admin.admin_dashbord"))

@admin_bp.route("/admin/user/delete/<int:user_id>",methods=["POST"])
@login_required
@role_required("admin")
def delete_user(user_id):

    if user_id == 1:
        flash("Admin utama tidak boleh dihapus","error")
        return redirect(url_for("admin.admin_dashbord"))

    user = manager.db.query(User).filter_by(id=user_id).first()

    if not user:
        flash("User tidak ditemukan","error")
        return redirect(url_for("admin.admin_dashbord"))

    if user.role == "admin" or user.id == session["user_id"]:
        flash("Tidak bisa ubah role sendiri","error")
        return redirect(url_for("admin.admin_dashboard"))

    done_del = manager.delete_user(user)
    if done_del:
        flash("User berhasil dihapus", "success")
    return redirect(url_for("admin.admin_dashbord"))
