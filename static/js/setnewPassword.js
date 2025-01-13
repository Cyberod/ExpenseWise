const showPasswordToggle1 = document.querySelector(".showPasswordToggle1");
const showPasswordToggle2 = document.querySelector(".showPasswordToggle2");

const passwordField1 = document.querySelector("#passwordField1");
const passwordField2 = document.querySelector("#passwordField2");



showPasswordToggle1.addEventListener("click", (e) => {
    if (showPasswordToggle1.textContent === "SHOW") {
        showPasswordToggle1.textContent = "HIDE"
        passwordField1.setAttribute("type", "text")
    }
    else {
    showPasswordToggle1.textContent = "SHOW"
    passwordField1.setAttribute("type", "password")
    }
})


showPasswordToggle2.addEventListener("click", (e) => {
    if (showPasswordToggle2.textContent === "SHOW") {
        showPasswordToggle2.textContent = "HIDE"
        passwordField2.setAttribute("type", "text")
    }
    else {
    showPasswordToggle2.textContent = "SHOW"
    passwordField2.setAttribute("type", "password")
    }
})