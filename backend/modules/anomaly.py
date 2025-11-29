from fastapi import APIRouter
from pydantic import BaseModel
from sklearn.ensemble import IsolationForest
import numpy as np
from typing import List

router = APIRouter()

class AnomalyRequest(BaseModel):
    data: List[List[float]]
    contamination: float = 0.1

@router.post("/anomaly/detect")
async def detect_anomalies(request: AnomalyRequest) -> dict:
    """Detect anomalies in numerical data using Isolation Forest."""
    try:
        X = np.array(request.data)
        
        iso_forest = IsolationForest(
            contamination=request.contamination,
            random_state=42
        )
        predictions = iso_forest.fit_predict(X)
        scores = iso_forest.score_samples(X)
        
        anomalies = [
            {
                "index": i,
                "score": float(scores[i]),
                "is_anomaly": bool(predictions[i] == -1)
            }
            for i in range(len(predictions))
        ]
        
        return {
            "success": True,
            "data": {
                "anomalies": anomalies,
                "total_anomalies": int(sum(predictions == -1))
            },
            "error": None
        }
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}
