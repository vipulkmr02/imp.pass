function clear_message() {
    document.querySelector("#message").innerText = "Cleared!";
}

document.addEventListener("click", (event) => {
    if (event.detail == 3)
        clear_message();

})