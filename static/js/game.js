document.addEventListener("DOMContentLoaded", () => {

    const input = document.getElementById("guess");
    const form = document.getElementById("guess-form");

    if (!input) {
        return;
    }

    input.focus();

    input.addEventListener("input", () => {

        input.value = input.value
            .replace(/[^a-zA-Z]/g, "")
            .toUpperCase()
            .slice(0, 5);

    });


    if (form) {

        form.addEventListener("submit", (event) => {

            const guess = input.value.trim();

            if (guess.length !== 5) {

                event.preventDefault();

                input.focus();

                return;
            }

            if (!/^[A-Z]{5}$/.test(guess)) {

                event.preventDefault();

                input.focus();

            }

        });

    }

});