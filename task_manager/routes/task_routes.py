from flask import Blueprint,render_template,redirect,request,url_for,session
from datetime import datetime

from decorators import login_required,owner_required
from extensions import manager
from config.constants import ADD_INPUT,SORT_OPTION
from database.models import Task

task_bp = Blueprint("task",__name__,url_prefix="/task")

@task_bp.route("/mark/<int:id_>",methods = ["GET","POST"])
@login_required
@owner_required(model=Task,param="id_")
def mark_task(task):
    '''Fungsi Flask, ubah_status'''
    if request.method == "POST":
        manager.mark_as_done(task)
        return redirect(url_for("task.view"))

@task_bp.route("/delete/<int:id_>", methods = ["POST"])
@login_required # route protection
@owner_required(model=Task,param="id_")
def delete_task(task):
    '''Fungsi Flask - hapus task berdasarkan id'''
    if request.method == "POST":
        print("DELETE ROUTE TERPANGGIL:", task)
        manager.db.delete(task)
        manager.db.commit()
        return redirect(url_for("task.view"))

@task_bp.route("/edit/<int:id_>", methods = ["GET","POST"])
@login_required
@owner_required(model=Task,param="id_")
def edit_task(task):
    '''Fungsi Flask - edit task berdasarkan id'''

    if request.method == "POST":
        title = request.form.get("title")
        descrip = request.form.get("descrip")
        category = request.form.get("category")
        priority = request.form.get("priority")
        due_date = request.form.get("due_date")

        manager.edit_task(
            task,
            title=title,
            descrip=descrip,
            category=category,
            priority=priority,
            due_date=due_date
        )
        return redirect(url_for("task.view"))

    return render_template("task/edit.html",task = task)

@task_bp.route("/add", methods = ["GET","POST"])
@login_required
def add():
    ''' Fungsi Flask -  tambah task'''
    user_id = session["user_id"]

    if request.method == "POST":
        title = request.form["title"]
        descrip = request.form["descrip"]
        category = request.form["category"]
        due_date = request.form["due_date"]
        priority = request.form["priority"]

        if not title or not descrip or not category or not due_date:
            return render_template("/task/add.html",
                                   error = "Semua input data harus di isi !!!",
                                   ADD_INPUT = ADD_INPUT)

        try:
            date_obj = datetime.strptime(due_date, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%d/%m/%Y")
        except ValueError:
            return render_template("/task/add.html",
                                   error_date="Date tidak valid !!!",
                                   ADD_INPUT=ADD_INPUT)


        manager.create_task(title,descrip,category,formatted_date,user_id,priority)
        return redirect(url_for("task.view"))
    return render_template("/task/add.html", ADD_INPUT = ADD_INPUT)

@task_bp.route("/view", methods = ["GET","POST"])
@login_required
def view():
    '''Fungsi Flask - memperlihatkan task'''
    page = int(request.args.get("page",1,type=int))
    search_by = request.args.get("search_by","").strip() or None
    category_by = request.args.get("category_by","").strip() or None
    status_by = request.args.get("status_by","").strip() or None
    sort_by = request.args.get("sort_by","").strip() or None

    user_id = session.get("user_id")
    result = manager.get_tasks_by_user(user_id)

    if request.method == "GET": # tampikan semua task
        if len(result)<1:
            return redirect(url_for("task.add"))

    # search task
    if search_by:
        result = manager.search_task(result,search_by)

    # filter task
    if category_by: # berdasarkan category
        result = manager.filter_tasks(result,"category",category_by)

    if status_by: # berdasarkan status
        result = manager.filter_tasks(result,"statue",status_by)

    # sort task
    if sort_by in SORT_OPTION:
        result = manager.sorts(result,sort_by)

    # paginate
    per_page = 3
    total = len(result)
    total_pages = (total + per_page - 1) // per_page

    result_paginate = manager.paginate(result,page,per_page)

    return render_template("/task/dashboard.html",
                            tasks = result_paginate,
                            page = page,
                            per_page = per_page,
                            total_pages = total_pages,
                            category_by = category_by,
                            status_by = status_by,
                            sort_by = sort_by
                            )
