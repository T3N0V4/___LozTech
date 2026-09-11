const buscador =
    document.getElementById(
        "driver-search"
    );

const filas =
    document.querySelectorAll(
        "#drivers-table tbody tr"
    );

buscador?.addEventListener(
    "input",
    () => {

        const texto =
            buscador.value
                .toLowerCase();

        filas.forEach(
            fila => {

                const contenido =
                    fila.textContent
                        .toLowerCase();

                fila.style.display =
                    contenido.includes(
                        texto
                    )
                        ? ""
                        : "none";
            }
        );
    }
);