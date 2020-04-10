from app import models
import views

def register_action(result):
    username = result['username']
    password = result['password']
    j = models.create_user(username, password)
    if j != 0:
        return ("error", "error")
    return (username, password)

def singin_action(result):
    username = result['username']
    password = result['password']
    j = models.check_user(username, password)
    if j == 0:
        return ("error", "error")
    return (username, password)

def get_task_action(username, password):
    id = models.get_id(username, password)
    tasks = models.get_tasks(id)
    return tasks

def create_task_action(username, password, result):
    title = result['groupe']
    id = models.get_id(username, password)
    id_task = models.create_task(id, title)
    return (id_task)

def edit_task_action(task_id, result):
    value = result['groupe']
    if value == '1':
        status = "not started"
    elif value == '2':
        status = "in progress"
    else:
        status = "done"
    models.edit_task(task_id, status)


def get_info_action(id_task):
    return (models.get_info(id_task))