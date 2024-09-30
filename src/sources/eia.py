import os
from dotenv import load_dotenv

from dlt.sources.rest_api import rest_api_source


load_dotenv(override=True)

source = rest_api_source(
    config={
        "client": {
            "base_url": "https://api.eia.gov/v2/",
            "headers": {},
        },
        "resource_defaults": {
            "endpoint": {
                "params": {
                    "api_key": os.getenv("API_KEY"),
                    "offset": "0",
                    "frequency": "monthly",
                    "start": "2000-01",
                },
            },
        },
        "resources": [
            {
                "name": "imports",
                "endpoint": {
                    "path": "crude-oil-imports/data",
                    "params": {
                        "data[0]": "quantity",  # quantity data
                    },
                },
            },
            {
                "name": "prices",
                "endpoint": {
                    "path": "petroleum/pri/spt/data/",
                    "params": {
                        "facets[product][]": "EPCWTI",  # only WTI prices
                        "data[0]": "value",  # price data
                    },
                },
            },
            {
                "name": "production",
                "endpoint": {
                    "path": "petroleum/crd/crpdn/data",
                    "params": {
                        "data[0]": "value",  # production data
                    },
                },
            },
            {
                "name": "net_imports",
                "endpoint": {
                    "path": "petroleum/move/neti/data",
                    "params": {
                        "facets[product][]": "EPC0",  # only crude oil
                        "data[0]": "value",
                    },
                },
            },
            {
                "name": "stocks",
                "endpoint": {
                    "path": "petroleum/stoc/wstk/data",
                    "params": {
                        "frequency": "weekly",
                        "facets[product][]": "EPC0",  # only crude oil
                        "facets[series][]": "WCRSTUS1",  # entire US
                        "data[0]": "value",
                    },
                },
            },
            {
                "name": "refinery_stocks",
                "endpoint": {
                    "path": "petroleum/stoc/ref/data",
                    "params": {
                        "facets[product][]": "EPC0",  # only crude oil
                        "data[0]": "value",
                    },
                },
            },
            {
                "name": "refinery_net_input",
                "endpoint": {
                    "path": "petroleum/pnp/wiup/data",
                    "params": {
                        "data[0]": "value",
                        "frequency": "weekly",
                        "facets[product][]": "EPC0",  # only crude oil
                    },
                },
            },
            {
                "name": "supply_estimates",
                "endpoint": {
                    "path": "petroleum/sum/sndw/data",
                    "params": {
                        "data[0]": "value",
                        "frequency": "weekly",
                        "facets[product][]": "EPC0",  # only crude oil
                        "facets[process][]": "FPF",  # field production
                    },
                },
            },
            {
                "name": "international_production",
                "endpoint": {
                    "path": "international/data",
                    "params": {
                        "data[0]": "value",
                        "facets[productId][]": "57",  # only crude oil
                        "facets[activityId][1]": "1",  # production
                        "facets[activityId][2]": "2",  # or consumption
                    },
                },
            },
        ],
    }
)
