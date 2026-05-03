from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Deployment Metrics API")

# In-memory "database"
db = []

# Data model for incoming POST requests
class Deployment(BaseModel):
    service_name: str
    build_time_seconds: int
    success: bool

@app.get("/")
def health_check():
    return {"status": "healthy", "total_records": len(db)}

# Input Endpoint
@app.post("/deployments")
def add_deployment(deployment: Deployment):
    db.append(deployment.model_dump())
    return {"message": "Deployment recorded successfully", "id": len(db) - 1}

# Dynamic Route with Error Handling
@app.get("/deployments/{deploy_id}")
def get_deployment(deploy_id: int):
    if deploy_id < 0 or deploy_id >= len(db):
        raise HTTPException(status_code=404, detail="Deployment record not found")
    return db[deploy_id]

# Computation Endpoint
@app.get("/metrics/summary")
def get_summary():
    if not db:
        return {"average_build_time": 0, "success_rate": "0%"}
    
    avg_time = sum(d["build_time_seconds"] for d in db) / len(db)
    success_count = sum(1 for d in db if d["success"])
    success_rate = (success_count / len(db)) * 100
    
    return {
        "average_build_time": round(avg_time, 2),
        "success_rate": f"{round(success_rate, 1)}%"
    }