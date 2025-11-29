from fastapi import APIRouter
from pydantic import BaseModel
from sklearn.linear_model import LinearRegression
import numpy as np
from typing import List
from scipy import stats

router = APIRouter()

class TimeSeriesRequest(BaseModel):
    data: List[float]
    forecast_steps: int = 10
    seasonal_period: int = None

@router.post("/timeseries/analyze")
async def analyze_timeseries(request: TimeSeriesRequest) -> dict:
    """Analyze time series data with trend, seasonality, and forecasting."""
    try:
        data = np.array(request.data)
        n = len(data)
        
        # Trend analysis using linear regression
        X = np.arange(n).reshape(-1, 1)
        model = LinearRegression()
        model.fit(X, data)
        trend = model.predict(X)
        
        # Detrend the data
        detrended = data - trend
        
        # Calculate statistics
        mean_val = float(np.mean(data))
        std_val = float(np.std(data))
        
        # Detect seasonality (simple autocorrelation)
        if request.seasonal_period and request.seasonal_period < n:
            seasonal_component = []
            for i in range(request.seasonal_period):
                seasonal_vals = data[i::request.seasonal_period]
                seasonal_component.append(float(np.mean(seasonal_vals)))
        else:
            seasonal_component = None
        
        # Simple forecast (linear extrapolation)
        X_future = np.arange(n, n + request.forecast_steps).reshape(-1, 1)
        forecast = model.predict(X_future)
        
        # Calculate confidence intervals (simple approach)
        residuals = data - trend
        std_residuals = np.std(residuals)
        confidence_upper = forecast + 1.96 * std_residuals
        confidence_lower = forecast - 1.96 * std_residuals
        
        # Moving average
        window = min(7, n // 4)
        if window > 0:
            moving_avg = np.convolve(data, np.ones(window)/window, mode='valid')
            moving_avg = np.pad(moving_avg, (window-1, 0), mode='edge').tolist()
        else:
            moving_avg = data.tolist()
        
        return {
            "success": True,
            "data": {
                "original": data.tolist(),
                "trend": trend.tolist(),
                "detrended": detrended.tolist(),
                "moving_average": moving_avg,
                "forecast": forecast.tolist(),
                "confidence_upper": confidence_upper.tolist(),
                "confidence_lower": confidence_lower.tolist(),
                "seasonal_component": seasonal_component,
                "statistics": {
                    "mean": mean_val,
                    "std": std_val,
                    "trend_slope": float(model.coef_[0]),
                    "trend_intercept": float(model.intercept_)
                }
            },
            "error": None
        }
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}
