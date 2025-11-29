from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
import pandas as pd
import numpy as np
from typing import List, Literal
import io
import json

router = APIRouter()

class DataCleaningRequest(BaseModel):
    data: List[List[float]]
    handle_missing: Literal["drop", "mean", "median", "zero"] = "mean"
    remove_outliers: bool = False
    outlier_threshold: float = 3.0  # Standard deviations

class DataTransformRequest(BaseModel):
    data: List[List[float]]
    method: Literal["normalize", "standardize", "minmax"] = "standardize"

@router.post("/data/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload and parse CSV, JSON, or Excel files."""
    try:
        content = await file.read()
        
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content))
        elif file.filename.endswith('.json'):
            df = pd.read_json(io.BytesIO(content))
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(io.BytesIO(content))
        else:
            return {"success": False, "data": None, "error": "Unsupported file format"}
        
        # Basic statistics
        stats = {
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "numeric_columns": df.select_dtypes(include=[np.number]).columns.tolist()
        }
        
        # Sample data
        sample = df.head(10).to_dict(orient='records')
        
        return {
            "success": True,
            "data": {
                "statistics": stats,
                "sample": sample,
                "full_data": df.to_dict(orient='records')
            },
            "error": None
        }
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}

@router.post("/data/clean")
async def clean_data(request: DataCleaningRequest) -> dict:
    """Clean data by handling missing values and outliers."""
    try:
        data = np.array(request.data, dtype=float)
        
        # Handle missing values (NaN)
        if request.handle_missing == "drop":
            data = data[~np.isnan(data).any(axis=1)]
        elif request.handle_missing == "mean":
            col_mean = np.nanmean(data, axis=0)
            inds = np.where(np.isnan(data))
            data[inds] = np.take(col_mean, inds[1])
        elif request.handle_missing == "median":
            col_median = np.nanmedian(data, axis=0)
            inds = np.where(np.isnan(data))
            data[inds] = np.take(col_median, inds[1])
        elif request.handle_missing == "zero":
            data = np.nan_to_num(data, nan=0.0)
        
        # Remove outliers using z-score
        if request.remove_outliers:
            z_scores = np.abs((data - np.mean(data, axis=0)) / np.std(data, axis=0))
            data = data[(z_scores < request.outlier_threshold).all(axis=1)]
        
        return {
            "success": True,
            "data": {
                "cleaned_data": data.tolist(),
                "original_shape": request.data.__len__(),
                "cleaned_shape": len(data),
                "rows_removed": request.data.__len__() - len(data)
            },
            "error": None
        }
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}

@router.post("/data/transform")
async def transform_data(request: DataTransformRequest) -> dict:
    """Transform data using various scaling methods."""
    try:
        data = np.array(request.data)
        
        if request.method == "normalize":
            # L2 normalization
            norms = np.linalg.norm(data, axis=1, keepdims=True)
            transformed = data / (norms + 1e-10)
            
        elif request.method == "standardize":
            # Z-score standardization
            mean = np.mean(data, axis=0)
            std = np.std(data, axis=0)
            transformed = (data - mean) / (std + 1e-10)
            
        elif request.method == "minmax":
            # Min-max scaling to [0, 1]
            min_val = np.min(data, axis=0)
            max_val = np.max(data, axis=0)
            transformed = (data - min_val) / (max_val - min_val + 1e-10)
        
        return {
            "success": True,
            "data": {
                "transformed_data": transformed.tolist(),
                "method": request.method,
                "original_stats": {
                    "mean": np.mean(data, axis=0).tolist(),
                    "std": np.std(data, axis=0).tolist(),
                    "min": np.min(data, axis=0).tolist(),
                    "max": np.max(data, axis=0).tolist()
                }
            },
            "error": None
        }
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}
