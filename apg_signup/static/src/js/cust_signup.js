/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

const allOtpInputs = document.querySelectorAll('.otp-input')
const signUpDiv = document.querySelector('#div_signup');
const getOtpDiv = document.querySelector('#div_generate_otp');
const otpDiv = document.querySelector('#div_otp');
const signInDiv = document.querySelector('#o_signin_div');
const otpVerifiedDiv = document.querySelector('#div_otp_verified');
// const confirmButton = document.querySelector('#confirm_otp');
const mobileNo = document.querySelector('#phone');
// const emailField = document.querySelector('#login');
// const submitButton = document.querySelector('#submit_button');

// if (otpField) otpField.style.display = 'none';
// if (confirmButton) confirmButton.style.display = 'none';

publicWidget.registry.custSignup = publicWidget.Widget.extend({
    selector: '.o-cust-signup-form',
    events: {
        'click .o-cust-otp-button': 'generate_otp',
        'click .otp-verify': 'confirm_otp',
    },

    /**
     * @private
     */
    generate_otp: async function () {
        const mobileValue = mobileNo.value;
        const phonePattern = /^\d{10}$/;

        if (!phonePattern.test(mobileValue)) {
            alert('Please enter a valid phone number with exactly 10 digits.');
            mobileNo.focus();
            return;
        }

        try {
            const url = `/generate/otp`;
            const params = {
                'mobile' : mobileValue,
            };
            const response = await rpc(url, params);
            if (response['true'] == true) {
                console.log("OTP sent successfully:", response);
                getOtpDiv.classList.add("o-cust-hide")
                signInDiv.classList.add("o-cust-hide")
                signUpDiv.classList.add("o-cust-hide")
                otpDiv.style.display = 'block';
                mobileNo.readOnly = true;
                // alert('OTP sent to your phone. Please check.');

                // Show OTP input and confirm button
                // if (otpField) otpField.style.display = 'block';
                // if (confirmButton) confirmButton.style.display = 'block';

                // Optionally, store the OTP server response in a hidden field
                // if (otpHiddenField) otpHiddenField.value = response.otp;
                
                // getOtpDiv.style.display = 'none';
            } else {
                alert(response['error'] || 'Failed to generate OTP. Please try again.');
            }
        } catch (error) {
            console.error('Error during OTP generation:', error);
            alert('An error occurred while generating OTP. Please try again later.');
        }
    },

    confirm_otp: async function () {
        let otpCode = '';
        const phoneValue = mobileNo.value;
        allOtpInputs.forEach(input => {
            if (input.value.trim() === '') {
                alert('Please enter the OTP.');
            }
        });
        allOtpInputs.forEach(input => {
            otpCode += input.value.trim(); // Trim to remove any accidental whitespace
        });
        console.log('Merged OTP:', otpCode);
        if (otpCode.length === 6) {
            try {
                const url = `/otp/verification`;
                const params = { mobile: phoneValue, otp: otpCode };
                const response = await rpc(url, params);
                console.log("OTP Verification Response:", response);

                if (response['true'] === true) {
                    signUpDiv.classList.remove("o-cust-hide")
                    otpVerifiedDiv.classList.remove("o-cust-hide")
                    otpVerifiedDiv.classList.add("o-cust-visible")
                    signUpDiv.classList.add("o-cust-visible")
                    otpDiv.style.display = 'none';
                    // alert('OTP verified successfully!');
                    // is_otp_verify.checked = true;

                    // Hide OTP input and confirm button after successful verification
                    // otpField.style.display = 'none';
                    // confirmButton.style.display = 'none';
                } else {
                    alert(response['error'] || 'Invalid OTP. Please try again.');
                }
            } catch (error) {
                console.error('Error during OTP verification:', error);
                alert('An error occurred during OTP verification. Please try again later.');
            }
        } 
        else {
            console.log('Incomplete OTP. Please fill all fields.');
        }
    },
});
