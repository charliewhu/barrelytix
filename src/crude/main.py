import os


API_KEY = os.environ.get("API_KEY")
API_URL = f"https://api.eia.gov/v2/crude-oil-imports/data/?frequency=monthly&data[0]=quantity&start=2023-01&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000&api_key={API_KEY}"
API_URL = f"https://api.eia.gov/v2/crude-oil-imports/data/?api_key={API_KEY}"
