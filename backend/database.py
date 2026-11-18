import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "huellitas_cerca_db")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

municipios_col = db["municipios"]
usuarios_col = db["usuarios"]
mascotas_col = db["mascotas"]
campanas_col = db["campanas"]
aliados_col = db["aliados"]
