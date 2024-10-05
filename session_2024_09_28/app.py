from flask import Flask, request, jsonify
from weather import WeatherRecord, WeatherResponse
import re

app = Flask(__name__)

digit_pattern = re.compile(r'-?\d+')
records = WeatherRecord.load_from_file()


@app.get('/search')
def search():
    name = request.args.get('name', default='')
    page = request.args.get('page', default='1')
    per_page = request.args.get('per_page', default='10')
    min_temp = request.args.get('min_temp')
    max_temp = request.args.get('max_temp')

    if min_temp is not None:
        if digit_pattern.fullmatch(min_temp):
            min_temp = int(min_temp)
        else:
            return error_response('Invalid minimum temperature.')
    if max_temp is not None:
        if digit_pattern.fullmatch(max_temp):
            max_temp = int(max_temp)
        else:
            return error_response('Invalid minimum temperature.')

    if per_page.isdigit():
        per_page = int(per_page)
    else:
        return error_response('Invalid number of results per page.')

    if not page.isdigit() or int(page) == 0:
        return error_response('Invalid page number.')
    else:
        page = int(page)

    return jsonify(WeatherResponse(page, per_page, name, records, min_temp, max_temp).to_dict())


def error_response(message):
    return jsonify({'error': f'{message}'})


if __name__ == '__main__':
    app.json.ensure_ascii = False
    app.json.sort_keys = False
    app.run(debug=True)
