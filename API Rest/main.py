from flask import Flask, jsonify, request, abort
import database

"""Funcion para la creacion de los endpoints y el servidor Flask. Retorna la aplicacion"""
def create_app():
    app = Flask(__name__)

    database.init_app(app)

    """Endpoint para obtener todos los registros de la lista de tareas. Retorna un JSON con todas las tareas y el codigo de estado 200"""
    @app.route('/tasks', methods = ['GET'])
    def get_all_tasks():
        return jsonify(database.list_all_tasks()), 200

    """Endpoint para registrar una nueva tarea, solo se ingresa la descripcion de la tarea. Retorna un JSON con la nueva tarea y el codigo de estado 201"""
    @app.route('/tasks', methods=['POST'])
    def record_new_task():
        data = request.get_json()
        descript_task = data.get("descriptionTask")

        if not descript_task:
            abort(400, 'La descripcion es obligatoria')

        id_new_task = database.record_task_db(descript_task)
        new_task = database.task_by_id(id_new_task)
        
        return jsonify(new_task), 201

    """Endpoint para actualizar una tarea. Retorna una cadena vacia con el codigo de estado 204"""
    @app.route('/tasks/<int:id_task>', methods=['PUT'])
    def update_task(id_task):
        data = request.get_json()

        if not data:
            abort(400, 'Se deben proporcionar datos')

        completed_task = data.get("completedTask")
        desc_task = data.get("descriptionTask")
            
        database.update_task_db(id_task, completed_task, desc_task)

        return '', 204

    """Endpoint para eliminar una tarea. Retorna una cadena vacia con el codigo de estado 204"""
    @app.route('/tasks/<int:id_task>', methods=['DELETE'])   
    def delete_task(id_task):
        database.delete_task_db(id_task)

        return '', 204
    
    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        database.create_table()
    app.run(debug=True)