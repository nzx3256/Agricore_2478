from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import farm_routes, farmer_routes, equipment_routes, auth, \
        field_job_routes, report_routes

app = FastAPI(title="AgiCore")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(farm_routes.router)
app.include_router(farmer_routes.router)
app.include_router(equipment_routes.router)
app.include_router(field_job_routes.router)
app.include_router(report_routes.router)
app.include_router(auth.router)

@app.get("/health", tags=["health"])
async def get_health():
    return {"status": "ok"}
