from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from database import municipios_col, usuarios_col, mascotas_col
from auth_utils import require_admin_municipal

router = APIRouter(prefix="/municipios", tags=["Municipios SaaS"])


def serialize_municipio(doc: dict) -> dict:
    doc["id"] = str(doc.pop("_id"))
    return doc


@router.get("")
async def listar_municipios():
    cursor = municipios_col.find({"estado_licencia": "ACTIVA"}).sort("partido", 1)
    items = [serialize_municipio(doc) async for doc in cursor]
    return items


@router.get("/mi-panel/refugios")
async def listar_refugios_mi_panel(
    admin_user: dict = Depends(require_admin_municipal),
):
    cursor = usuarios_col.find(
        {"rol": "REFUGIO", "partido": admin_user["partido"]},
        {"password_hash": 0},
    ).sort("nombre", 1)
    items = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        doc.pop("password_hash", None)
        items.append(doc)
    return items


@router.patch("/mi-panel/refugios/{refugio_id}/verificar")
async def verificar_refugio(
    refugio_id: str,
    admin_user: dict = Depends(require_admin_municipal),
):
    if not ObjectId.is_valid(refugio_id):
        raise HTTPException(status_code=400, detail="ID de refugio inválido")

    refugio = await usuarios_col.find_one({"_id": ObjectId(refugio_id)})
    if not refugio:
        raise HTTPException(status_code=404, detail="Refugio no encontrado")

    if refugio.get("partido") != admin_user.get("partido"):
        raise HTTPException(status_code=403, detail="El refugio no pertenece a tu partido")

    nuevo_estado = not bool(refugio.get("verificado_municipio", False))
    await usuarios_col.update_one(
        {"_id": ObjectId(refugio_id)},
        {"$set": {"verificado_municipio": nuevo_estado}},
    )

    await mascotas_col.update_many(
        {"$or": [{"creador_id": refugio_id}, {"usuario_id": refugio_id}]},
        {"$set": {"verificado_municipio": nuevo_estado}},
    )

    return {
        "id": refugio_id,
        "verificado_municipio": nuevo_estado,
    }


@router.get("/{municipio_id}")
async def detalle_municipio(municipio_id: str):
    if not ObjectId.is_valid(municipio_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    doc = await municipios_col.find_one({"_id": ObjectId(municipio_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Municipio no encontrado")
    return serialize_municipio(doc)
