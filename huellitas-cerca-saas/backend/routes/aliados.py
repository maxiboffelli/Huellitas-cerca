from typing import Optional
from fastapi import APIRouter, Query
from database import aliados_col

router = APIRouter(prefix="/aliados", tags=["Aliados, Veterinarias y Sponsors"])


def serialize_aliado(doc: dict) -> dict:
    doc["id"] = str(doc.pop("_id"))
    return doc


@router.get("")
async def listar_aliados(partido: Optional[str] = Query(None)):
    if partido:
        filtro = {"activo": True, "partido": {"$in": [partido, "TODOS"]}}
    else:
        filtro = {"activo": True}
    cursor = aliados_col.find(filtro)
    return [serialize_aliado(doc) async for doc in cursor]
