# 7 Day Weather forecast

The module provides a 7 day weather forecast from the Open Weather Map and then converted to am image using quickcharts.io  See a full article from [PythonHowToProgram](https://pythonhowtoprogram.com/get-weather-forecasts-and-show-it-on-a-chart-using-python-3/)


## What problem does this solve?
The module will help to return a 7 day weather forecast for a given location either as a dictionary, a chart image file, or a web link with the chart image

### How does it do this?
There are three key services that are used for this module:

1. The `geopy` library to convert a string to lat-long
2. [Open Weather Map](https://openweathermap.org/) online service (you can get an API key through a free account in the profile section)
3. Then finally from [QuickCharts](https://quickchart.io/) to convert the time series weather data into a chart

### How do you install this?
MCLogger is avaialble through PyPi and you may use pip:

```
	pip install weatherchart
```

Or, through git:
```
	git clone https://github.com/pub12/weatherchart.git
```


### How do you use weatherchart?
The weatherchart library is super easy to use.  You need to simply pass the Open Weather API key, a timezone, and then a location string.  A URL will be returned of the chart or saved as a file

```
from weatherchart import WeatherChart

wchart = WeatherChart('<open weather map token>', 'Asia/Hong_Kong')
print( wchart.get_forecast_chart_image_by_loc('Tokyo', 'out_file.jpg' ) )
```

### Class Methods overview
- #### constructor(self, map_key, tz_location='Asia/Singapore'):
	Constructor must include the Open Weather MAP API key, and also a timezone.  The timezone list can be found on the [Wiki Timezone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) page.  The reason for the timzone is to ensure the right time period is extract for the next 7 days

- #### get_full_weather_data(self, lat, long):
    Return a dictionary with weather a full detailed range of data (temperature, min, max, humidity and many more) for next 7 days including today.  The location must be provided as a lat long.  

- #### get_forecast_by_location(self, loc_string):
    Return a dictionary with weather data (temperature, min, max, humidity) for next 7 days including today.  The location must be provided as a location description (e.g. "Seattle", "New York, New York").  Output is the same as the method `get_forecast()`

- #### get_forecast(self, lat, long):
    Return a dictionary with weather data (temperature, min, max, humidity) for next 7 days including today.  The location must be provided as a lat long.  
    A ditionary will be returned with the following:

    ```
    {
        'temp': <float>,
        'temp_min':  <float>,
        'temp_max':  <float>,
        'wind_speed':  <float>,
        'humidity':  <float> 
    }
    ```

- #### get_forecast_chart_image_by_loc( self, loc_string,   output_file=None):
    This will return an image with a chart showing the 7 day forecast.  If a filename is provided then the image will be saved as an image as well (.jpg).  Input is a location sring and the function will return a URL string.  An example output below:

    [7 day forecast for Tokyo, Japan](https://quickchart.io/chart/render/zf-cf915d3f-de6b-41e1-9998-687610dd06e1)

