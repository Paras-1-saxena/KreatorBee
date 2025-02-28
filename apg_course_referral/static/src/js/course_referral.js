/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
document.addEventListener('DOMContentLoaded', function () {
    const copyButton = document.getElementById('copy_div');  // Copy button ID
    if (copyButton) {
        copyButton.addEventListener('click', function () {
            const fieldTextElement = document.getElementById('generated_url'); 
            console.log(">>>>>>>fieldTextElement>>>>>>>>") 
            // Field ID
            if (fieldTextElement) {
                const fieldText = fieldTextElement.innerText.trim();
                console.log(">>>>>>>fieldTextElement>>>>>>>>",fieldText)   
                // Trim spaces for cleaner copying
                navigator.clipboard.writeText(fieldText).then(() => {
                    alert('Copied to clipboard!');
                }).catch((err) => {
                    console.error('Failed to copy: ', err);
                    alert('Failed to copy. Please try again.');
                });
            } else {
                alert('Element with ID "generated_url" not found.');
            }
        });
    } else {
        alert('Copy button not found.');
    }
});