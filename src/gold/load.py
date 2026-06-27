import pandas as pd
from sqlalchemy import create_engine, text
import sys
import time

DB_URI= "postgresql://postgres:scooby@localhost:5432/weather_db"
silver_level_file = 'silver_weather_data.parquet'


def load_to_gold():
	print("Loading transformed data into  Postgres in...")
	for i in range(3,0,-1):
		print(i)
		time.sleep(0.5)

	try:
		df = pd.read_parquet(silver_level_file)

		dim_location_df = df[['location_id','latitude','longitude','timezone']].drop_duplicates()
		dim_location_df['city_name']='Greater Noida'


		fact_df = df.rename(columns={
					'time':'forecast_time',
					'temperature_2m':'temperature_celsius',
					'relative_humidity_2m':'humidity_percentage',
					'cloud_cover':'cloud_cover_percentage',
					'precipitation_probability':'precipitation_probability',
					'visibility':'visibility_in_m'
					})[['location_id','forecast_time','temperature_celsius','humidity_percentage','cloud_cover_percentage','precipitation_probability','weather_code','visibility_in_m','is_day']]

		fact_df['is_day']=fact_df['is_day'].astype(bool)

		engine = create_engine(DB_URI)
		with engine.begin() as conn:

			#Dimension table
			dim_location_df.to_sql('temp_dim_location', conn, if_exists='replace', index=False)
			conn.execute(text("""
				INSERT INTO dim_location (location_id, latitude,
				longitude,city_name,timezone)
				SELECT
					location_id,
					latitude,
					longitude,
					city_name,
					timezone
				FROM temp_dim_location
				ON CONFLICT (location_id) DO NOTHING;
				"""))


			conn.execute(text("DROP TABLE temp_dim_location"))


			#Fact table
			fact_df.to_sql("temp_fact_df", conn, if_exists='replace', index=False)
			conn.execute(text("""
				INSERT INTO fact_weather (location_id,forecast_time,temperature_celsius,
				humidity_percentage,cloud_cover_percentage,precipitation_probability,
				weather_code,visibility_in_m,is_day)
				SELECT
					location_id,
					CAST(forecast_time AS TIMESTAMP),
					temperature_celsius,
					humidity_percentage,
					cloud_cover_percentage,
					precipitation_probability,
					weather_code,
					visibility_in_m,
					is_day
				FROM temp_fact_df
				ON CONFLICT (location_id,forecast_time)
				DO UPDATE SET
					temperature_celsius=EXCLUDED.temperature_celsius,
					humidity_percentage=EXCLUDED.humidity_percentage,
                                        cloud_cover_percentage=EXCLUDED.cloud_cover_percentage,
                                        precipitation_probability=EXCLUDED.precipitation_probability,
                                        weather_code=EXCLUDED.weather_code,
                                        visibility_in_m=EXCLUDED.visibility_in_m
				"""))
			conn.execute(text("DROP TABLE temp_fact_df"))


		print("Yayy!! Gold Layer Created Successfully")



	except Exception as e:
		print(f"CRITICAL ERROR: {e}")
		raise



if __name__=="__main__":
	load_to_gold()
