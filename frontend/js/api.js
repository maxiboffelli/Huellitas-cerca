async function apiFetch(endpoint, options = {}) {
    const token = localStorage.getItem("hc_token");
    const headers = {
        "Content-Type": "application/json",
        ...(options.headers || {})
    };
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(`${CONFIG.API_BASE_URL}${endpoint}`, {
        ...options,
        headers
    });

    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
        throw new Error(data.detail || "Error en la solicitud al servidor");
    }
    return data;
}

function populatePartidosSelect(selectElement, includeAllLabel = null) {
    if (!selectElement) return;
    selectElement.innerHTML = "";
    if (includeAllLabel) {
        const optAll = document.createElement("option");
        optAll.value = "";
        optAll.textContent = includeAllLabel;
        selectElement.appendChild(optAll);
    }
    CONFIG.PARTIDOS_BUENOS_AIRES.forEach(partido => {
        const opt = document.createElement("option");
        opt.value = partido;
        opt.textContent = partido;
        selectElement.appendChild(opt);
    });
}

function renderNavbar(activePage) {
    const header = document.getElementById("app-header");
    if (!header) return;
    const user = JSON.parse(localStorage.getItem("hc_user") || "null");

    const navLink = (href, id, label) => {
        const isActive = activePage === id;
        const cls = isActive
            ? "px-4 py-2 rounded-pill text-xs sm:text-sm font-semibold bg-brand-card text-brand-primary border border-brand-tagBg"
            : "px-4 py-2 rounded-pill text-xs sm:text-sm font-semibold text-brand-textMuted hover:text-brand-primary transition-colors";
        return `<a href="${href}" class="${cls}">${label}</a>`;
    };

    header.innerHTML = `
        <div class="max-w-7xl mx-auto px-4 py-3 flex flex-wrap justify-between items-center gap-3">
            <a href="index.html" class="flex items-center space-x-2">
                <i class="fa-solid fa-paw text-brand-accent text-2xl"></i>
                <div class="flex flex-col">
                    <span class="font-bold text-lg tracking-tight leading-none text-brand-primary">${CONFIG.APP_NAME}</span>
                    <span class="text-[10px] tracking-widest uppercase text-brand-textMuted font-semibold">${CONFIG.SUBTITLE}</span>
                </div>
            </a>
            <nav class="flex flex-wrap items-center gap-1 bg-brand-tagBg/40 p-1 rounded-pill border border-brand-tagBg">
                ${navLink("index.html", "inicio", "Inicio")}
                ${navLink("catalogo.html", "catalogo", "Adopciones y Perdidos")}
                ${navLink("campanas.html", "campanas", "Campañas")}
                ${navLink("municipios.html", "municipios", "Municipios")}
                ${user
                    ? navLink("dashboard.html", "dashboard", "Mi Panel")
                    : navLink("login.html", "login", "Ingresar")}
            </nav>
        </div>
    `;
}
