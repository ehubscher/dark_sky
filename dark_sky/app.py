import datetime
import json
import numpy
import requests
from config import api_key
from datetime import datetime, timedelta, timezone, tzinfo
from numpy import array
from requests import Response
from typing import Dict, List


if __name__ == '__main__':
    # 1. Retrieve & display the following for dates Jan 14 2017
    # through Jan 20 2017 at 0:00am (midnight) Eastern Time.

    mtl_lattitude: float = 45.5017  # north
    mtl_longitude: float = -73.5673  # west

    est_offset: timedelta = timedelta(hours=-5)
    est_timezone: tzinfo = timezone(offset=est_offset)

    historical_data: Dict[str, Dict[str, str]] = dict()

    for day in range(14, 21):
        time: datetime = datetime(year=2017, month=1, day=day, hour=0, tzinfo=est_timezone)
        url: str = f'https://api.darksky.net/forecast/{api_key}/{mtl_lattitude},{mtl_longitude},{int(time.timestamp())}'

        resp: Response = requests.get(url=url)
        json_data: dict = resp.json()

        historical_data[time.strftime('%d-%m-%Y')] = json_data['daily']['data'][0]

    for data in historical_data.values():
        print(f'Date: {datetime.fromtimestamp(int(data["time"]), est_timezone).ctime()}')
        print(f'Cloud Cover: {data["cloudCover"]}')
        print(f'Pressure: {data["pressure"]}')
        print(f'Moon Phase: {data["moonPhase"]}')
        print(f'Min. Temperature: {data["temperatureMin"]}')
        print(f'Max Temperature: {data["temperatureMax"]}')
        print(f'Sunrise Time: {datetime.fromtimestamp(int(data["sunriseTime"]), est_timezone).ctime()}')
        print(f'Sunset Time: {datetime.fromtimestamp(int(data["sunsetTime"]), est_timezone).ctime()}')
        print('\r\n')

    # 2. Calculate & display by how many minutes/seconds the Sunrise Time
    # shifts daily on average.

    historical_sunrise: array = array(
        list(data['sunriseTime'] for data in historical_data.values())
    )

    sunrise_shift = list(
        map(lambda x: (float(x)/60), list(numpy.diff(numpy.diff(historical_sunrise))))
    )

    for day, shift in zip(range(14, 21), sunrise_shift):
        print(
            f'From {datetime(year=2017, month=1, day=day, hour=0, tzinfo=est_timezone).ctime()} '
            f'to '
            f'{datetime(year=2017, month=1, day=day + 1, hour=0, tzinfo=est_timezone).ctime()}, '
            f'the Sunrise Time shifted by {shift} minutes'
        )

    # 3. Find & display closest match of what date the sunrise will
    # occur at 7:00am Eastern Time? Suppose a linear trend from findings above.

    historical_sunrise_datetime: List[datetime] = list(
        datetime.fromtimestamp(float(data['sunriseTime']), est_timezone) for data in historical_data.values()
    )

    delta: Dict[datetime, int] = dict()

    for day, sunrise in zip(range(14, 21), historical_sunrise_datetime):
        temp_date: datetime = datetime(year=2017, month=1, day=day, hour=7, tzinfo=est_timezone)
        delta[sunrise] = (sunrise - temp_date).seconds

    print(f'\r\nDate with closest Sunrise Time to 7:00 am: {min(delta, key=delta.get)}')
