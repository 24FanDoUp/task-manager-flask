'''Config untuk konstanta, variable pasti'''



SORT_OPTION = [
    "newest",
    "oldest",
    "due_date",
    "priority"
]

ADD_INPUT = [
    "title",
    "descrip",
    "category"
    ]

UI_FEATURE = [
    "Create Task",
    "Edit Task",
    "Delete Task",
    "Search Task",
    "Mark as done Task",
    "Filter, Search, Sort"
]

UI_2 = [
    "Id",
    "Title",
    "Status",
    "Category",
    "Create_at",
    "Due_date"
]

STATUS_UI = {
    "Done": "[ V ]",
    "Pending" : "[ - ]"
}


PRIORITY_MAP = {
    "rendah":1,
    "sedang":2,
    "tinggi":3
}

STATUS_MAP = {
    "Done": 1,
    "Pending" : 0
}

VALID_CATEGORY = {
    1 : "id",
    2 : "title",
    3 : "statue",
    4 : "category",
    5 : "create_at",
    6 : "due_date"
}

STATUS = [
    "Done",
    "Pending"
]
