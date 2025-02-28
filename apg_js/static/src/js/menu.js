document.getElementById("burgerMenu").addEventListener("click", function() {
    const sidebar = document.getElementById("sidebar");
    const mainContent = document.querySelector(".main-content");
    const burgerIcon = document.querySelector("#burgerMenu .navbar-toggler-icon i");

    // Toggle the 'collapsed' class on the sidebar
    sidebar.classList.toggle("collapsed");
    // Toggle the 'shifted' class on the main content
    mainContent.classList.toggle("shifted");

    // Change the icon to close icon when the menu is open, burger icon when closed
    if (sidebar.classList.contains("collapsed")) {
        burgerIcon.classList.remove("fa-times");
        burgerIcon.classList.add("fa-bars");
    } else {
        burgerIcon.classList.remove("fa-bars");
        burgerIcon.classList.add("fa-times");
    }
    });

    $('.nav-link').click(function(e) {
    if ($(window).width() <= 768) {
        e.preventDefault();
        var submenu = $(this).next('.submenu');
        submenu.slideToggle();
        $(this).find('.fas').toggleClass('fa-angle-left fa-angle-down');
    } else {
        $('.nav-link .fas').removeClass('fa-angle-left');
    }
    });

    $(window).resize(function() {
    if ($(window).width() > 768) {
        $('.submenu').hide(); // Ensure submenus are shown on desktop
    } else {
        $('.submenu').show();
    }
});
var currentUrl = window.location.pathname;  // Get the current URL path
// Find all <a> tags on the page
var links = document.querySelectorAll("a");

// Loop through all <a> tags
links.forEach(function(link) {
    // If the href of the <a> matches the current URL, add the 'active' class
    if (link.getAttribute("href") === currentUrl) {
        link.classList.add("active");
    }
});
