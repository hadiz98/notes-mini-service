from fastapi import FastAPI

app = FastAPI(
    title="Notes Mini Service",
)

@app.get("/health")
def health_check():
    return {"status": "ok"}
