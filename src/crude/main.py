import dlt

from .sources import eia


def main():
    pipeline = dlt.pipeline(
        pipeline_name="black",  # database name
        dataset_name="eia",  # schema name
        destination="duckdb",
        progress="log",
    )

    load_info = pipeline.run(eia.source)
    print(load_info)


if __name__ == "__main__":
    main()
