function getCurrentUser() {
    const raw = localStorage.getItem("hc_user");
    return raw ? JSON.parse(raw) : null;
}

function saveSession(authResponse) {
    localStorage.setItem("hc_token", authResponse.access_token);
    localStorage.setItem("hc_user", JSON.stringify(authResponse.usuario));
}

function logout() {
    localStorage.removeItem("hc_token");
    localStorage.removeItem("hc_user");
    window.location.href = "login.html";
}

function requireAuth() {
    const token = localStorage.getItem("hc_token");
    const user = getCurrentUser();
    if (!token || !user) {
        window.location.href = "login.html";
        return null;
    }
    return user;
}
