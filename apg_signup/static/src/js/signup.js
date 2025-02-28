/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

const otpField = document.querySelector('#otp_input');
const getOtpButton = document.querySelector('#get_otp');
const confirmButton = document.querySelector('#confirm_otp');
const phoneField = document.querySelector('#phone');
const emailField = document.querySelector('#login');
const submitButton = document.querySelector('#submit_button');

if (otpField) otpField.style.display = 'none';
if (confirmButton) confirmButton.style.display = 'none';

publicWidget.registry.customSignup = publicWidget.Widget.extend({
    selector: '.cust_signup_form',
    events: {
        'click .o_generate_otp': 'o_generate_otp',
        'click .o_confirm_otp': 'o_confirm_otp',
    },

    /**
     * @private
     */
    o_generate_otp: async function () {
        console.log(">>>>>>>>>>>>>>>0000000<<<<<<<<<<<<<,")
        const phoneValue = phoneField.value;
        const phonePattern = /^\d{10}$/;

        if (!phonePattern.test(phoneValue)) {
            alert('Please enter a valid phone number with exactly 10 digits.');
            phoneField.focus();
            return;
        }

        try {
            const url = `/generate/otp`;
            const params = {
                'mobile' : phoneValue,
            };
            const response = await rpc(url, params);
            if (response['true'] == true) {
                console.log("OTP sent successfully:", response);
                alert('OTP sent to your phone. Please check.');

                // Show OTP input and confirm button
                if (otpField) otpField.style.display = 'block';
                if (confirmButton) confirmButton.style.display = 'block';

                // Optionally, store the OTP server response in a hidden field
                // if (otpHiddenField) otpHiddenField.value = response.otp;
                phoneField.readOnly = true;
                getOtpButton.style.display = 'none';
            } else {
                alert(response['error'] || 'Failed to generate OTP. Please try again.');
            }
        } catch (error) {
            console.error('Error during OTP generation:', error);
            alert('An error occurred while generating OTP. Please try again later.');
        }
    },

    o_confirm_otp: async function () {
        console.log(">>>>>>>>>>>>>>>t2<<<<<<<<<<<<<,")
        const enteredOtp = otpField.value;
        const phoneValue = phoneField.value;

        if (!enteredOtp) {
            alert('Please enter the OTP.');
            otpField.focus();
            return;
        }

        try {
            const url = `/otp/verification`;
            const params = { mobile: phoneValue, otp: enteredOtp };
            const response = await rpc(url, params);
            console.log("OTP Verification Response:", response);

            if (response['true'] === true) {
                alert('OTP verified successfully!');
                // is_otp_verify.checked = true;

                // Hide OTP input and confirm button after successful verification
                otpField.style.display = 'none';
                confirmButton.style.display = 'none';
            } else {
                alert(response['error'] || 'Invalid OTP. Please try again.');
            }
        } catch (error) {
            console.error('Error during OTP verification:', error);
            alert('An error occurred during OTP verification. Please try again later.');
        }
    },
});
