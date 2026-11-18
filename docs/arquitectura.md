# Arquitectura Técnica: Plataforma SaaS Municipal + Red de Refugios

## 1. Definición y Stack
- **Modelo:** SaaS B2B Municipal + Red Comunitaria/Refugios (Provincia de Buenos Aires).
- **Nombre configurable:** Variable global `APP_NAME = "Huellitas Cerca"` (provisional / configurable).
- **Frontend:** HTML5 multipágina, Tailwind CSS (CDN), Vanilla JS modular (`js/config.js`, `js/api.js`, `js/auth.js`).
- **Backend:** Python 3.12 + FastAPI (API RESTful asíncrona).
- **Base de Datos:** MongoDB Atlas (driver `motor` + `pydantic` v2).
- **Imágenes:** URL externa o Supabase Storage (bucket público `mascotas-imagenes`).

---

## 2. Sistema de Diseño (Tokens UI)
- **Paleta de colores:**
  - Fondo general (`bg`): `#F5F2EB`
  - Tarjetas (`card`): `#FAF8F5`
  - Primario (`primary`): `#6B6B58`
  - Secundario (`secondary`): `#A7B07A`
  - Acento (`accent`): `#C86D51` (Hover: `#B25A40`)
  - Texto oscuro (`textDark`): `#3A3A32`
  - Texto secundario (`textMuted`): `#7A7A6E`
  - Bordes/Tags (`tagBg`): `#E8E4D9`
  - Éxito / Sello Oficial (`greenBadge`): `#5A7D58`
- **Geometría:** Tarjetas con `rounded-card` (`20px`), botones/inputs/pills con `rounded-pill` (`60px`), sin sombras (`shadow-none`), bordes finos `1px solid #E8E4D9`.

---

## 3. Colecciones MongoDB Atlas
- `municipios`: Tenants con licencia SaaS activa (`nombre`, `partido`, `provincia`, `area_responsable`, `whatsapp_institucional`, `estado_licencia`, `metricas`).
- `usuarios`: `ADMIN_MUNICIPAL`, `REFUGIO` (verificado o independiente con `municipio_id: null`), `CIUDADANO`.
- `mascotas`: Unifica `ADOPCION`, `PERDIDO` y `ENCONTRADO` con filtro por `partido` e insignia `verificado_municipio`.
- `campanas`: Operativos municipales de `VACUNACION`, `CASTRACION` o `CASTRACION_Y_VACUNACION`.
- `aliados`: Sponsors y veterinarias (`VETERINARIA`, `MARCA_ALIMENTO`, `PET_SHOP`) globales (`partido: "TODOS"`) o locales por `partido`.
