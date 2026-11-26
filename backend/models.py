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
    licencia_activa: bool = True
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
    tiene_vacunas_vigentes: bool = False
    cartilla_vacunacion_url: Optional[str] = None
    fecha_desparasitacion: Optional[str] = None
    esterilizacion_detalle: Optional[str] = None
    vacunas_incluidas: list[str] = Field(default_factory=list)


class MascotaCreate(BaseModel):
    tipo_publicacion: Literal["ADOPCION", "PERDIDO", "ENCONTRADO"] = "ADOPCION"
    estado_adopcion: Optional[str] = "en adopción"
    nombre: str
    especie: Literal["PERRO", "GATO"]
    sexo: Literal["MACHO", "HEMBRA"]
    tamano: Literal["PEQUENO", "MEDIANO", "GRANDE"]
    edad: str
    edad_detalle: Optional[str] = None
    partido: Optional[str] = None
    zona_barrio: str
    descripcion: str
    caracter: Optional[str] = Field(None, max_length=100)
    socializacion: Optional[str] = None
    foto_url: str
    fotos_adicionales: list[str] = Field(default_factory=list)
    gancho: Optional[str] = None
    convivencia: Optional[str] = None
    salud: SaludMascota = Field(default_factory=SaludMascota)
    whatsapp_contacto: Optional[str] = None


class MascotaUpdate(BaseModel):
    tipo_publicacion: Optional[Literal["ADOPCION", "PERDIDO", "ENCONTRADO"]] = None
    estado_adopcion: Optional[str] = None
    estado: Optional[Literal["ACTIVA", "RESUELTA", "PAUSADA"]] = None
    nombre: Optional[str] = None
    especie: Optional[Literal["PERRO", "GATO"]] = None
    sexo: Optional[Literal["MACHO", "HEMBRA"]] = None
    tamano: Optional[Literal["PEQUENO", "MEDIANO", "GRANDE"]] = None
    edad: Optional[str] = None
    edad_detalle: Optional[str] = None
    partido: Optional[str] = None
    zona_barrio: Optional[str] = None
    descripcion: Optional[str] = None
    caracter: Optional[str] = Field(None, max_length=100)
    socializacion: Optional[str] = None
    gancho: Optional[str] = None
    convivencia: Optional[str] = None
    foto_url: Optional[str] = None
    fotos_adicionales: Optional[list[str]] = None
    salud: Optional[SaludMascota] = None
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
    contacto_turno: Optional[str] = None
    link_oficial: Optional[str] = None
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
