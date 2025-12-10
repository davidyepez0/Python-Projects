import sqlite3
from tabulate import tabulate
from datetime import datetime

"""Funcion para la creacion o conexion con la base de datos. Retorna la creacion o conexion a la base de datos 'myDatabase.db'"""
def dbConnection():
    try:
        return sqlite3.connect("myDatabase.db")
    except Exception as e:
        print(f"Ha ocurrido un error al crear la base de datos ({e})")

"""Funcion para la creacion de la tabla 'Expenses'."""
def createExpensesTable():
    try:
        with dbConnection() as connection:
            cursor = connection.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS Expenses(
                        idExpense INTEGER PRIMARY KEY AUTOINCREMENT,
                        amount REAL NOT NULL,
                        category TEXT NOT NULL,
                        description TEXT,
                        dateExpense TEXT NOT NULL);''')

            print("La tabla 'Expenses' se creo con exito")
    except Exception as e:
        print(f"Ha ocurrido un error al crear la tabla ({e})")

"""Funcion para la insercion de datos en la tabla 'Expenses'."""
def recordExpense(userAmount, userCategory, userDescription, userDate):
    try:
        with dbConnection() as connection:
            cursor = connection.cursor()

            sqlQuery = '''INSERT INTO Expenses (amount, category, description, dateExpense)
                        VALUES (?, ?, ?, ?);'''
            
            valuesQuery = (userAmount, userCategory, userDescription, userDate)

            cursor.execute(sqlQuery, valuesQuery)

            print("Datos ingresados correctamente")
    except Exception as e:
        print(f"Error al ingresar los datos ({e})")

"""Funcion para filtrar los registros por un rango de fechas y listar los registros desde los mas recientes. Retorna los registros filtrados o sin filtrar"""
def filterDateExpenses(fechaInicio = None, fechaFin = None):

    query = '''SELECT dateExpense, amount, category FROM Expenses'''

    if fechaInicio and fechaFin:
        query += ''' WHERE dateExpense BETWEEN ? AND ?'''

    query += ''' ORDER BY dateExpense DESC'''

    try:
        with dbConnection() as connection:
            return connection.execute(query, (fechaInicio, fechaFin)).fetchall()
    except Exception as e:
        print(f"Error al listar los gastos ({e})")

"""Funcion para filtrar el total de los gastos por una categoria y mostrar el total de gastos. Retorna el total de gastos con o sin filtro"""
def totalFilterExpenses(category = None):

    query = '''SELECT SUM(amount) FROM Expenses'''

    if category:
        query += ''' WHERE category = ?'''

    try:
        with dbConnection() as connection:
            return connection.execute(query, (category,)).fetchall()
    except Exception as e:
        print(f"Error al mostrar los totales ({e})")

"""Funcion para mostrar los registros de los gastos de manera ordenada en una tabla. Retorna una tabla con los gastos con o sin filtro"""
def showAmounts(category = None):

    data = totalFilterExpenses(category)

    if not data:
        print("Aun no hay registros de gastos")
        return 

    table = tabulate(data, headers = ["Total de gastos"], tablefmt = "grid") 
    print(table)

"""Funcion para mostrar todos los registros de manera ordenada en una tabla. Retorna una tabla con el gasto, la categoria, la descripcion y la fecha de cada registro"""
def showListExpenses(fechaInicio = None, fechaFin = None):
    
    data = filterDateExpenses(fechaInicio, fechaFin)

    if not data:
        print("Aun no hay registros de gastos")
        return 

    table = tabulate(data, headers = ["Gasto", "Categoria", "Descripcion", "Fecha"], tablefmt = "grid")
    print(table)

"""Funcion para verificar las fechas que ingresa el usuario. Retorna el input verificado"""
def handleDates(userDate):
    while True:
        try:
            a = input(userDate)
            datetime.strptime(a, "%Y-%m-%d")
            return a
        except ValueError:
            print("La fecha no es valida")

"""Funcion para verificar los numeros que ingresa el usuario. Retorna el input verificado"""
def handleIntsInputs(userInput):
    while True:
        try:
            return int(input(userInput))
        except ValueError:
            print("Debe ingrese un valor valido")   

"""Funcion para mostrar el menu para usuario donde se llaman a todas la funciones anteriores"""
def menu():
    createExpensesTable()
    print("Bienvenido al gestor de gastos personales")

    while True:
    
        option = handleIntsInputs("¿Que desea hacer?:\n1. Ingresar un gasto\n2. Ver todos los gastos\n3. Ver los gastos por fecha\n" \
                        "4. Ver total gastado\n5. Ver total por categoria\n6. Salir\n")
        
        match option:
            case 1: 
                userAmount = handleIntsInputs("Ingrese el monto de dinero usado: ")
                userCategory = input("Ingrese la categoria para el gasto: ")
                userDescription = input("Ingrese la descripcion para el gasto: ")
                userDate = handleDates("Ingrese la fecha del gasto: ")
                recordExpense(userAmount, userCategory, userDescription, userDate)
            case 2: showListExpenses()
            case 3:
                userDate1 = handleDates("Ingrese la fecha de inicio para el filtro: ")
                userDate2 = handleDates("Ingrese la fecha final para el filtro: ")
                showListExpenses(userDate1, userDate2)
            case 4: showAmounts()
            case 5:
                categoryUser = input("Ingrese la categoria para el filtro: ") 
                showAmounts(categoryUser)
            case 6:
                break
            case _: print("Ingrese una opcion valida")

    print("Ha salido del gestor de gastos")
    
menu()