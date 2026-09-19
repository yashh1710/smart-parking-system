from fastapi import FastAPI

app = FastAPI(
    title="Smart Parking System API",
    description="AI-Based Intelligent Vehicle-Aware Smart Parking Management System",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Smart Parking System Backend is running",
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }