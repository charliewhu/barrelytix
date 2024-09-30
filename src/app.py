import duckdb
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
import streamlit as st
import plotly.graph_objects as go

import db
import extract
import model
import services


@st.cache_resource
def load_model():
    # initialise database and regression model
    try:
        linear_model: LinearRegression = joblib.load("linear_regression_model.pkl")
        print("loading model again?")
    except FileNotFoundError:
        try:
            model.create_linear_regression()
            linear_model: LinearRegression = joblib.load("linear_regression_model.pkl")
        except duckdb.IOException:
            extract.pipeline()
            model.create_linear_regression()
            linear_model: LinearRegression = joblib.load("linear_regression_model.pkl")

    return linear_model


if __name__ == "__main__":
    st.set_page_config(page_title="Barrelytix")
    linear_model = load_model()
    st.title("Barrelytix")

    with duckdb.connect(db.DATABASE_URL, read_only=True) as conn:
        merged = services.get_merged_data(conn)

    st.divider()

    with st.sidebar:
        st.markdown("## Model Parameters")
        import_quantity = st.number_input(
            label="Import Quantity",
            value=20_000,
            min_value=0,
            step=1000,
        )
        production = st.number_input(
            label="Production",
            value=30_000_000,
            min_value=0,
            step=1_000_000,
        )

    st.markdown("### Next predicted price (given the input parameters)")

    price = linear_model.predict(
        pd.DataFrame(
            {
                "import_quantity": [import_quantity],
                "production": [production],
            }
        )
    )

    st.markdown(f"## ${price[0]:.2f}")

    st.divider()

    fig = go.Figure()

    # Adding price trace
    fig.add_trace(
        go.Scatter(
            x=merged["period"],
            y=merged["price"],
            mode="lines",
            name="Price",
            yaxis="y1",
        )
    )

    # Adding quantity trace
    fig.add_trace(
        go.Scatter(
            x=merged["period"],
            y=merged["import_quantity"],
            mode="lines",
            name="Quantity",
            yaxis="y2",
        )
    )

    # Create secondary y-axis
    fig.update_layout(
        title="Prices and Imports over Time",
        xaxis=dict(title="Period"),
        yaxis=dict(title="Price", side="left"),
        yaxis2=dict(
            title="Import Quantity",
            side="right",
            overlaying="y",
            showgrid=False,
        ),
    )

    st.plotly_chart(fig)

    st.divider()

    st.markdown("### Source data")
    st.dataframe(merged)

    with duckdb.connect(db.DATABASE_URL, read_only=True) as conn:
        x = services.get_latest_load(conn)
        st.button(
            f"Fetch New Data (Takes ~30 seconds. Last Fetched: {x:%d-%m-%Y})",
            on_click=extract.pipeline,
        )

    st.button(
        "Recalculate model",
        on_click=model.create_linear_regression,
    )

    st.write("All data is from the EIA API")
