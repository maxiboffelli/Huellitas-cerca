from typing import Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from bson import ObjectId
from database import mascotas_col, municipios_col
from models import MascotaCreate, MascotaUpdate, MascotaEstadoUpdate
from auth_utils import get_current_user

router = APIRouter(prefix="/mascotas", tags=["Mascotas y Perdidos"])


def serialize_mascota(doc: dict) -> dict:
    doc["id"] = str(doc.pop("_id"))
    return doc


async def verificar_licencia_municipio(partido: str):
    """Verifica que el municipio del partido tenga licencia activa."""
    muni = await municipios_col.find_one({"partido": partido})
    if muni and not muni.get("licencia_activa", muni.get("estado_licencia", "ACTIVA") == "ACTIVA"):
        raise HTTPException(
            status_code=403,
            detail="Municipio sin licencia activa. No se pueden publicar mascotas hasta que el municipio active su licencia."
        )


@router.get("")
async def listar_mascotas(
    partido: Optional[str] = Query(None),
    tipo_publicacion: Optional[str] = Query(None),
    especie: Optional[str] = Query(None),
    tamano: Optional[str] = Query(None),
    edad: Optional[str] = Query(None),
    solo_verificados: bool = Query(False),
    estado: str = Query("ACTIVA"),
):
    filtro = {"estado": estado}
    if partido:
        filtro["partido"] = partido
    if tipo_publicacion:
        filtro["tipo_publicacion"] = tipo_publicacion
    if especie:
        filtro["especie"] = especie
    if tamano:
        filtro["tamano"] = tamano
    if edad:
        filtro["edad"] = edad
    if solo_verificados:
        filtro["verificado_municipio"] = True

    cursor = mascotas_col.find(filtro).sort("creado_en", -1)
    return [serialize_mascota(doc) async for doc in cursor]


@router.get("/mis-publicaciones")
async def mis_publicaciones(current_user: dict = Depends(get_current_user)):
    cursor = mascotas_col.find({"usuario_id": current_user["id"]}).sort("creado_en", -1)
    return [serialize_mascota(doc) async for doc in cursor]


@router.get("/{mascota_id}")
async def detalle_mascota(mascota_id: str):
    if not ObjectId.is_valid(mascota_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    doc = await mascotas_col.find_one({"_id": ObjectId(mascota_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")
    return serialize_mascota(doc)


@router.post("", status_code=201)
async def crear_mascota(payload: MascotaCreate, current_user: dict = Depends(get_current_user)):
    partido_destino = payload.partido or current_user["partido"]
    await verificar_licencia_municipio(partido_destino)

    doc = {
        "municipio_id": current_user.get("municipio_id"),
        "usuario_id": current_user["id"],
        "publicador_nombre": current_user["nombre"],
        "publicador_rol": current_user["rol"],
        "partido": partido_destino,
        "zona_barrio": payload.zona_barrio,
        "verificado_municipio": current_user.get("verificado_municipio", False),
        "tipo_publicacion": payload.tipo_publicacion,
        "estado": "ACTIVA",
        "nombre": payload.nombre,
        "especie": payload.especie,
        "sexo": payload.sexo,
        "tamano": payload.tamano,
        "edad": payload.edad,
        "descripcion": payload.descripcion,
        "gancho": payload.gancho or "",
        "convivencia": payload.convivencia or "",
        "foto_url": payload.foto_url,
        "salud": payload.salud.model_dump(),
        "whatsapp_contacto": payload.whatsapp_contacto or current_user.get("whatsapp", ""),
        "creado_en": datetime.now(timezone.utc),
    }
    res = await mascotas_col.insert_one(doc)
    doc["id"] = str(res.inserted_id)
    doc.pop("_id", None)
    return doc


@router.patch("/{mascota_id}/estado")
async def actualizar_estado(
    mascota_id: str,
    payload: MascotaEstadoUpdate,
    current_user: dict = Depends(get_current_user),
):
    if not ObjectId.is_valid(mascota_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    mascota = await mascotas_col.find_one({"_id": ObjectId(mascota_id)})
    if not mascota:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")

    es_dueno = mascota["usuario_id"] == current_user["id"]
    es_admin_mismo_partido = (
        current_user["rol"] == "ADMIN_MUNICIPAL"
        and mascota["partido"] == current_user["partido"]
    )
    if not (es_dueno or es_admin_mismo_partido):
        raise HTTPException(status_code=403, detail="No tienes permisos sobre esta publicación")

    await mascotas_col.update_one(
        {"_id": ObjectId(mascota_id)}, {"$set": {"estado": payload.estado}}
    )
    return {"id": mascota_id, "estado": payload.estado}


@router.patch("/{mascota_id}")
async def editar_mascota(
    mascota_id: str,
    payload: MascotaUpdate,
    current_user: dict = Depends(get_current_user),
):
    if not ObjectId.is_valid(mascota_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    mascota = await mascotas_col.find_one({"_id": ObjectId(mascota_id)})
    if not mascota:
        raise HTTPException(status_code=404, detail="Publicación no encontrada")

    es_dueno = mascota["usuario_id"] == current_user["id"]
    es_admin_mismo_partido = (
        current_user["rol"] == "ADMIN_MUNICIPAL"
        and mascota["partido"] == current_user["partido"]
    )
    if not (es_dueno or es_admin_mismo_partido):
        raise HTTPException(status_code=403, detail="No tienes permisos para editar esta publicación")

    updates = payload.model_dump(exclude_none=True)
    if "salud" in updates and updates["salud"]:
        updates["salud"] = payload.salud.model_dump()

    if updates:
        await mascotas_col.update_one({"_id": ObjectId(mascota_id)}, {"$set": updates})

    doc = await mascotas_col.find_one({"_id": ObjectId(mascota_id)})
    return serialize_mascota(doc)
