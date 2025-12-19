from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI(title="Churn Prediction API")

# Load model
model = joblib.load("../models/random_forest_model_1.pkl")

# Input schema (RAW user input)
class CustomerInput(BaseModel):
    Contract: int              # 0,1,2
    tenure: int
    OnlineSecurity: int        # 0/1
    TechSupport: int           # 0/1
    TotalCharges: float
    OnlineBackup: int          # 0/1
    MonthlyCharges: float
    PaperlessBilling: int      # 0/1
    DeviceProtection: int      # 0/1
    Dependents: int            # 0/1


@app.post("/predict")
def predict(data: CustomerInput):

    # Arrange features EXACTLY as model expects
    input_array = np.array([[  
        data.Contract,
        data.tenure,
        data.OnlineSecurity,
        data.TechSupport,
        data.TotalCharges,
        data.OnlineBackup,
        data.MonthlyCharges,
        data.PaperlessBilling,
        data.DeviceProtection,
        data.Dependents
    ]])

    prediction = model.predict(input_array)[0]
    probability = model.predict_proba(input_array)[0][1]

    return {
        "churn_prediction": int(prediction),
        "churn_probability": round(float(probability), 3)
    }
