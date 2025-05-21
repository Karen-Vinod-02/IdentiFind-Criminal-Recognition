document.addEventListener("DOMContentLoaded", function () {
    // Hide registration form by default
    document.getElementById("register").style.display = "none";

    // Attach event listeners to buttons
    document.getElementById("loginBtn").addEventListener("click", function () {
        toggleForms("login");
    });

    document.getElementById("registerBtn").addEventListener("click", function () {
        toggleForms("register");
    });

    // Attach event listener to menu button
    document.querySelector(".nav-menu-btn i").addEventListener("click", toggleMenu);
});

// Function to toggle navigation menu (for mobile)
function toggleMenu() {
    let menu = document.getElementById("navMenu");
    menu.classList.toggle("responsive");
}

// Function to toggle between login and registration forms
function toggleForms(formType) {
    let loginForm = document.getElementById("login");
    let registerForm = document.getElementById("register");
    let loginBtn = document.getElementById("loginBtn");
    let registerBtn = document.getElementById("registerBtn");

    if (formType === "login") {
        loginForm.style.display = "block";
        registerForm.style.display = "none";
        loginBtn.classList.add("white-btn");
        registerBtn.classList.remove("white-btn");
    } else {
        loginForm.style.display = "none";
        registerForm.style.display = "block";
        registerBtn.classList.add("white-btn");
        loginBtn.classList.remove("white-btn");
    }
}
