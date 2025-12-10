import sqlite3

with sqlite3.connect("myDatabase.db") as connection:
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Tasks (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   taskDescription TEXT NOT NULL,
                   completeTask INTEGER NOT NULL);''')
    
    connection.commit()

def addTask():
    descriptionTask = input("Ingrese una tarea para la lista: ")

    cursor.execute(f'''INSERT INTO Tasks (taskDescription, completeTask)
                   VALUES ("{descriptionTask}", 0);''')
    
    connection.commit()
    print("Tarea añadida exitosamente")

def taskList():
    cursor.execute('''SELECT * FROM Tasks;''')
    allTasks = cursor.fetchall()

    print("\nTareas por hacer")
    for task in allTasks:
        print(f"{task[0]}. {task[1]} {"(Completa)" if task[2] == 1 else "(Incompleta)"}")

def completeTask():
    idTaskComplete = int(input("Ingrese el numero de la tarea que completo: "))

    cursor.execute(f'''UPDATE Tasks
                   SET completeTask = 1
                   WHERE id = "{idTaskComplete}";''')
    
    connection.commit()
    print("Tarea completada exitosamente")

def deleteTask():
    taskList()
    taskToDelete = int(input("Ingrese el numero de la tarea que desea eliminar: "))
    
    cursor.execute(f'''DELETE FROM Tasks
                   WHERE id = "{taskToDelete}";''')
    
    connection.commit()
    print("Tarea eliminada exitosamente")

def menu():
    print("Bienvenido a su To-Do List")
    
    while True:

        option = int(input("\n¿Que desea hacer?:" \
        "\n- Para añadir una tarea presione 1\n- Para listar sus tareas presione 2" \
        "\n- Para marcar una tarea como completada presione 3\n- Para eliminar una tarea presione 4" \
        "\n- Para salir de la To-Do List presione 5\n"))

        match option:
            case 1: addTask()
            case 2: taskList()
            case 3: completeTask()
            case 4: deleteTask()
            case 5: break
    
    print("Has salido de tu To-Do List")

menu()
