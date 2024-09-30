import duckdb
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    root_mean_squared_error,
)

import db
import services


def create_linear_regression():
    """
    Use data from database to create a linear regression
    and save to a file
    """
    with duckdb.connect(db.DATABASE_URL, read_only=True) as conn:
        df = services.get_merged_data(conn)

    # Shift the price column to create the target variable price at t+1
    df["next_price"] = df["price"].shift(-1)
    df.dropna(inplace=True)

    # Define independent variables at time t
    X = df[["import_quantity", "production"]]

    # Define the target variable at time t+1
    y = df["next_price"]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=1,
    )

    # Fit the model to the training data
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Save model
    joblib.dump(model, "linear_regression_model.pkl")
    y_pred = model.predict(X_test)

    # Model evaluation
    rmse = root_mean_squared_error(y_test, y_pred)
    print(f"Root Mean Squared Error: {rmse}")
    mae = mean_absolute_error(y_test, y_pred)
    print(f"Mean Absolute Error: {mae}")
