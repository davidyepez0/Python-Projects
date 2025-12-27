from flask import Flask, jsonify, request, abort
import requests

"""Funcion para la creacion del endpoint y el servidor de Flask. Retorna la aplicacion"""
def create_app():
    app = Flask(__name__)

    """Endpoint para la conversion de una moneda a otra a traves de una API externa. Retorna un JSON con la moneda de origen, destino, cantidad y conversion"""
    @app.route('/convert', methods=['POST'])
    def currency_conversion():
        data = request.get_json()

        if not data:
            abort(400, 'No hay datos')

        origin_currency = data.get('origin_currency')
        destination_currency = data.get('destination_currency')
        currency_amount = data.get('currency_amount')

        validation(origin_currency, destination_currency, currency_amount)
        
        origin_currency = origin_currency.upper()
        destination_currency = destination_currency.upper()

        try:
            extern_api = requests.get(f'https://api.frankfurter.dev/v1/latest?base={origin_currency}&symbols={destination_currency}&amount={currency_amount}', timeout=5)
        except requests.exceptions.Timeout as e:
            abort(400, f'Se agoto el tiempo de espera de la solicitud: ({e})')

        if extern_api.status_code == 200:
            response = extern_api.json()
            conversion= response["rates"][destination_currency]
        else:
            abort(400, 'Algo ocurrio mal....')

        final_data = {"origin_currency": origin_currency,
                      "destination_currency": destination_currency,
                      "currency_amount": currency_amount,
                      "conversion": conversion}

        return jsonify(final_data), 200
    
    return app

"""Funcion para la validacion de los datos ingresados, que no esten vacios y que la cantidad sea un numero"""
def validation(origin, destination, amount):
    if origin is None or len(origin) != 3:
        abort(400, 'La moneda de origen debe tener 3 letras')
    if destination is None or len(destination) != 3:
        abort(400, 'La moneda de destino debe tener 3 letras')
    if amount is None or not isinstance(amount, (float, int)):
        abort(400, 'La cantidad debe ser un numero valido')
    if amount <= 0:
        abort(400, 'La cantidad debe ser mayor a cero')

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)