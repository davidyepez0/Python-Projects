import sqlite3
from flask import g, abort

"""Funcion para la creacion y conexion de la base de datos guardada en la variable de Flask g. Retorna la creacion y conexion de la base de datos"""
def db_connection():
    if 'db' not in g:
        g.db = sqlite3.connect("myDatabase.db")
        g.db.row_factory = sqlite3.Row
    return g.db

"""Funcion que se encarga de cerrar la conexion con la base de datos despues de cada peticion."""
def close_db(exception = None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

"""Funcion para siempre cerrar la conexion de la base de datos sin importar lo que pase"""
def init_app(app):
    app.teardown_appcontext(close_db)

"""Funcion para la creacion de la tabla 'tasks'."""
def create_table():

    db = db_connection()
    cursor = db.cursor()

    query = '''CREATE TABLE IF NOT EXISTS tasks (
            idTask INTEGER PRIMARY KEY AUTOINCREMENT,
            descriptionTask TEXT NOT NULL,
            completedTask INTEGER NOT NULL);'''
            
    cursor.execute(query)
    db.commit()

"""Funcion para registrar una nueva tarea en la base de datos. Retorna el id del nuevo registro ingresado"""
def record_task_db(descript_task):

    if descript_task is None or descript_task == "":
        abort(400, 'Valores ingresados incorrectamente')

    db = db_connection()
    cursor = db.cursor()

    query = '''INSERT INTO tasks (descriptionTask, completedTask) VALUES (?, ?);'''

    cursor.execute(query, (descript_task, 0))

    db.commit()

    last_id = cursor.lastrowid

    return last_id

"""Funcion para listar todas las tareas de la base de datos. Retorna una lista con un diccionario de cada registro"""
def list_all_tasks():

    db = db_connection()
    cursor = db.cursor()

    query = '''SELECT * FROM tasks;'''
    cursor.execute(query)
    data = cursor.fetchall()

    tasks_list = [dict(row) for row in data]

    return tasks_list

"""Funcion para buscar una tarea por id en la base de datos. Retorna un diccionario con la tarea que coincide"""
def task_by_id(id_task):

    db = db_connection()
    cursor = db.cursor()

    query = '''SELECT * FROM tasks WHERE idTask = ?'''
    cursor.execute(query, (id_task, ))
    data = cursor.fetchone()

    if data is None:
        abort(404, 'Tarea no encontrada')

    one_task = dict(data)

    return one_task
    
"""Funcion para actualizar una tarea de la base de datos"""
def update_task_db(id_task, completed_task = None, desc_task = None):

    if completed_task is None and desc_task is None:
        abort(400, 'Se debe enviar al menos un campo para actualizar')

    query = '''UPDATE tasks SET '''
    values = []
    fields = []

    if desc_task is None or desc_task == "":
        abort(400, "El campo (descriptionTask) no puede estar vacia")
    
    fields.append('descriptionTask = ? ')
    values.append(desc_task)

    if completed_task is not None:
        fields.append('completedTask = ? ')
        values.append(completed_task)

    query += ', '.join(fields) + '''WHERE idTask = ?;'''
    values.append(id_task)

    db = db_connection()
    cursor = db.cursor()

    cursor.execute(query, tuple(values))

    if cursor.rowcount == 0:
        abort(404, 'Id no encontrado')

    db.commit()     

"""Funcion para eliminar una tarea de la base de datos"""
def delete_task_db(id_task):

    db = db_connection()
    cursor = db.cursor()

    query = '''DELETE FROM tasks WHERE idTask = ?'''
    cursor.execute(query, (id_task, ))

    if cursor.rowcount == 0:
        abort(404, 'Id no encontrado')

    db.commit()