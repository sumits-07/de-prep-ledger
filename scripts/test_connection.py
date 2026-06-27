from sqlalchemy import create_engine, text
import sys

DB_URI= 'postgresql://postgres:scooby@localhost:5432/weather_db'


def test_database_connection():
	print("Attempting to connect to the databse...")
	try:
		engine=create_engine(DB_URI)
		with engine.connect() as connection:
			result = connection.execute(text("SELECT version();"))
			db_version = result.scalar()

			print("Connection Successful! You are good to go!!")
			print(f"Database Engine: {db_version}")

	except Exception as e:
		print("Connection failed. The error cased is:")
		print("_"*40)
		print(e)
		sys.exit(1)

if __name__ == "__main__":
	test_database_connection()
