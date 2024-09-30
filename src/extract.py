import dlt

from sources import eia


def pipeline():
    pipeline = dlt.pipeline(
        pipeline_name="black",  # database name
        dataset_name="eia",  # schema name
        destination="duckdb",
        progress="log",
    )

    load_info = pipeline.run(eia.source)
    print(f"{load_info=}")


if __name__ == "__main__":
    pipeline()
