from app import app
import pymysql as sql
import config

def create_user(username, password):
    cnx = sql.connect(host=config.DATABASE_HOST, user=config.DATABASE_USER, passwd=config.DATABASE_PASS, db=config.DATABASE_NAME, unix_socket=config.DATABASE_SOCK)
    cursor = cnx.cursor()
    sql_code = (
        "SELECT * FROM user WHERE username=%s"
    )
    data = (username)
    cursor.execute(sql_code, data)
    k = cursor.rowcount
    if k != 0:
        return (k)
    sql_code = (
        "INSERT INTO user (username, password) "
        "VALUES (%s, %s)"
    )
    data = (username, password)
    cursor.execute(sql_code, data)
    cnx.commit()
    cursor.close()
    return (k)

def check_user(username, password):
    cnx = sql.connect(host=config.DATABASE_HOST, user=config.DATABASE_USER, passwd=config.DATABASE_PASS, db=config.DATABASE_NAME, unix_socket=config.DATABASE_SOCK)
    cursor = cnx.cursor()
    sql_code = (
        "SELECT * FROM user WHERE username=%s AND password=%s"
    )
    data = (username, password)
    cursor.execute(sql_code, data)
    k = cursor.rowcount
    cursor.close()
    return (k)

def get_id(username, password):
    cnx = sql.connect(host=config.DATABASE_HOST, user=config.DATABASE_USER, passwd=config.DATABASE_PASS, db=config.DATABASE_NAME, unix_socket=config.DATABASE_SOCK)
    cursor = cnx.cursor()
    sql_code = (
        "SELECT user_id FROM user WHERE username=%s AND password=%s"
    )
    data = (username, password)
    cursor.execute(sql_code, data)
    id = cursor.fetchone()
    my_id = int(id[0])
    return (my_id)

def get_tasks(id):
    tasks = []
    cnx = sql.connect(host=config.DATABASE_HOST, user=config.DATABASE_USER, passwd=config.DATABASE_PASS, db=config.DATABASE_NAME, unix_socket=config.DATABASE_SOCK)
    cursor = cnx.cursor()
    sql_code = (
        "SELECT fk_task_id FROM user_has_task WHERE fk_user_id=%s"
    )
    data = (id)
    cursor.execute(sql_code, data)
    all_id = cursor.fetchall()
    cursor.close()
    for my_id in all_id:
        cnx = sql.connect(host=config.DATABASE_HOST, user=config.DATABASE_USER, passwd=config.DATABASE_PASS, db=config.DATABASE_NAME, unix_socket=config.DATABASE_SOCK)
        cursor = cnx.cursor()
        sql_code = (
            "SELECT * FROM task WHERE task_id=%s"
        )
        data = (my_id)
        cursor.execute(sql_code, data)
        my_task = list(cursor.fetchall()[0])
        tasks.append(my_task)
        cursor.close()
    return tasks


def create_task(id, title):
    cnx = sql.connect(host=config.DATABASE_HOST, user=config.DATABASE_USER, passwd=config.DATABASE_PASS, db=config.DATABASE_NAME, unix_socket=config.DATABASE_SOCK)
    cursor = cnx.cursor()
    sql_code = (
        "INSERT INTO task (title)"
        "VALUES (%s)"
    )
    data = (title)
    cursor.execute(sql_code, data)
    cnx.commit()
    cursor.close()
    id_task = cursor.lastrowid
    cnx = sql.connect(host=config.DATABASE_HOST, user=config.DATABASE_USER, passwd=config.DATABASE_PASS, db=config.DATABASE_NAME, unix_socket=config.DATABASE_SOCK)
    cursor = cnx.cursor()
    sql_code = (
        "INSERT INTO user_has_task (fk_user_id, fk_task_id)"
        "VALUES (%s, %s)"
    )
    datas = (id, id_task)
    cursor.execute(sql_code, datas)
    cnx.commit()
    cursor.close()
    return (id_task)

def edit_task(task_id, status):
    cnx = sql.connect(host=config.DATABASE_HOST, user=config.DATABASE_USER, passwd=config.DATABASE_PASS, db=config.DATABASE_NAME, unix_socket=config.DATABASE_SOCK)
    cursor = cnx.cursor()
    sql_code = (
        "UPDATE task SET status=%s WHERE task_id=%s"
    )
    data = (status, task_id)
    cursor.execute(sql_code, data)
    cnx.commit()
    cursor.close()
    if status == "done":
        cnx = sql.connect(host=config.DATABASE_HOST, user=config.DATABASE_USER, passwd=config.DATABASE_PASS, db=config.DATABASE_NAME, unix_socket=config.DATABASE_SOCK)
        cursor = cnx.cursor()
        sql_code = (
            "UPDATE task SET end=NOW() WHERE task_id=%s"
        )
        data = (task_id)
        cursor.execute(sql_code, data)
        cnx.commit()
        cursor.close()

def get_info(id_task):
    cnx = sql.connect(host=config.DATABASE_HOST, user=config.DATABASE_USER, passwd=config.DATABASE_PASS, db=config.DATABASE_NAME, unix_socket=config.DATABASE_SOCK)
    cursor = cnx.cursor()
    sql_code = (
        "SELECT * FROM task WHERE task_id=%s"
    )
    data = (id_task)
    cursor.execute(sql_code, data)
    values = cursor.fetchone()
    nb_task = values[0]
    title = values[1]
    begin = values[2]
    end = values[3]
    status = values[4]
    cursor.close()
    if end == None:
        end = "Not finished yet"
        date_end = ""
    else:
        date_end = end
        end = "Finished on "
    return (nb_task, title, begin, end, date_end, status)