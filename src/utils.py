import re
import json
import requests
import traceback


def handle_weather_request(data, country_codes, url, endpoint, api_key, date_rg, time_rg):
    try:
        city = data['city']
        country = data['country']
    except KeyError:
        return json.dumps({
            'status': 'failure',
            'error_message': 'Invalid/missing data',
            'traceback': str(traceback.format_exc())
        })
    # check if country is specified in proper country code
    if country.upper() not in country_codes:
        return json.dumps({
            'status': 'failure',
            'error_message': 'Country code not valid'
        })

    # create URL for GET request to OpenWeather API
    url = "%s%s?q=%s,%s&mode=json&APPID=%s" % (url, endpoint, city, country, api_key)
    # send GET request to OpenWeather API
    try:
        api_response = requests.get(url)
    # can add multiple specific exceptions here
    except Exception:
        return json.dumps({
            'status': 'failure',
            'error_message': 'Unable to get a response from OpenWeather API',
            'traceback': str(traceback.format_exc())
        })

    # verify that OK response code is returned
    if api_response.status_code == 200:
        api_response_data = api_response.json()

        try:
            response = get_weather_information_from_response(
                api_response_data,
                date_rg,
                time_rg
            )
        except Exception:
            return json.dumps({
                'status': 'failure',
                'error_message': 'Unable to parse information from OpenWeather API response',
                'traceback': str(traceback.format_exc())
            })

        # return successful response
        return json.dumps({
            'status': 'success',
            'response': response
        })
    else:
        return json.dumps({
            'status': 'failure',
            'status_code': str(api_response.status_code),
            'error_message': 'OpenWeather API did not return correct response',
            'traceback': str(traceback.format_exc())
        })


def get_weather_information_from_response(api_response_data, date_rg, time_rg):
    response = dict()
    # get location information
    if 'city' in api_response_data.keys():
        response['city'] = api_response_data['city']['name']
        response['country'] = api_response_data['city']['country']
        response['coordinates'] = dict()
        response['coordinates']['longitude'] = api_response_data['city']['coord']['lon']
        response['coordinates']['latitude'] = api_response_data['city']['coord']['lat']
    else:
        response['city'] = api_response_data['name']
        response['country'] = api_response_data['sys']['country']
        response['coordinates'] = dict()
        response['coordinates']['longitude'] = api_response_data['coord']['lon']
        response['coordinates']['latitude'] = api_response_data['coord']['lat']

    # get weather information
    if 'list' in api_response_data.keys():
        response['weather'] = []
        for weather_data in api_response_data['list']:
            unit_weather_data = extract_unit_weather_information(weather_data, date_rg, time_rg)
            response['weather'].append(unit_weather_data)
    else:
        unit_weather_data = extract_unit_weather_information(api_response_data, date_rg, time_rg)
        response['weather'] = unit_weather_data

    return response


def extract_unit_weather_information(weather_data, date_rg, time_rg):
    unit_weather_data = dict()
    # date and time information is joined together in the api response. Separate them through regex if
    # possible. Otherwise, use date and time as is
    if 'date_txt' in weather_data.keys():
        date_time = weather_data['dt_txt']
        date = re.search(date_rg, date_time)
        time = re.search(time_rg, date_time)
        if date and time:
            unit_weather_data['date'] = date.group(0)
            unit_weather_data['time'] = time.group(0)
        else:
            unit_weather_data['date_time'] = date_time
    else:
        unit_weather_data['date'] = weather_data['dt']

    # get weather information
    unit_weather_data['min_temperature'] = weather_data['main']['temp_min']
    unit_weather_data['max_temperature'] = weather_data['main']['temp_max']
    unit_weather_data['humidity'] = weather_data['main']['humidity']
    unit_weather_data['pressure'] = weather_data['main']['pressure']

    # get state and description of weather
    unit_weather_data['weather'] = []
    for weather_elem in weather_data['weather']:
        unit_weather_data['weather'].append({
            'state': weather_elem['main'],
            'description': weather_elem['description']
        })

    # get wind information
    unit_weather_data['wind_speed'] = weather_data['wind']['speed']

    return unit_weather_data
