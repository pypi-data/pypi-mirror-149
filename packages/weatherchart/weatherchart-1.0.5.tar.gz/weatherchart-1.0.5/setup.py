# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['weatherchart']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'weatherchart',
    'version': '1.0.5',
    'description': 'Generate chart image based on 7 day forecast form a given location',
    'long_description': '# 7 Day Weather forecast\n\nThe module provides a 7 day weather forecast from the Open Weather Map and then converted to am image using quickcharts.io  See a full article from [PythonHowToProgram](https://pythonhowtoprogram.com/get-weather-forecasts-and-show-it-on-a-chart-using-python-3/)\n\n\n## What problem does this solve?\nThe module will help to return a 7 day weather forecast for a given location either as a dictionary, a chart image file, or a web link with the chart image\n\n### How does it do this?\nThere are three key services that are used for this module:\n\n1. The `geopy` library to convert a string to lat-long\n2. [Open Weather Map](https://openweathermap.org/) online service (you can get an API key through a free account in the profile section)\n3. Then finally from [QuickCharts](https://quickchart.io/) to convert the time series weather data into a chart\n\n### How do you install this?\nMCLogger is avaialble through PyPi and you may use pip:\n\n```\n\tpip install weatherchart\n```\n\nOr, through git:\n```\n\tgit clone https://github.com/pub12/weatherchart.git\n```\n\n\n### How do you use weatherchart?\nThe weatherchart library is super easy to use.  You need to simply pass the Open Weather API key, a timezone, and then a location string.  A URL will be returned of the chart or saved as a file\n\n```\nfrom weatherchart import WeatherChart\n\nwchart = WeatherChart(\'<open weather map token>\', \'Asia/Hong_Kong\')\nprint( wchart.get_forecast_chart_image_by_loc(\'Tokyo\', \'out_file.jpg\' ) )\n```\n\n### Class Methods overview\n- #### constructor(self, map_key, tz_location=\'Asia/Singapore\'):\n\tConstructor must include the Open Weather MAP API key, and also a timezone.  The timezone list can be found on the [Wiki Timezone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) page.  The reason for the timzone is to ensure the right time period is extract for the next 7 days\n\n- #### get_full_weather_data(self, lat, long):\n    Return a dictionary with weather a full detailed range of data (temperature, min, max, humidity and many more) for next 7 days including today.  The location must be provided as a lat long.  \n\n- #### get_forecast_by_location(self, loc_string):\n    Return a dictionary with weather data (temperature, min, max, humidity) for next 7 days including today.  The location must be provided as a location description (e.g. "Seattle", "New York, New York").  Output is the same as the method `get_forecast()`\n\n- #### get_forecast(self, lat, long):\n    Return a dictionary with weather data (temperature, min, max, humidity) for next 7 days including today.  The location must be provided as a lat long.  \n    A ditionary will be returned with the following:\n\n    ```\n    {\n        \'temp\': <float>,\n        \'temp_min\':  <float>,\n        \'temp_max\':  <float>,\n        \'wind_speed\':  <float>,\n        \'humidity\':  <float> \n    }\n    ```\n\n- #### get_forecast_chart_image_by_loc( self, loc_string,   output_file=None):\n    This will return an image with a chart showing the 7 day forecast.  If a filename is provided then the image will be saved as an image as well (.jpg).  Input is a location sring and the function will return a URL string.  An example output below:\n\n    ![7 day forecast for Tokyo, Japan](https://quickchart.io/chart/render/zf-cf915d3f-de6b-41e1-9998-687610dd06e1)\n\n',
    'author': 'pub12',
    'author_email': 'pubudu79@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pubs12/weatherchart',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
