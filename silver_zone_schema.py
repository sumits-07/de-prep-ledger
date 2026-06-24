import pandas as pd
import json
import os


def export_schema_pandas():
	input_file_path = 'silver_weather_data.parquet'
	output_file_path='silver_schema.json'

	print(f"Initialising schema extraction on {output_file_path} using pandas...")
	try:
		df=pd.read_parquet(input_file_path)
		output={
			"column_names":df.columns.tolist(),
			"dtypes":df.dtypes.astype(str).to_dict(),
			"record_count":len(df)
			}

		with open(output_file_path, 'w') as f:
			json.dump({"Description":output}, f,indent=4)

		print(f"Mission Accompolished: Schema successfully exported to {output_file_path}")

		exact_location=os.path.abspath(output_file_path)
		print(f"File stored at location: {exact_location}")

	except FileNotFoundError:
		print(f"CRITICAL ERROR: {input_file_path} not  found. I guess tranform.py did not run or failed to run")
		sys.exit(1)

	except Exception as e:
		print(f"CRITICAL ERROR: {e}")
		sys.exit(1)

if __name__ == "__main__":
	export_schema_pandas()
