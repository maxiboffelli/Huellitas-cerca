from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from bson import ObjectId
from database import campanas_col
from models import CampanaCreate
from auth_utils import require_admin_municipal

router = APIRouter(prefix="/campanas", tags=["Campañas Municipales"])


def serialize_campana(doc: dict) -> dict:
    doc["id"] = str(doc.pop("_id"))
    return doc


@router.get("")
async def listar_campanas(
    partido: Optional[str] = Query(None),
    activa: bool = Query(True),
):
    filtro = {"activa": activa}
    if partido:
        filtro["partido"] = partido
    cursor = campanas_col.find(filtro).sort("fecha_inicio", 1)
    return [serialize_campana(doc) async for doc in cursor]


@router.get("/mis-campanas")
async def mis_campanas(
    admin_user: dict = Depends(require_admin_municipal),
):
    cursor = campanas_col.find({"partido": admin_user["partido"]}).sort("fecha_inicio", -1)
    return [serialize_campana(doc) async for doc in cursor]


@router.post("", status_code=201)
async def crear_campana(
    payload: CampanaCreate,
    admin_user: dict = Depends(require_admin_municipal),
):
    doc = payload.model_dump()
    doc["municipio_id"] = admin_user.get("municipio_id")
    doc["partido"] = payload.partido or admin_user["partido"]
    res = await campanas_col.insert_one(doc)
    doc["id"] = str(res.inserted_id)
    doc.pop("_id", None)
    return doc


@router.patch("/{campana_id}/estado")
async def alternar_estado_campana(
    campana_id: str,
    admin_user: dict = Depends(require_admin_municipal),
):
    if not ObjectId.is_valid(campana_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    campana = await campanas_col.find_one({"_id": ObjectId(campana_id)})
    if not campana:
        raise HTTPException(status_code=404, detail="Campaña no encontrada")

    if campana.get("partido") != admin_user.get("partido"):
        raise HTTPException(status_code=403, detail="No tienes permisos sobre esta campaña")

    nuevo_estado = not bool(campana.get("activa", True))
    await campanas_col.update_one(
        {"_id": ObjectId(campana_id)},
        {"$set": {"activa": nuevo_estado}},
    )
    return {"id": campana_id, "activa": nuevo_estado}
