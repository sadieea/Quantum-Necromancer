from fastapi import APIRouter
from pydantic import BaseModel
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import numpy as np
from typing import List, Literal

router = APIRouter()

class RegressionRequest(BaseModel):
    X: List[List[float]]
    y: List[float]
    algorithm: Literal["linear", "polynomial", "ridge", "lasso"] = "linear"
    degree: int = 2  # For polynomial
    alpha: float = 1.0  # For ridge/lasso
    predict_X: List[List[float]] = None

@router.post("/regression/analyze")
async def perform_regression(request: RegressionRequest) -> dict:
    """Perform regression analysis with various algorithms."""
    try:
        X = np.array(request.X)
        y = np.array(request.y)
        
        if request.algorithm == "polynomial":
            poly = PolynomialFeatures(degree=request.degree)
            X_poly = poly.fit_transform(X)
            model = LinearRegression()
            model.fit(X_poly, y)
            y_pred = model.predict(X_poly)
            
            if request.predict_X:
                X_new_poly = poly.transform(np.array(request.predict_X))
                predictions = model.predict(X_new_poly).tolist()
            else:
                predictions = None
                
        elif request.algorithm == "ridge":
            model = Ridge(alpha=request.alpha)
            model.fit(X, y)
            y_pred = model.predict(X)
            predictions = model.predict(np.array(request.predict_X)).tolist() if request.predict_X else None
            
        elif request.algorithm == "lasso":
            model = Lasso(alpha=request.alpha)
            model.fit(X, y)
            y_pred = model.predict(X)
            predictions = model.predict(np.array(request.predict_X)).tolist() if request.predict_X else None
            
        else:  # linear
            model = LinearRegression()
            model.fit(X, y)
            y_pred = model.predict(X)
            predictions = model.predict(np.array(request.predict_X)).tolist() if request.predict_X else None
        
        # Calculate metrics
        r2 = float(r2_score(y, y_pred))
        mse = float(mean_squared_error(y, y_pred))
        mae = float(mean_absolute_error(y, y_pred))
        rmse = float(np.sqrt(mse))
        
        return {
            "success": True,
            "data": {
                "coefficients": model.coef_.tolist() if hasattr(model, 'coef_') else None,
                "intercept": float(model.intercept_) if hasattr(model, 'intercept_') else None,
                "r2_score": r2,
                "mse": mse,
                "rmse": rmse,
                "mae": mae,
                "fitted_values": y_pred.tolist(),
                "predictions": predictions,
                "algorithm": request.algorithm
            },
            "error": None
        }
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}
