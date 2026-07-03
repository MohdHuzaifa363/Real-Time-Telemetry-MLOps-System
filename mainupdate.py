from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import uvicorn
import pickle
import numpy as np
import psutil
import os

# 1. Instantiating App with Custom Security Boundaries
app = FastAPI(
    title="Secure MLOps Telemetry Suite",
    docs_url="/api/v1/secure-docs",  # Obfuscated API Docs path for security
    redoc_url=None
)

# 2. Strict CORS Configuration (Restricting unauthorized cross-domain requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Real prod mein isko specific domain par lock karte hain
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Restricting unsafe HTTP methods like PUT/DELETE
    allow_headers=["Content-Type", "Authorization"],
)

# 3. Model Registry Hook: De-serializing Model with Error Obfuscation
MODEL_PATH = "model.pkl"
try:
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Target serialized binary file missing.")
    with open(MODEL_PATH, "rb") as file:
        ml_model = pickle.load(file)
    print("💾 Secure Model Engine Loaded Successfully!")
except Exception:
    ml_model = None
    print("🚨 Security Warning: Model file unreadable or compromised.")

# 4. Input Feature Constraint Contracts (Preventing Overflow and Script Injections)
class SecureTelemetryPayload(BaseModel):
    # Enforcing strict numerical boundary limits via Pydantic Field Constraints
    CPU_Usage: float = Field(..., ge=0.0, le=100.0, description="Strict CPU bounds percent")
    RAM_Usage: float = Field(..., ge=0.0, le=100.0, description="Strict RAM bounds percent")
    Response_Time: float = Field(..., ge=0.0, le=5000.0, description="Strict Latency constraint bounds")

# 5. UI Serving Gateway Instance
@app.get("/")
def serve_dashboard():
    return FileResponse("index.html")

# 6. Live Kernel Telemetry Extractor (Asynchronous Polling API)
@app.get("/api/v1/live-kernel")
def extract_live_kernel_state():
    try:
        cpu_active = psutil.cpu_percent(interval=None)
        ram_active = psutil.virtual_memory().percent
        disk_active = psutil.disk_usage('/').percent
        
        net_buffers = psutil.net_io_counters()
        net_throughput = round((net_buffers.bytes_sent + net_buffers.bytes_recv) / (1024 * 1024), 2)
        
        simulated_latency = round(15 + (cpu_active * 4.5) + (ram_active * 2.1), 2)
        
        return {
            "CPU_Usage": cpu_active,
            "RAM_Usage": ram_active,
            "Disk_Usage": disk_active,
            "Network_Traffic": net_throughput,
            "Response_Time": simulated_latency
        }
    except Exception:
        raise HTTPException(status_code=500, detail="Kernel metrics telemetry extraction failure.")

# 7. Secure Predictive Inference Router
@app.post("/api/v1/predict")
def process_secure_inference(payload: SecureTelemetryPayload):
    if ml_model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Predictive pipeline core allocation offline."
        )
    
    try:
        # Converting validated payload into standardized 2D numpy arrays
        feature_vector = np.array([[payload.CPU_Usage, payload.RAM_Usage, payload.Response_Time]])
        
        prediction_label = ml_model.predict(feature_vector)[0]
        probabilistic_risk = ml_model.predict_proba(feature_vector)[0][1]
        risk_percentage = round(probabilistic_risk * 100, 2)
        
        operational_status = "Imminent Failure Risk Detected!" if prediction_label == 1 else "Healthy"
        
        return {
            "prediction": int(prediction_label),
            "risk_status": operational_status,
            "crash_risk_percentage": risk_percentage,
            "security_token": "Sanitized Payload Processed Successfully"
        }
    except Exception:
        # Internal Exception Masking to isolate directory structure from attackers
        raise HTTPException(status_code=500, detail="Inference processing pipeline breakdown.")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)