DIM_LOCATION_TABLE_DDL="""
CREATE TABLE IF NOT EXISTS dim_location (
    location_id VARCHAR(50) PRIMARY KEY,
    latitude FLOAT NOT NULL,
	logitude FLOAT NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

DIM_WEATHER_CODE_TABLE_DDL="""
CREATE TABLE IF NOT EXISTS dim_weather_code(
    weather_code INT PRIMARY KEY,
	description VARCHAR(255) NOT NULL
	);
"""


FACT_WEATHER_TABLE_DDL="""
CREATE TABLE IF NOT EXISTS fact_weather (
    location_id VARCHAR(50) REFERENCES dim_location(location_id),
	forecast_time TIMESTAMP NOT NULL,
	temperature_celsius FLOAT,
	humidity_percentage FLOAT,
	cloud_cover_percentage FLOAT,
	precipitation_probability FLOAT,
	weather_code INT REFERENCES dim_weather_code(weather_code),
	visibility_in_m FLOAT,
	is_DAY BOOLEAN,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (location_id,forecast_time)); --Composite primary key
"""