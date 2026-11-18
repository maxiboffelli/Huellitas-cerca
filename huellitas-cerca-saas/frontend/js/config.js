const CONFIG = {
    APP_NAME: "Huellitas Cerca",
    SUBTITLE: "GESTIÓN MUNICIPAL Y RED DE REFUGIOS",
    API_BASE_URL: "http://127.0.0.1:8000/api",
    PARTIDOS_BUENOS_AIRES: [
        "Tandil",
        "La Plata",
        "General Pueyrredón",
        "Bahía Blanca",
        "Quilmes",
        "Lanús",
        "Avellaneda",
        "Lomas de Zamora",
        "San Isidro",
        "Vicente López",
        "Tigre",
        "Pilar",
        "Morón",
        "Merlo",
        "Moreno",
        "Olavarría",
        "Junín",
        "Pergamino",
        "Zárate",
        "San Nicolás"
    ]
};

const TAILWIND_BRAND_CONFIG = {
    theme: {
        extend: {
            colors: {
                brand: {
                    bg: '#F5F2EB',
                    card: '#FAF8F5',
                    primary: '#6B6B58',
                    secondary: '#A7B07A',
                    accent: '#C86D51',
                    accentHover: '#B25A40',
                    textDark: '#3A3A32',
                    textMuted: '#7A7A6E',
                    tagBg: '#E8E4D9',
                    greenBadge: '#5A7D58',
                }
            },
            borderRadius: {
                'card': '20px',
                'pill': '60px'
            }
        }
    }
};
