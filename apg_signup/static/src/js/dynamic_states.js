// /** 
//  * File: dynamic_states.js 
//  * Description: Dynamically load states based on selected country in Odoo 18 website forms
//  */
// odoo.define('apg_signup.dynamic_states', function (require) {
//     'use strict';

//     const publicWidget = require('web.public.widget');

    

//     return publicWidget.registry.DynamicStates;
// });

/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.DynamicStates = publicWidget.Widget.extend({
    selector: '#billing_address_row_cust', // Form container selector
    events: {
        'change .js_country_select': '_onCountryChange', // Country dropdown change event
        'change .js_state_select': '_onStateChange', // State dropdown change event
    },

    /**
     * Called when the country dropdown value changes.
     * Dynamically fetch and update the states dropdown based on the selected country.
     */

    _onCountryChange: async function () {
        const countrySelect = document.querySelector(".js_country_select");
        // const $countrySelect = $(event.currentTarget);
        const countryId = countrySelect.value; // Get selected country ID
        const $stateSelect = this.$('.js_state_select');

        if (!countryId) {
            $stateSelect.html('<option value="">Select State</option>').prop('disabled', true);
            return;
        }
        
        const url = `/get_states_by_country`;
        const params = {
            'country_id' : countryId,
        };
        const states = await rpc(url, params);
        if (states.length > 0) {
            let options = '<option value="">Select State</option>';
            states.forEach(function (state) {
                options += `<option value="${state.id}">${state.name}</option>`;
            });
            $stateSelect.html(options).prop('disabled', false);
            
        } else {
            $stateSelect.html('<option value="">No States Available</option>').prop('disabled', true);
        }
    },

    _onStateChange: async function (ev) {
        let state_id = $(ev.currentTarget).val();
        try {
            const url = `/update_location`;
            const params = {
                'state_id' : state_id,
            };
            const response = await rpc(url, params);
            if (response['success'] == true) {

            }else {
                alert('Failed to update.');
            }
        }catch (error) {
            alert('Failed to update.');
        }

    }
});