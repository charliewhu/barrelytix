import os
import httpx
import dlt

API_KEY = os.environ.get("API_KEY")
API_URL = f"https://api.eia.gov/v2/crude-oil-imports/data/?api_key={API_KEY}"
API_EXAMPLE_PARAMS = "frequency=monthly&data[0]=quantity&start=2023-01&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"
DB_PATH = "db.duckdb"


# Create a dlt pipeline that will load
# chess player data to the DuckDB destination
pipeline = dlt.pipeline(
    pipeline_name="chess_pipeline", destination="duckdb", dataset_name="player_data"
)


def get_data_from_chess_api():
    # Grab some player data from Chess.com API
    data = []
    for player in ["magnuscarlsen", "rpragchess"]:
        response = httpx.get(f"https://api.chess.com/pub/player/{player}")
        response.raise_for_status()
        data.append(response.json())

    return data


def main():
    if not os.path.exists(DB_PATH):
        print("hi")

    data = get_data_from_chess_api()

    # Extract, normalize, and load the data
    load_info = pipeline.run(data, table_name="player")


if __name__ == "__main__":
    main()
