from fastapi import APIRouter
from pydantic import BaseModel
import numpy as np
from typing import List, Literal
from scipy.stats import pearsonr, spearmanr

router = APIRouter()

class CorrelationRequest(BaseModel):
    data: List[List[float]]
    method: Literal["pearson", "spearman"] = "pearson"
    feature_names: List[str] = None

@router.post("/correlation/analyze")
async def analyze_correlation(request: CorrelationRequest) -> dict:
    """Calculate correlation matrix and pairwise correlations."""
    try:
        data = np.array(request.data)
        n_features = data.shape[1]
        
        # Generate feature names if not provided
        if not request.feature_names:
            feature_names = [f"Feature_{i}" for i in range(n_features)]
        else:
            feature_names = request.feature_names
        
        # Calculate correlation matrix
        if request.method == "pearson":
            corr_matrix = np.corrcoef(data.T)
        else:  # spearman
            from scipy.stats import spearmanr
            corr_matrix, _ = spearmanr(data, axis=0)
        
        # Find strongest correlations
        correlations = []
        for i in range(n_features):
            for j in range(i + 1, n_features):
                correlations.append({
                    "feature1": feature_names[i],
                    "feature2": feature_names[j],
                    "correlation": float(corr_matrix[i, j]),
                    "abs_correlation": float(abs(corr_matrix[i, j]))
                })
        
        # Sort by absolute correlation
        correlations.sort(key=lambda x: x["abs_correlation"], reverse=True)
        
        return {
            "success": True,
            "data": {
                "correlation_matrix": corr_matrix.tolist(),
                "feature_names": feature_names,
                "top_correlations": correlations[:10],
                "all_correlations": correlations,
                "method": request.method
            },
            "error": None
        }
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}
