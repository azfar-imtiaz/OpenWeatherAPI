import json
import traceback
from flask_cors import CORS
from flask import Flask, request

import utils
import config
import constants


app = Flask(__name__)
# for cross origin resource sharing
CORS(app)


@app.route('/api/multiple-day-forecast', methods=['POST'])
def get_five_day_forecast():
    # verify if request method is POST
    if request.method == 'POST':
        try:
            data = request.get_json()
        except Exception:
            return json.dumps({
                'status': 'failure',
                'error_message': 'Unable to extract parameters from request',
                'traceback': str(traceback.format_exc())
            })

        try:
            # handle the weather request - extract parameters, call OpenWeather API, parse information etc.
            response = utils.handle_weather_request(
                data,
                constants.COUNTRY_CODES,
                config.URL,
                config.MULTIPLE_DAY_FORECAST_ENDPOINT,
                config.API_KEY,
                constants.DATE_RG,
                constants.TIME_RG
            )
            return response
        except Exception:
            return json.dumps({
                'status': 'failure',
                'error_message': 'Error handling weather request',
                'traceback': str(traceback.format_exc())
            })
    else:
        return json.dumps({
            'status': 'failure',
            'error_message': 'Please send city and country information through a POST request',
            'traceback': str(traceback.format_exc())
        })


@app.route('/api/current-weather', methods=['GET'])
def get_current_weather():
    # verify if request method is GET
    if request.method == 'GET':
        try:
            data = request.get_json()
            if data is None:
                data = dict(request.args)
        except Exception:
            return json.dumps({
                'status': 'failure',
                'error_message': 'Unable to extract parameters from request',
                'traceback': str(traceback.format_exc())
            })

        try:
            # handle the weather request - extract parameters, call OpenWeather API, parse information etc.
            response = utils.handle_weather_request(
                data,
                constants.COUNTRY_CODES,
                config.URL,
                config.CURRENT_WEATHER_ENDPOINT,
                config.API_KEY,
                constants.DATE_RG,
                constants.TIME_RG
            )
            return response
        except Exception:
            return json.dumps({
                'status': 'failure',
                'error_message': 'Error handling weather request',
                'traceback': str(traceback.format_exc())
            })
    else:
        return json.dumps({
            'status': 'failure',
            'error_message': 'Please send city and country information through a GET request',
            'traceback': str(traceback.format_exc())
        })


if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT)
