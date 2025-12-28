from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle

app = FastAPI()

# ✅ CORS MUST BE HERE (after app = FastAPI())
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all (safe for demo)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# load model
with open("ets_yellowstone_model.pkl", "rb") as f:
    model = pickle.load(f)

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/forecast")
def forecast(months: int = 6):
    preds = model.forecast(months)
    result = []
    for i, val in enumerate(preds):
        result.append({
            "month": i + 1,
            "visits": float(val)
        })
    return {"forecast": result}
