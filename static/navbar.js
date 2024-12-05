// Toggle Button
const navMenu = document.getElementById("nav-menu");
const navLinks = document.querySelectorAll(".nav-link"); // Select all elements with the 'nav-link' class
const hamburger = document.getElementById("hamburger");

// Toggle menu visibility when clicking the hamburger icon
hamburger.addEventListener("click", () => {
    navMenu.classList.toggle("left-[0]"); // Toggle the class to show/hide the mobile menu
    hamburger.classList.toggle("ri-close-line"); // Change hamburger to "X" when menu is open
    hamburger.classList.toggle("ri-menu-4-line"); // Revert to hamburger icon when menu is closed
});

// Close menu when clicking any of the navigation links
navLinks.forEach(link => {
    link.addEventListener("click", () => {
        navMenu.classList.toggle("left-[0]");// Hide the menu when a link is clicked
        hamburger.classList.toggle("ri-menu-4-line"); // Revert to hamburger icon when menu is closed
        hamburger.classList.toggle("ri-close-line"); // Change hamburger to "X" when menu is open

    });
});