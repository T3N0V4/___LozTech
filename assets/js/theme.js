;(() => {
    const selector = document.getElementById("theme-selector");
    const temas = new Set(["black", "blue", "violet", "cosmos", "grey"]);
    const clave = "loztech-theme";

    function leerTema() {
        try { return localStorage.getItem(clave); }
        catch { return null; }
    }

    function aplicarTema(tema) {
        if (!temas.has(tema)) tema = "black";
        document.documentElement.setAttribute("data-theme", tema);
        if (selector) selector.value = tema;
        try { localStorage.setItem(clave, tema); }
        catch { /* Local files may block storage; navigation links carry the theme. */ }
        document.querySelectorAll('a[href]').forEach(enlace => {
            const destino = new URL(enlace.getAttribute("href"), location.href);
            const actual = new URL(location.href);
            if (destino.protocol !== actual.protocol || destino.host !== actual.host ||
                !destino.pathname.endsWith(".html") ||
                destino.pathname.slice(0, destino.pathname.lastIndexOf("/")) !==
                actual.pathname.slice(0, actual.pathname.lastIndexOf("/"))) return;
            if (enlace.closest(".nav")) {
                if (destino.pathname === actual.pathname) enlace.setAttribute("aria-current", "page");
                else enlace.removeAttribute("aria-current");
            }
            destino.searchParams.set("theme", tema);
            enlace.href = destino.href;
        });
    }

    const solicitado = new URL(location.href).searchParams.get("theme");
    aplicarTema(temas.has(solicitado) ? solicitado : leerTema());
    selector?.addEventListener("change", () => {
        aplicarTema(selector.value);
        // Keep a navigation-provided theme from reverting a later choice on reload.
        const actual = new URL(location.href);
        actual.searchParams.set("theme", selector.value);
        try { window.history.replaceState(null, "", actual.href); }
        catch { /* Some local-file environments do not allow history changes. */ }
    });
    window.addEventListener("pageshow", () => {
        aplicarTema(leerTema() || document.documentElement.getAttribute("data-theme"));
    });
    window.addEventListener("storage", evento => {
        if (evento.key === clave) aplicarTema(evento.newValue);
    });
})();