$(document).ready(function() {
    var currentUrl = window.location.pathname;
    console.log(">>>>>>>>>>currentUrl<<<<<<<<<",currentUrl)
    if (currentUrl === '/forumsection') {
        $("header").hide();
        $("footer").hide();
    }
});