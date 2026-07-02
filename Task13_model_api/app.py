from fastapi import FastAPI
from pydantic import BaseModel
import joblib

model = joblib.load("trained_model.joblib")

app = FastAPI()

class Patient(BaseModel):
    features: list

@app.get("/")
def home():
    return {"message": "Binary Classification API Running"}

@app.post("/predict")
def predict(patient: Patient):

    prediction = model.predict([patient.features])[0]
    probability = model.predict_proba([patient.features])[0][1]

    return {
        "prediction": int(prediction),
        "probability": float(probability)
    }