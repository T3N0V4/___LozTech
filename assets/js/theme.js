const selector =
    document.getElementById(
        "theme-selector"
    );


function aplicarTema(tema) {

    document.documentElement
        .setAttribute(
            "data-theme",
            tema
        );

    if (selector) {
        selector.value = tema;
    }
}


const temaGuardado =
    localStorage.getItem(
        "loztech-theme"
    );


const temaInicial =
    temaGuardado || "black";


aplicarTema(
    temaInicial
);


selector?.addEventListener(
    "change",
    () => {

        const tema =
            selector.value;

        aplicarTema(
            tema
        );

        localStorage.setItem(
            "loztech-theme",
            tema
        );
    }
);