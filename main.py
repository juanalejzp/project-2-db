from fastapi import FastAPI
from app.routes import router  # Importa el enrutador desde routes.py

app = FastAPI()

# Incluye el enrutador en la aplicación principal
app.include_router(router)
