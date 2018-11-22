#Weather information

##Get multiple day forecasts or the current weather!

###Get it up and running
- In order to run the script, you need to have Python3 installed on your system.
- Before running the script, please install the required Python modules by opening a terminal, going into the project folder and running the following command:

		pip3 install -r requirements.txt

- To run the script, go into the src folder and run the following command:

		python3 web_service.py

###The APIs
There are two APIs:

####Get current weather
Endpoint: `/api/current-weather`

Request type: `GET`

Parameters: `city name`, `country code` (according to ISO 3166 country codes)

Sample request: `http://127.0.0.1:3500/api/current-weather?city=Islamabad&country=PK`



####Get multiple day forecast
Endpoint: `/api/multiple-day-forecast`

Request type: `POST`

Parameters: `city name`, `country code` (according to ISO 3166 country codes)

Sample request: `http://127.0.0.1:3500/api/multiple-day-forecast`

Sample input:
	```{
		"city": "Stockholm",
		"country": "SE"
	}```