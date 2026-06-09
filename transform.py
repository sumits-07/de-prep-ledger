import json
import pandas as pd
import time


def transform_weather_data():
	print("Transfor sequence starting in....")
	for i in range(3,0,-1):
		print (i)
		time.sleep(0.5)

	# Opening the Bronze layer file
	with open("raw_weather_data.json","r") as file:
		raw_data = json.load(file)

	# We just need the 'hourly' dictionary
	hourly_forecast = raw_data['hourly']

	#injecting the dictionary into pandas to flatten it
	df = pd.DataFrame(hourly_forecast)

	print("Data flattening successful")
	print("_"*39)
	print(df.head())
	df.to_parquet('silver_weather_data.paraquet',index=False)
	print("Checkpoint reached...Silver layer created")

	return df


transform_weather_data()
