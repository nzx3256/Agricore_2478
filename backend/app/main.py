from fastapi import FastAPI
from app.routers import farm_routes, farmer_routes, equipment_routes

app = FastAPI(title="AgiCore")

app.include_router(farm_routes.router)
app.include_router(farmer_routes.router)
app.include_router(equipment_routes.router)

@app.get("/health", tags=["health"])
async def get_health():
    return {"status": "ok"}
