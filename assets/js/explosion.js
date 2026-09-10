window.addEventListener(
    "load",
    () => {

        const explosion =
            document.getElementById(
                "explosion"
            );

        const cards =
            document.querySelectorAll(
                ".card"
            );


        if (!explosion) {
            return;
        }


        cards.forEach(
            (card) => {

                const x =
                    Math.floor(
                        Math.random()
                        * 180
                        - 90
                    );

                const y =
                    Math.floor(
                        Math.random()
                        * 140
                        - 70
                    );

                const rotation =
                    Math.floor(
                        Math.random()
                        * 16
                        - 8
                    );


                card.style.setProperty(
                    "--explode-x",
                    `${x}px`
                );

                card.style.setProperty(
                    "--explode-y",
                    `${y}px`
                );

                card.style.setProperty(
                    "--explode-r",
                    `${rotation}deg`
                );
            }
        );


        setTimeout(
    () => {

        document.body
            .classList
            .add(
                "explosion-activa"
            );

        explosion.style.opacity = "0";

        setTimeout(
            () => {
                explosion.remove();
            },
            250
        );

        setTimeout(
            () => {
                document.body
                    .classList
                    .remove(
                        "explosion-activa"
                    );
            },
            1500
        );

    },
    900
);})