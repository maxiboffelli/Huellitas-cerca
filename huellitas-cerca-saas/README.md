# Huellitas Cerca (SaaS Municipal B2B + Red de Refugios)

## Puesta en marcha rápida
1. `cd backend`
2. `python -m venv venv` y activar (`venv\Scripts\activate` en Windows o `source venv/bin/activate` en Linux/Mac)
3. `pip install -r requirements.txt`
4. Copiar `.env.example` a `.env` y pegar tu `MONGO_URI` de MongoDB Atlas.
5. Cargar datos iniciales de Buenos Aires: `python seed.py`
6. Iniciar servidor: `uvicorn main:app --reload`
7. Abrir `frontend/index.html` con Live Server.

## Usuarios de prueba cargados por `seed.py` (Contraseña para todos: `123456`)
- **Admin Municipal (Tandil):** `admin@tandil.gob.ar`
- **Refugio Verificado (Tandil):** `refugio@tandil.org`
- **Refugio Independiente (Mar del Plata):** `refugio@mdp.org`
- **Ciudadano (La Plata):** `vecino@laplata.com`
