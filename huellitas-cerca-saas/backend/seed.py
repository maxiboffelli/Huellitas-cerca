import asyncio
from datetime import datetime, timezone
from database import (
    municipios_col,
    usuarios_col,
    mascotas_col,
    campanas_col,
    aliados_col,
)
from auth_utils import hash_password


async def run_seed():
    print("Limpiando colecciones previas...")
    await municipios_col.delete_many({})
    await usuarios_col.delete_many({})
    await mascotas_col.delete_many({})
    await campanas_col.delete_many({})
    await aliados_col.delete_many({})

    print("Insertando municipios con licencia SaaS...")
    res_munis = await municipios_col.insert_many([
        {
            "nombre": "Municipio de Tandil",
            "partido": "Tandil",
            "provincia": "Buenos Aires",
            "area_responsable": "Dirección de Bromatología y Zoonosis",
            "whatsapp_institucional": "5492494000001",
            "logo_url": "https://images.unsplash.com/photo-1517849845537-4d257902454a?w=200",
            "estado_licencia": "ACTIVA",
            "metricas": {"adopciones_logradas": 142, "castraciones_realizadas": 580},
        },
        {
            "nombre": "Municipalidad de La Plata",
            "partido": "La Plata",
            "provincia": "Buenos Aires",
            "area_responsable": "Dirección de Protección Animal y Zoonosis",
            "whatsapp_institucional": "5492214000002",
            "logo_url": "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=200",
            "estado_licencia": "ACTIVA",
            "metricas": {"adopciones_logradas": 310, "castraciones_realizadas": 1240},
        },
    ])
    id_tandil = str(res_munis.inserted_ids[0])
    id_laplata = str(res_munis.inserted_ids[1])

    print("Insertando usuarios de prueba (clave para todos: 123456)...")
    pwd = hash_password("123456")
    res_users = await usuarios_col.insert_many([
        {
            "nombre": "Zoonosis Tandil (Oficial)",
            "email": "admin@tandil.gob.ar",
            "password_hash": pwd,
            "whatsapp": "5492494000001",
            "partido": "Tandil",
            "rol": "ADMIN_MUNICIPAL",
            "municipio_id": id_tandil,
            "verificado_municipio": True,
            "creado_en": datetime.now(timezone.utc),
        },
        {
            "nombre": "Refugio Patitas Serranas",
            "email": "refugio@tandil.org",
            "password_hash": pwd,
            "whatsapp": "5492494111111",
            "partido": "Tandil",
            "rol": "REFUGIO",
            "municipio_id": id_tandil,
            "verificado_municipio": True,
            "creado_en": datetime.now(timezone.utc),
        },
        {
            "nombre": "Refugio Independiente Mar del Plata",
            "email": "refugio@mdp.org",
            "password_hash": pwd,
            "whatsapp": "5492234222222",
            "partido": "General Pueyrredón",
            "rol": "REFUGIO",
            "municipio_id": None,
            "verificado_municipio": False,
            "creado_en": datetime.now(timezone.utc),
        },
        {
            "nombre": "Laura Vecina",
            "email": "vecino@laplata.com",
            "password_hash": pwd,
            "whatsapp": "5492214333333",
            "partido": "La Plata",
            "rol": "CIUDADANO",
            "municipio_id": None,
            "verificado_municipio": False,
            "creado_en": datetime.now(timezone.utc),
        },
    ])
    u_admin_tandil, u_ref_verif, u_ref_indep, u_ciudadano = [str(x) for x in res_users.inserted_ids]

    print("Insertando mascotas (Adopción, Perdidos y Encontrados)...")
    await mascotas_col.insert_many([
        {
            "municipio_id": id_tandil,
            "usuario_id": u_ref_verif,
            "publicador_nombre": "Refugio Patitas Serranas",
            "publicador_rol": "REFUGIO",
            "partido": "Tandil",
            "zona_barrio": "Villa Italia",
            "verificado_municipio": True,
            "tipo_publicacion": "ADOPCION",
            "estado": "ACTIVA",
            "nombre": "Bruno",
            "especie": "PERRO",
            "sexo": "MACHO",
            "tamano": "MEDIANO",
            "edad": "ADULTO",
            "descripcion": "Rescatado de la vía pública, súper dócil con niños y otros perros.",
            "foto_url": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&w=600&q=80",
            "salud": {"vacunado": True, "antirrabica": True, "esterilizado": True, "desparasitado": True},
            "whatsapp_contacto": "5492494111111",
            "creado_en": datetime.now(timezone.utc),
        },
        {
            "municipio_id": id_tandil,
            "usuario_id": u_admin_tandil,
            "publicador_nombre": "Zoonosis Tandil (Oficial)",
            "publicador_rol": "ADMIN_MUNICIPAL",
            "partido": "Tandil",
            "zona_barrio": "Centro",
            "verificado_municipio": True,
            "tipo_publicacion": "ENCONTRADO",
            "estado": "ACTIVA",
            "nombre": "Sin nombre (Collar rojo)",
            "especie": "PERRO",
            "sexo": "HEMBRA",
            "tamano": "PEQUENO",
            "edad": "ADULTO",
            "descripcion": "Encontrada desorientada cerca de Plaza Independencia. Resguardada en Zoonosis.",
            "foto_url": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?auto=format&fit=crop&w=600&q=80",
            "salud": {"vacunado": True, "antirrabica": True, "esterilizado": False, "desparasitado": True},
            "whatsapp_contacto": "5492494000001",
            "creado_en": datetime.now(timezone.utc),
        },
        {
            "municipio_id": None,
            "usuario_id": u_ciudadano,
            "publicador_nombre": "Laura Vecina",
            "publicador_rol": "CIUDADANO",
            "partido": "La Plata",
            "zona_barrio": "Tolosa",
            "verificado_municipio": False,
            "tipo_publicacion": "PERDIDO",
            "estado": "ACTIVA",
            "nombre": "Milo",
            "especie": "GATO",
            "sexo": "MACHO",
            "tamano": "PEQUENO",
            "edad": "ADULTO",
            "descripcion": "Se escapó por los techos en calle 528 y 7. Tiene una mancha blanca en el pecho.",
            "foto_url": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?auto=format&fit=crop&w=600&q=80",
            "salud": {"vacunado": True, "antirrabica": True, "esterilizado": True, "desparasitado": True},
            "whatsapp_contacto": "5492214333333",
            "creado_en": datetime.now(timezone.utc),
        },
        {
            "municipio_id": None,
            "usuario_id": u_ref_indep,
            "publicador_nombre": "Refugio Independiente Mar del Plata",
            "publicador_rol": "REFUGIO",
            "partido": "General Pueyrredón",
            "zona_barrio": "Puerto",
            "verificado_municipio": False,
            "tipo_publicacion": "ADOPCION",
            "estado": "ACTIVA",
            "nombre": "Luna",
            "especie": "GATO",
            "sexo": "HEMBRA",
            "tamano": "PEQUENO",
            "edad": "CACHORRO",
            "descripcion": "Cachorra de 4 meses, usa piedritas y ya tiene primera dosis de vacuna.",
            "foto_url": "https://images.unsplash.com/photo-1573865526739-10659fec78a5?auto=format&fit=crop&w=600&q=80",
            "salud": {"vacunado": True, "antirrabica": False, "esterilizado": False, "desparasitado": True},
            "whatsapp_contacto": "5492234222222",
            "creado_en": datetime.now(timezone.utc),
        },
    ])

    print("Insertando campañas municipales...")
    await campanas_col.insert_many([
        {
            "municipio_id": id_tandil,
            "partido": "Tandil",
            "titulo": "Quirófano Móvil y Antirrábica Gratuita",
            "tipo": "CASTRACION_Y_VACUNACION",
            "fecha_inicio": "2026-11-24",
            "fecha_fin": "2026-11-28",
            "horario": "08:30 a 12:30 hs",
            "ubicacion": "Centro Comunitario Barrio Movediza",
            "requisitos": "Ayuno de 12 hs de sólidos. Perros con correa y bozal; gatos en bolsa de red o transportadora.",
            "requiere_turno": False,
            "link_turnos": None,
            "activa": True,
        },
        {
            "municipio_id": id_laplata,
            "partido": "La Plata",
            "titulo": "Jornada Integral de Zoonosis y Vacunación",
            "tipo": "VACUNACION",
            "fecha_inicio": "2026-11-25",
            "fecha_fin": "2026-11-30",
            "horario": "09:00 a 14:00 hs",
            "ubicacion": "Parque Saavedra - Puesto Móvil Municipal",
            "requisitos": "Concurrir con DNI del responsable mayor de 18 años. Aplicación gratuita sin turno.",
            "requiere_turno": False,
            "link_turnos": None,
            "activa": True,
        },
    ])

    print("Insertando aliados, sponsors y veterinarias...")
    await aliados_col.insert_many([
        {
            "categoria": "MARCA_ALIMENTO",
            "nombre": "NutriCan Argentina (Sponsor Oficial)",
            "partido": "TODOS",
            "direccion": "Red Nacional de Distribuidores",
            "guardia_24hs": False,
            "beneficio_adopcion": "25% de descuento en la primera bolsa de alimento para adoptantes registrados.",
            "codigo_descuento": "HUELLITAS25",
            "whatsapp": "5491140000000",
            "logo_url": "https://images.unsplash.com/photo-1589924691995-400dc9ecc119?w=200",
            "activo": True,
        },
        {
            "categoria": "VETERINARIA",
            "nombre": "Clínica Veterinaria Las Sierras",
            "partido": "Tandil",
            "direccion": "Av. España 642, Tandil",
            "guardia_24hs": True,
            "beneficio_adopcion": "Primera consulta clínica y desparasitación sin cargo presentando ficha de adopción.",
            "codigo_descuento": "SIERRAS-VET",
            "whatsapp": "5492494555555",
            "logo_url": "https://images.unsplash.com/photo-1628009368231-7bb7cfcb0def?w=200",
            "activo": True,
        },
        {
            "categoria": "VETERINARIA",
            "nombre": "Veterinaria Diagonal Norte",
            "partido": "La Plata",
            "direccion": "Diagonal 74 N° 1420, La Plata",
            "guardia_24hs": True,
            "beneficio_adopcion": "20% OFF en plan sanitario inicial y vacunación.",
            "codigo_descuento": "LP-HUELLITAS",
            "whatsapp": "5492214666666",
            "logo_url": "https://images.unsplash.com/photo-1576201836106-db1758fd1c97?w=200",
            "activo": True,
        },
    ])
    print("Seed completado con éxito.")


if __name__ == "__main__":
    asyncio.run(run_seed())
