from fastapi import APIRouter
from pydantic import BaseModel
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
import numpy as np
from typing import List, Literal

router = APIRouter()

class ClusteringRequest(BaseModel):
    data: List[List[float]]
    algorithm: Literal["kmeans", "dbscan", "hierarchical"] = "kmeans"
    n_clusters: int = 3
    eps: float = 0.5  # For DBSCAN
    min_samples: int = 5  # For DBSCAN

@router.post("/clustering/analyze")
async def perform_clustering(request: ClusteringRequest) -> dict:
    """Perform clustering analysis using various algorithms."""
    try:
        X = np.array(request.data)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        if request.algorithm == "kmeans":
            model = KMeans(n_clusters=request.n_clusters, random_state=42, n_init=10)
            labels = model.fit_predict(X_scaled)
            centers = scaler.inverse_transform(model.cluster_centers_).tolist()
            inertia = float(model.inertia_)
            
        elif request.algorithm == "dbscan":
            model = DBSCAN(eps=request.eps, min_samples=request.min_samples)
            labels = model.fit_predict(X_scaled)
            centers = None
            inertia = None
            
        elif request.algorithm == "hierarchical":
            model = AgglomerativeClustering(n_clusters=request.n_clusters)
            labels = model.fit_predict(X_scaled)
            centers = None
            inertia = None
        
        # Calculate cluster statistics
        unique_labels = np.unique(labels)
        cluster_stats = []
        for label in unique_labels:
            mask = labels == label
            cluster_data = X[mask]
            cluster_stats.append({
                "cluster_id": int(label),
                "size": int(np.sum(mask)),
                "mean": cluster_data.mean(axis=0).tolist(),
                "std": cluster_data.std(axis=0).tolist()
            })
        
        return {
            "success": True,
            "data": {
                "labels": labels.tolist(),
                "n_clusters": len(unique_labels),
                "centers": centers,
                "inertia": inertia,
                "cluster_stats": cluster_stats,
                "algorithm": request.algorithm
            },
            "error": None
        }
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}
