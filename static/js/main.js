
// Get all nav links
const navLinks = document.querySelectorAll('.nav-link');

// Get current path
const currentPath = window.location.pathname;

// Add click handler to each nav link
navLinks.forEach(link => {
    // Set active class based on current URL path
    if (link.getAttribute('href') === currentPath) {
        link.classList.add('active');
    }

    link.addEventListener('click', function() {
        // Remove active class from all links
        navLinks.forEach(navLink => navLink.classList.remove('active'));
        // Add active class to clicked link
        this.classList.add('active');
        // Store active link path in localStorage
        localStorage.setItem('activeNavLink', this.getAttribute('href'));
    });
});

// Check localStorage on page load
document.addEventListener('DOMContentLoaded', () => {
    const activeNavPath = localStorage.getItem('activeNavLink');
    if (activeNavPath) {
        navLinks.forEach(link => {
            if (link.getAttribute('href') === activeNavPath) {
                link.classList.add('active');
            }
        });
    }
});




