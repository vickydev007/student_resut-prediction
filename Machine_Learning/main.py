import numpy as np
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from logics import students, validate

app = FastAPI()
model = joblib.load("predict.pkl")
scaler = joblib.load("scaler.pkl") 



class StudentInput(BaseModel):
    reg_no: str

    unit1_test_mark: float
    unit2_test_mark: float
    unit3_test_mark: float
    unit4_test_mark: float
    unit5_test_mark: float

    cat1_mark: float
    cat2_mark: float

    assignment1_mark: float
    assignment2_mark: float
    assignment3_mark: float
    assignment4_mark: float
    assignment5_mark: float

    attendance: float
    lms_activity: float

@app.get("/")
def home():
    return {"message": "Student Performance Prediction API is running"}

@app.post("/predict")
def predict(student:StudentInput):
    feature_cols = [
        "unit1_test_mark","unit2_test_mark","unit3_test_mark",
        "unit4_test_mark","unit5_test_mark",
        "cat1_mark","cat2_mark",
        "assignment1_mark","assignment2_mark","assignment3_mark",
        "assignment4_mark","assignment5_mark",
        "attendance","lms_activity"
    ]

    # 1. Build DataFrame (CRITICAL)
    X = pd.DataFrame([[getattr(student, col) for col in feature_cols]],
                     columns=feature_cols)

    x=X[["unit1_test_mark","unit2_test_mark","unit3_test_mark",
        "unit4_test_mark","unit5_test_mark",
        "cat1_mark","cat2_mark",
        "assignment1_mark","assignment2_mark","assignment3_mark",
        "assignment4_mark","assignment5_mark"]]
    x = x.astype(float)
    data=scaler.transform(x)
    prediction=model.predict(data)[0]
    probability=model.predict_proba(data)[0][1]
    result = "Pass" if prediction==1 else "Fail"

    attendance_status=students(student.attendance)
    attendance_status= "The person Attedance is low." if attendance_status=="low" else "The person attendance will be continue in the course." if attendance_status=="Continue" else "The person will drop the course."
    unit_test=[student.unit1_test_mark, student.unit2_test_mark, student.unit3_test_mark, student.unit4_test_mark, student.unit5_test_mark]
    weak_units=validate(unit_test)

    return {"registration_number": student.reg_no,
            "prediction": f"The student will {result} with a probability of {probability:.2f}",
            "Course Status": attendance_status,

            "weak_units": weak_units}
