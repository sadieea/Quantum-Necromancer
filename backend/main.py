from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modules import quantum, lda, anomaly, clustering, regression, timeseries, correlation, dataprocessing

app = FastAPI(title="Quantum Necromancer Data Science API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"success": True, "data": {"status": "alive"}, "error": None}

@app.get("/api/capabilities")
async def get_capabilities():
    """Return all available analysis capabilities."""
    return {
        "success": True,
        "data": {
            "modules": [
                {"name": "Quantum Random Generation", "endpoint": "/api/quantum/generate"},
                {"name": "Topic Modeling (LDA)", "endpoint": "/api/lda/analyze"},
                {"name": "Anomaly Detection", "endpoint": "/api/anomaly/detect"},
                {"name": "Clustering Analysis", "endpoint": "/api/clustering/analyze"},
                {"name": "Regression Analysis", "endpoint": "/api/regression/analyze"},
                {"name": "Time Series Analysis", "endpoint": "/api/timeseries/analyze"},
                {"name": "Correlation Analysis", "endpoint": "/api/correlation/analyze"},
                {"name": "Data Processing", "endpoint": "/api/data/*"}
            ]
        },
        "error": None
    }

# Original modules
app.include_router(quantum.router, prefix="/api")
app.include_router(lda.router, prefix="/api")
app.include_router(anomaly.router, prefix="/api")

# New enhanced modules
app.include_router(clustering.router, prefix="/api")
app.include_router(regression.router, prefix="/api")
app.include_router(timeseries.router, prefix="/api")
app.include_router(correlation.router, prefix="/api")
app.include_router(dataprocessing.router, prefix="/api")
