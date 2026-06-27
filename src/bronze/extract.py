import requests
import json
import time

api_url = "https://historical-forecast-api.open-meteo.com/v1/forecast?"

payload={
	"latitude":28.47,
	"longitude":77.03,
	"past_days":90,
	"forecast_days":0,
	"hourly":["temperature_2m","relative_humidity_2m","cloud_cover","precipitation","weather_code","visibility","is_day"]
	,"timezone":"Asia/Calcutta"
}

def extract_weather_data():
	#print("Initialising extraction sequence starting in...")
	#for i in range(3,0,-1):
	#	print(i)
	#	time.sleep(1)

	response = requests.get(api_url, params=payload)


	if response.status_code==200:

		data = response.json()
		with open('raw_weather_data.json','w') as file:
			json.dump(data, file, indent=4)
		print("Checkpoint reached...Raw JSON payload written to raw_weather_data.json successfully - Bronze Layer ready")
	else:
		print(f"Maydyay...Mayday...Mayday...CRITICAL FAILURE: API returned status code {response.status_code}")
		return


if __name__ == "__main__":
	extract_weather_data()
