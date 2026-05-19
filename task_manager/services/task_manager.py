'''File untuk semua logic Personal Task manager'''

import datetime as dt
from utils.helper import get_today
from config.constants import STATUS_MAP,PRIORITY_MAP,STATUS
from config.settings import DATE_FORMAT
from database.db import SessionLocal
from database.models import Task,User
from werkzeug.security import generate_password_hash, check_password_hash


class ManagerTask:
    '''Class untuk semua logic'''
    def __init__(self):
        self.db = SessionLocal()

    def delete_user(self,user):
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False

    def register(self,username,password):
        '''Fungsi manager - register user'''
        user = self.db.query(User).filter_by(username=username).first()
        if user:
            return False

        hased_password = generate_password_hash(password)
        new_user = User(
            username=username,
            password=hased_password,
            role="user"
            )
        self.db.add(new_user)
        self.db.commit()
        return True

    def login(self,username,password):
        '''Fungsi manager - login user'''
        user = self.db.query(User).filter_by(username=username).first()

        if user and check_password_hash(user.password,password):
            return user
        return None

    def query(self,data,filter_by=None,search_by=None,sort_by=None):
        '''Fungsi manager - Gabungan Fungsi Fil,Search,sort'''
        result = data

        if filter_by:
            for (category,value) in filter_by:
                result = self.filter_tasks(result,category,value)

        if search_by:
            keyword = search_by
            result = self.search_task(result,keyword)

        if sort_by:
            (category,ord_) = sort_by
            result = self.sort_tasks(result,category,ord_)

        return result

    def sorts(self,data,tipe):
        rules = {
            "newest": lambda : self.sort_tasks(data,"id","desc"),
            "oldest": lambda : self.sort_tasks(data,"id","asc"),
            "due_date": lambda : self.sort_tasks(data,"due_date","asc"),
            "priority":lambda : self.sort_tasks(data,"priority","desc")
        }

        rule = rules.get(tipe)
        if not rule:
            return data
        return rule()

    def sort_tasks(self,data,cat_sort,order):
        '''Fungsi manager - sort task'''
        if order not in ["asc","ascending","desc","descending"]:
            order = "Asc"

        rules = {
            "id": lambda item : item.id,
            "title": lambda item : item.title,
            "statue": lambda item : STATUS_MAP[item.statue],
            "category": lambda item : item.category,
            "priority": lambda item : PRIORITY_MAP[item.priority],
            "created_at": lambda item : dt.datetime.strptime(item.created_at,DATE_FORMAT),
            "due_date": lambda item : dt.datetime.strptime(item.due_date,DATE_FORMAT) if item.due_date else dt.datetime.max
        }

        rule = rules.get(cat_sort)
        if not rule:
            return data
        reverse = order in ["desc","descending"]
        return sorted(data,key=rule,reverse=reverse)

    def filter_tasks(self,data,cat_filter,val_filter):
        '''Fungsi manager - filter task'''
        rules = {
            "id": lambda item : val_filter.isdigit() and item.id == int(val_filter),
            "title": lambda item : val_filter.lower() in item.title.lower(),
            "statue": lambda item : val_filter.lower() == item.statue.lower(),
            "category": lambda item : val_filter.lower() == item.category.lower(),
            "created_at": lambda item : val_filter == item.created_at,
            "due_date": lambda item : val_filter == item.due_date
        }
        rule = rules.get(cat_filter)
        if not rule:
            return data
        return list(filter(rule,data))
        # return [item for item in data if rule(item)]

    def mark_as_done(self,task):
        '''Fungsi manager - Tandai Selesai'''
        if task.statue not in STATUS:
            return False

        task.statue = "Done" if task.statue == "Pending" else "Pending"
        self.db.commit()
        return True

    def search_task(self,data,key_search:str):
        '''Fungsi manager - Cari kata di dalam task'''
        return [i for i in data
                if key_search in i.title.lower()
                or key_search in i.descrip.lower()]

    def delete_task(self,task):
        '''Fungsi manager - Hapus task based id'''
        if not task:
            return False
        self.db.delete(task)
        self.db.commit()
        return True

    def edit_task(self,task,title:str=None,descrip:str=None,category:str=None,priority:str=None,due_date:str=None):
        '''Fungsi manager - edit task based id'''
        if not task:
            return False

        task.title = title
        task.descrip = descrip
        task.category = category
        task.priority = priority
        task.due_date = due_date
        self.db.commit()
        return True

    def create_task(self,title,descrip,category,due_date,user_id,priority):
        '''fungsi manager - menambah task baru'''
        task = Task(
            title = title,
            descrip = descrip,
            category = category,
            statue = "Pending",
            created_at = get_today(),
            due_date = due_date,
            user_id = user_id,
            priority = priority
        )
        self.db.add(task)
        self.db.commit()
        return True

    def paginate(self,data,page,per_page):
        '''Fungsi Helper UI - Tampilkan task dalam halaman'''
        start = (page-1)*per_page
        end = start + per_page
        return data[start:end]

    def get_user_task(self,task_id,user_id):
        return self.db.query(Task).filter_by(
            id = task_id,
            user_id = user_id
        ).first()

    def get_tasks_by_user(self,user_id):
        '''mengambil data berdasarkan user id'''
        return self.db.query(Task).filter_by(user_id=user_id).all()

    def get_all_task(self):
        '''Fungsi helper manager - task berdasarkan id'''
        return self.db.query(Task).all()

    def valid_due_date(self,due_date):
        '''Fungsi Helper manager - Valid due date'''
        try:
            dt.datetime.strptime(due_date,DATE_FORMAT)
            return True
        except ValueError:
            return False
