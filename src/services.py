import datetime
import duckdb
import joblib
from sklearn.linear_model import LinearRegression


def get_model(filename: str) -> LinearRegression:
    return joblib.load(filename)


def get_latest_load(conn: duckdb.DuckDBPyConnection) -> datetime.datetime:
    result = conn.query("select max(inserted_at) from eia._dlt_loads").fetchone()
    if result:
        return result[0]

    return datetime.datetime(1900, 1, 1)


def get_prices(conn: duckdb.DuckDBPyConnection):
    return conn.query("""
        select 
            period,
            value as price
        from eia.prices
        order by period
    """).df()


def get_imports(conn: duckdb.DuckDBPyConnection):
    return conn.query("""
            select 
                period,
                sum(cast(quantity as integer)) as import_quantity
            from eia.imports 
            where destination_type = 'RF'
            group by period
            order by period
        """).df()


def get_production(conn: duckdb.DuckDBPyConnection):
    return conn.query("""
            select 
                period,
                sum(cast(value as integer)) * 1000 as production
            from eia.production 
            group by period
            order by period
        """).df()


def get_stocks(conn: duckdb.DuckDBPyConnection):
    return conn.query("""
            select 
                period,
                sum(cast(value as integer)) * 1000 as stocks
            from eia.production 
            group by period
            order by period
        """).df()


def get_merged_data(conn: duckdb.DuckDBPyConnection):
    prices = get_prices(conn)
    imports = get_imports(conn)
    production = get_production(conn)

    merged = prices.merge(imports, on="period", how="inner")
    merged = merged.merge(production, on="period", how="inner")

    return merged
