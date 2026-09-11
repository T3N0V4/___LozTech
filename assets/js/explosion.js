;(() => {
    function iniciarExplosion() {
        const explosion = document.getElementById("explosion");
        if (!explosion) return;
        const esPanel = /(?:^|\/)index\.html$/i.test(location.pathname);
        const movimientoReducido = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
        if (!esPanel || movimientoReducido) {
            explosion.remove();
            return;
        }

        explosion.classList.add("explosion-visible");
        document.querySelectorAll(".card").forEach(card => {
            card.style.setProperty("--explode-x", `${Math.floor(Math.random() * 180 - 90)}px`);
            card.style.setProperty("--explode-y", `${Math.floor(Math.random() * 140 - 70)}px`);
            card.style.setProperty("--explode-r", `${Math.floor(Math.random() * 16 - 8)}deg`);
        });
        setTimeout(() => {
            document.body.classList.add("explosion-activa");
            explosion.style.opacity = "0";
            setTimeout(() => explosion.remove(), 250);
            setTimeout(() => document.body.classList.remove("explosion-activa"), 1500);
        }, 900);
    }
    if (document.readyState === "complete") iniciarExplosion();
    else window.addEventListener("load", iniciarExplosion, { once: true });
})();