from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import routes_discovery, routes_crm

app = FastAPI(title="AI Lead Discovery Platform", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_discovery.router)
app.include_router(routes_crm.router)

@app.get("/")
def health_check():
    return {"status": "active", "module": "AI Lead Discovery Engine"}