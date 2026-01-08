from fastapi import FastAPI
from app.database import init_db
from app import routes 

app = FastAPI(title="Notes Mini Service", version="0.1.0")

# Health check route
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Include notes routes
app.include_router(routes.router)
