from fastapi import FastAPI, Query
import pickle
import pandas as pd

app = FastAPI()

# Load model once at startup
with open("ets_yellowstone_model.pkl", "rb") as f:
    model = pickle.load(f)

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/forecast")
def forecast(months: int = Query(12, ge=1, le=24)):
    forecast_values = model.forecast(months)

    future_dates = pd.date_range(
        start=pd.Timestamp.today().normalize() + pd.DateOffset(months=1),
        periods=months,
        freq="MS"
    )

    result = [
        {"date": str(d.date()), "visits": int(v)}
        for d, v in zip(future_dates, forecast_values)
    ]

    return {
        "park": "Yellowstone National Park",
        "months": months,
        "forecast": result
    }
