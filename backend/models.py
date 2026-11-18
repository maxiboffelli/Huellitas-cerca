from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class MetricasMunicipio(BaseModel):
    adopciones_logradas: int = 0
    castraciones_realizadas: int = 0


class MunicipioCreate(BaseModel):
    nombre: str
    partido: str
    provincia: str = "Buenos Aires"
    area_responsable: str
    whatsapp_institucional: str
    logo_url: Optional[str] = None
    estado_licencia: Literal["ACTIVA", "SUSPENDIDA"] = "ACTIVA"
    metricas: MetricasMunicipio = Field(default_factory=MetricasMunicipio)


class UsuarioRegister(BaseModel):
    nombre: str
    email: EmailStr
    password: str
    whatsapp: str
    partido: str
    rol: Literal["ADMIN_MUNICIPAL", "REFUGIO", "CIUDADANO"] = "CIUDADANO"
    municipio_id: Optional[str] = None


class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str


class SaludMascota(BaseModel):
    vacunado: bool = False
    antirrabica: bool = False
    esterilizado: bool = False
    desparasitado: bool = False


class MascotaCreate(BaseModel):
    tipo_publicacion: Literal["ADOPCION", "PERDIDO", "ENCONTRADO"] = "ADOPCION"
    nombre: str
    especie: Literal["PERRO", "GATO"]
    sexo: Literal["MACHO", "HEMBRA"]
    tamano: Literal["PEQUENO", "MEDIANO", "GRANDE"]
    edad: Literal["CACHORRO", "ADULTO", "SENIOR"]
    partido: Optional[str] = None
    zona_barrio: str
    descripcion: str
    foto_url: str
    salud: SaludMascota = Field(default_factory=SaludMascota)
    whatsapp_contacto: Optional[str] = None


class MascotaEstadoUpdate(BaseModel):
    estado: Literal["ACTIVA", "RESUELTA", "PAUSADA"]


class CampanaCreate(BaseModel):
    titulo: str
    partido: Optional[str] = None
    tipo: Literal["VACUNACION", "CASTRACION", "CASTRACION_Y_VACUNACION"]
    fecha_inicio: str
    fecha_fin: str
    horario: str
    ubicacion: str
    requisitos: str
    requiere_turno: bool = False
    link_turnos: Optional[str] = None
    activa: bool = True


class AliadoCreate(BaseModel):
    categoria: Literal["VETERINARIA", "MARCA_ALIMENTO", "PET_SHOP"]
    nombre: str
    partido: str = "TODOS"
    direccion: Optional[str] = None
    guardia_24hs: bool = False
    beneficio_adopcion: str
    codigo_descuento: Optional[str] = None
    whatsapp: Optional[str] = None
    logo_url: Optional[str] = None
    activo: bool = True
