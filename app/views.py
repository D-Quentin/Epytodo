from app import app
from app import controllers
from flask import Flask, render_template, request

class variable:
    i = 0
    j = 0
    username = None
    password = None
    id_task = 0

@app.route ('/')
def     route_index():
    return render_template("home.html")

@app.route ('/register', methods=['POST'])
def     route_register():
    variable.i = 1
    return render_template("register.html")

@app.route ('/singin', methods=['POST'])
def     route_singin():
    variable.i = 2
    return render_template("singin.html")


@app.route('/user', methods=['GET'])
def     route_user():
    result = request.args
    if variable.i == 1:
        variable.username, variable.password = controllers.register_action(result)
        variable.i = 0
        if variable.username == "error":
            return render_template("error.html", error ="Account already exists", url="http://localhost:5000/register")
    if variable.i == 2:
        variable.username, variable.password = controllers.singin_action(result)
        variable.i = 0
        if variable.username == "error":
            return render_template("error.html", error ="Login or password des not matches", url="http://localhost:5000/singin")
    if variable.username == None:
        return render_template("error.html", error ="You must be loggeg in", url="http://localhost:5000/singin")
    return render_template("user.html", username=variable.username, password=variable.password)

@app.route('/singout', methods=['POST'])
def     route_singout():
    variable.username = None
    variable.password = None
    variable.i = 0
    return render_template("singout.html")

@app.route('/user/task', methods=['GET'])
def     route_task():
    variable.j = 2
    tasks = controllers.get_task_action(variable.username, variable.password)
    print "Done"
    return render_template("task.html", tasks=tasks)

@app.route('/user/task/add', methods=['POST'])
def     route_add_task():
    variable.j = 1
    return render_template("create_task.html")

@app.route('/user/task/id', methods=['POST'])
def     route_edit_task():
    result = request.form
    if variable.j == 2:
        variable.id_task, title, begin, end, date_end, status = controllers.get_info_action(result['groupe'])
        variable.j = 0
        return render_template("edit_task.html", nb_task=variable.id_task, title=title, begin=begin, end=end, status=status, date_end=date_end)
    print result['groupe']
    if result['groupe'] == '1' or result['groupe'] == '2' or result['groupe'] == '3':
        controllers.edit_task_action(variable.id_task, result)
        variable.j = 0
    if variable.j == 1:
        variable.id_task = controllers.create_task_action(variable.username, variable.password, result)
    nb_task, title, begin, end, date_end, status = controllers.get_info_action(variable.id_task)
    return render_template("edit_task.html", nb_task=nb_task, title=title, begin=begin, end=end, status=status, date_end=date_end)
