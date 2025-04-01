$(document).ready(function() {
    var currentUrl = window.location.pathname;
    console.log("Window Size==1==", $(window).width());
    if (window.innerWidth < 768) {  // Adjust width as needed
        console.log("Window Size", window.innerWidth);
        window.location.href = "/mobile-restricted"; // Redirect to the custom page
    }
    // var restricted_urls = [
    //     "/specific-page-1",  // Replace with actual URLs
    //     "/specific-page-2"
    // ];

    // var current_url = window.location.pathname;

    // if (restricted_urls.includes(current_url)){
    //     if (window.innerWidth < 768) {
    //         alert("Access restricted on mobile. Please use a desktop.");
    //         window.history.back(); // Go back to the previous page
    //     }
    // }
    // if (currentUrl === '/forumsection') {
    //     $("header").hide();
    //     $("footer").hide();
});