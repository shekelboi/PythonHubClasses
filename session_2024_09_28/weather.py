import json
import math
import re


class WeatherRecord:
    weather_pattern = r'(-?\d+)'
    wind_pattern = r'Wind: (\d+)'
    humidity_pattern = r'Humidity: (\d+)'

    @staticmethod
    def load_from_file(path='hackerrank_weather.json'):
        with open(path, encoding='utf-8') as file:
            data = json.load(file)
            records = []

            for record in data:
                records.append(WeatherRecord(record['name'], record['weather'], record['status']))
            return records

    def __init__(self, name, weather, status):
        self.name = name
        self.weather = int(re.match(WeatherRecord.weather_pattern, weather).groups()[0])
        self.wind = int(re.match(WeatherRecord.wind_pattern, status[0]).groups()[0])
        self.humidity = int(re.match(WeatherRecord.humidity_pattern, status[1]).groups()[0])

    def to_dict(self):
        return {
            'name': self.name,
            'weather': f'{self.weather} degree',
            'status': [
                f'Wind: {self.wind}Kmph',
                f'Humidity: {self.humidity}%'
            ]
        }


class WeatherResponse:
    def __init__(self, page: int, per_page: int, name: str, data: [WeatherRecord], min_temp=None, max_temp=None):
        self.page = page
        self.per_page = per_page
        self.data = WeatherResponse.filter_data(data, name, min_temp, max_temp)
        self.total = len(self.data)
        self.total_pages = math.ceil(self.total / self.per_page)

    @staticmethod
    def filter_data(data, name=None, min_temp=None, max_temp=None):
        print()
        filtered = []
        for record in data:
            print(name)
            if (name is None or re.search(re.escape(name), record.name, flags=re.IGNORECASE)) and \
                    (min_temp is None or record.weather >= min_temp) and \
                    (max_temp is None or record.weather <= max_temp):
                filtered.append(record)
        return filtered

    def select_page(self, page: int) -> [WeatherRecord]:
        return self.data[(page - 1) * self.per_page:page * self.per_page]

    def to_dict(self):
        return {
            'page': self.page,
            'per_page': self.per_page,
            'total': self.total,
            'total_pages': self.total_pages,
            'data': [r.to_dict() for r in self.select_page(self.page)]
        }
