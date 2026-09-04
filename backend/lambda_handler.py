"""
Robopulse Command Center
Day 9 - the entry point that AWS Lambda actually calls. Mangum transflates between lambda's event/context invocation model and the ASGI interface that FastAPI 
"""

from mangum import Mangum
from app.main import app

handler = Mangum(app)
