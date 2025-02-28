// odoo.define('apg_portal_dashboard.sidebar_menu', function (require) {
//     "use strict";
/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.customMenu = publicWidget.Widget.extend({
    selector: '#left-menu li',
    events: {
        'click': '_onMenuItemClick',
    },

    _onMenuItemClick: function (ev) {
        var page = $(ev.currentTarget).data('page');
        $.get('/my/' + page, function(response) {
            $('#portal_common_category').html(response);
        });
    },
});
// var header = document.getElementById("left-menu");
// var btns = header.getElementsByClassName("list");
// for (var i = 0; i < btns.length; i++) {
//     btns[i].addEventListener("click", function() {
    // var current = document.getElementById("left-menu").getElementsByClassName("active")[0];
    // var current = header.getElementsByTagName("li").getElementsByClassName("active");
//   current[0].className = current[0].className.replace(" active", "");
//   this.className += " active";
//   });
// }
// });
// $(document).ready(function() {
//   $('#left-menu li').on('click', function() {
//     const page = $(this).data('page');
    
//     // Fetch data from Odoo controllers dynamically
//     $.get('/website/get_content/' + page, function(response) {
//       $('#content-area').html(response);
//     });
//   });
// });
