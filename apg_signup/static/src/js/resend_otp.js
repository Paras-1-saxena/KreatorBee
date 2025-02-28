/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

const signUpDiv = document.querySelector('#div_signup');
const getOtpDiv = document.querySelector('#div_generate_otp');
const otpDiv = document.querySelector('#div_otp');
const signInDiv = document.querySelector('#o_signin_div');
const mobileNo = document.querySelector('#phone');

publicWidget.registry.resendOtp = publicWidget.Widget.extend({
    selector: '#div_otp',
    events: {
        'click .o-cust-resend-otp': 're_generate_otp',
    },

    /**
     * @private
     */
    re_generate_otp: async function () {
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
                alert('OTP Resend to your phone. Please check.');

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
});
