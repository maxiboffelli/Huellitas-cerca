import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routes import auth, municipios, mascotas, campanas, aliados

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "Huellitas Cerca")

app = FastAPI(
    title=f"{APP_NAME} - API SaaS Municipal",
    version="1.0.0",
    description="API RESTful para gestión municipal de adopciones, animales perdidos, zoonosis y red de refugios.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(municipios.router, prefix="/api")
app.include_router(mascotas.router, prefix="/api")
app.include_router(campanas.router, prefix="/api")
app.include_router(aliados.router, prefix="/api")


@app.get("/")
async def root():
    return {"app": APP_NAME, "status": "online", "docs": "/docs"}
