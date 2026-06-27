import json
import pandas as pd
#import time


def transform_weather_data():
	#print("Transfor sequence starting in....")
	#for i in range(3,0,-1):
	#	print (i)
	#	time.sleep(0.5)

	try:
		# Opening the Bronze layer file
		with open("raw_weather_data.json","r") as file:
			raw_data = json.load(file)

		lat= raw_data.get("latitude")
		lon= raw_data.get("longitude")
		tz=raw_data.get("timezone","Unknown")

		# Generating the Primary/Foreign key mapping
		location_id = f"{lat}_{lon}"
		print(f"Extracted Geographic Context: Loaction ID [{location_id}]")

		if 'hourly' not in raw_data:
			raise KeyError("The 'hourly' data block is missing from the payload")
		df=pd.DataFrame(raw_data['hourly'])


		df['location_id'] = location_id
		df['latitude']=lat
		df['longitude']=lon
		df['timezone']=tz



		print("Data flattening successful")
		print("_"*39)
		print(df.head())
		df.to_parquet('silver_weather_data.parquet',index=False)
		print("Checkpoint reached...Silver layer created")




	except FileNotFoundError:
		print("CRITICAL ERROR: raw data file not found, run transform.py first")

	except Exception as e:
		print(f"CRITICAL ERROR: Error occured during tranformation - {e}")



transform_weather_data()
