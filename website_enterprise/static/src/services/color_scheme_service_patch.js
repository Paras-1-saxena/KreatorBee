import { browser } from "@web/core/browser/browser";
import { patch } from "@web/core/utils/patch";

// Create a local implementation of color scheme handling (since we can't use the web_enterprise version)
const colorSchemeService = {
    reload() {
        if (document.querySelector("header.o_navbar + .o_action_manager > .o_website_preview")) {
            browser.location.pathname = "/@" + browser.location.pathname;
        } else {
            // Default behavior for reload (you can adjust it as needed)
            window.location.reload();
        }
    },
};

// Patch the service (since we're no longer depending on web_enterprise)
patch(colorSchemeService, {
    reload() {
        if (document.querySelector("header.o_navbar + .o_action_manager > .o_website_preview")) {
            browser.location.pathname = "/@" + browser.location.pathname;
        } else {
            super.reload();
        }
    },
});
