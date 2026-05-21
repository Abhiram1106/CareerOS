from fastapi import FastAPI

from .api.router import api_router

app = FastAPI(title="CareerOS ATS Engine", version="0.2.0")
app.include_router(api_router)


@app.get("/health")
def health():
    return {"status": "ok"}
