document.addEventListener("DOMContentLoaded", () => {

    const input = document.getElementById("guess");

    if (!input) {
        return;
    }

    input.addEventListener("input", () => {

        input.value = input.value
            .replace(/[^a-zA-Z]/g, "")
            .toUpperCase()
            .slice(0, 5);

    });

});