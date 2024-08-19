import os
from dotenv import load_dotenv
import dlt

from rest_api import (
    rest_api_source,
)


load_dotenv(override=True)


eia_source = rest_api_source(
    {
        "client": {
            "base_url": "https://api.eia.gov/v2/",
            "headers": {},
        },
        "resource_defaults": {
            "endpoint": {
                "params": {
                    "api_key": os.getenv("API_KEY"),
                    "offset": "0",
                    # "length": "10000",
                    "frequency": "monthly",
                    "start": "2000-01",
                    # "sort": [
                    #     {
                    #         "column": "period",
                    #         "direction": "desc",
                    #     }
                    # ],
                },
            },
        },
        "resources": [
            {
                "name": "imports",
                "endpoint": {
                    "path": "crude-oil-imports/data",
                    "params": {},
                },
            },
            {
                "name": "prices",
                "endpoint": {
                    "path": "petroleum/pri/spt/data/",
                    "params": {
                        "facets[product][]": "EPCWTI",  # only WTI prices
                    },
                },
            },
            {
                "name": "production",
                "endpoint": {
                    "path": "petroleum/crd/crpdn/data",
                    "params": {},
                },
            },
            {
                "name": "net_imports",
                "endpoint": {
                    "path": "petroleum/move/neti/data",
                    "params": {
                        "facets[product][]": "EPC0",  # only crude oil
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
                    },
                },
            },
            {
                "name": "refinery_stocks",
                "endpoint": {
                    "path": "petroleum/stoc/ref/data",
                    "params": {
                        "facets[product][]": "EPC0",  # only crude oil
                    },
                },
            },
            {
                "name": "refinery_net_input",
                "endpoint": {
                    "path": "petroleum/pnp/wiup/data",
                    "params": {
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
                        "facets[productId][]": "57",  # only crude oil
                        "facets[activityId][1]": "1",  # production
                        "facets[activityId][2]": "2",  # or consumption
                    },
                },
            },
        ],
    }
)


def main():
    pipeline = dlt.pipeline(
        pipeline_name="black",  # database name
        dataset_name="eia",  # schema name
        destination="duckdb",
        progress="log",
    )

    load_info = pipeline.run(eia_source)
    print(load_info)


if __name__ == "__main__":
    main()
