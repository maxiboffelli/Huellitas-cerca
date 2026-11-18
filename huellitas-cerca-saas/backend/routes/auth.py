from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from database import usuarios_col, municipios_col
from models import UsuarioRegister, UsuarioLogin
from auth_utils import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(payload: UsuarioRegister):
    existing = await usuarios_col.find_one({"email": payload.email.lower()})
    if existing:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    verificado = False
    municipio_id_str = None

    if payload.municipio_id:
        muni = await municipios_col.find_one({"_id": ObjectId(payload.municipio_id), "estado_licencia": "ACTIVA"})
        if muni:
            municipio_id_str = str(muni["_id"])
            if payload.rol == "ADMIN_MUNICIPAL":
                verificado = True

    doc = {
        "nombre": payload.nombre,
        "email": payload.email.lower(),
        "password_hash": hash_password(payload.password),
        "whatsapp": payload.whatsapp,
        "partido": payload.partido,
        "rol": payload.rol,
        "municipio_id": municipio_id_str,
        "verificado_municipio": verificado,
        "creado_en": datetime.now(timezone.utc),
    }
    res = await usuarios_col.insert_one(doc)
    user_id = str(res.inserted_id)
    token = create_access_token({"sub": user_id, "rol": doc["rol"]})

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": {
            "id": user_id,
            "nombre": doc["nombre"],
            "email": doc["email"],
            "rol": doc["rol"],
            "partido": doc["partido"],
            "municipio_id": doc["municipio_id"],
            "verificado_municipio": doc["verificado_municipio"],
            "whatsapp": doc["whatsapp"],
        },
    }


@router.post("/login")
async def login(payload: UsuarioLogin):
    user = await usuarios_col.find_one({"email": payload.email.lower()})
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    user_id = str(user["_id"])
    token = create_access_token({"sub": user_id, "rol": user["rol"]})

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": {
            "id": user_id,
            "nombre": user["nombre"],
            "email": user["email"],
            "rol": user["rol"],
            "partido": user["partido"],
            "municipio_id": user.get("municipio_id"),
            "verificado_municipio": user.get("verificado_municipio", False),
            "whatsapp": user.get("whatsapp", ""),
        },
    }
