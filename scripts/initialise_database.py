import os
import psycopg2 
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from src.db.models import DIM_WEATHER_CODE_TABLE_DDL, DIM_LOCATION_TABLE_DDL, FACT_WEATHER_TABLE_DDL


load_dotenv()

WMO_SEED_DATA = [
    (0, "Clear sky"),
    (1, "Mainly clear"),
    (2, "Partly cloudy"),
    (3, "Overcast"),
    (45, "Fog"),
    (48, "Depositing rime fog"),
    (51, "Drizzle: Light intensity"),
    (53, "Drizzle: Moderate intensity"),
    (55, "Drizzle: Dense intensity"),
    (56, "Freezing Drizzle: Light intensity"),
    (57, "Freezing Drizzle: Dense intensity"),
    (61, "Rain: Slight intensity"),
    (63, "Rain: Moderate intensity"),
    (65, "Rain: Heavy intensity"),
    (66, "Freezing Rain: Light intensity"),
    (67, "Freezing Rain: Heavy intensity"),
    (71, "Snow fall: Slight intensity"),
    (73, "Snow fall: Moderate intensity"),
    (75, "Snow fall: Heavy intensity"),
    (77, "Snow grains"),
    (80, "Rain showers: Slight"),
    (81, "Rain showers: Moderate"),
    (82, "Rain showers: Violent"),
    (85, "Snow showers: Slight"),
    (86, "Snow showers: Heavy"),
    (95, "Thunderstorm: Slight or moderate"),
    (96, "Thunderstorm with slight hail"),
    (99, "Thunderstorm with heavy hail")
]

def initialise_database():
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        port=os.environ.get("DB_PORT"),
        password=os.environ.get("DB_PASSWORD")
    )
    cursor = conn.cursor()

    try:
        print("Executing DDL statements from models.py...")
        cursor.execute(DIM_LOCATION_TABLE_DDL)
        cursor.execute(DIM_WEATHER_CODE_TABLE_DDL)
        cursor.execute(FACT_WEATHER_TABLE_DDL)


        print("Populating the static dim_weather_code table with WMO seed data...")
        insert_query = "INSERT INTO dim_weather_code (weather_code, description) VALUES %s ON CONFLICT (weather_code) DO NOTHING"

        execute_values(cursor, insert_query, WMO_SEED_DATA)

        conn.commit()
        print("Database Infrastrucre successfully creasted and dim_weather_code table populated with the WMO seed data.")

    except Exception as e:
        conn.rollback()
        print(f"CRITICAL ERROR occured during Db initialisation: {e}")
    
    finally:
        cursor.close()
        conn.close()
    
if __name__=="__main__":
    initialise_database()