from typing import Dict, TypedDict

from pandas import Timestamp

def PredictionData(TypedDict):
    from_dt:Timestamp
    ref_dt: Timestamp
    run_dt: Timestamp
    data: Dict


def Prediction(PredictionData):
    prediction_id: str