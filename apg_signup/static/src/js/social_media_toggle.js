document.addEventListener("DOMContentLoaded", function () {
    const tableBody = document.querySelector(".o-cust-social-media");

    // Function to create a new row
    function createRow() {
        // Create a new table row
        const newRow = document.createElement("tr");

        // Create the Social Media dropdown cell
        const socialMediaCell = document.createElement("td");
        const socialMediaDropdown = document.createElement("select");
        socialMediaDropdown.classList.add("form-select", "form-control-lg", "f14", "o-cust-form-control", "o-cust-layout");
        // socialMediaDropdown.style.marginBottom = "15px";
        socialMediaDropdown.name = "social_section_line";

        // Add options to the dropdown
        const socialMediaOptions = [
            { value: "facebook", text: "Facebook" },
            { value: "twitter", text: "Twitter" },
            { value: "instagram", text: "Instagram" },
            { value: "linkedin", text: "LinkedIn" },
            { value: "youtube", text: "YouTube" },
            { value: "x_portal", text: "X Portal" }
        ];
        socialMediaOptions.forEach(function (optionData) {
            const option = document.createElement("option");
            option.value = optionData.value;
            option.text = optionData.text;
            socialMediaDropdown.appendChild(option);
        });

        socialMediaCell.appendChild(socialMediaDropdown);

        // Create the Link input field cell
        const linkCell = document.createElement("td");
        const linkInput = document.createElement("input");
        linkInput.type = "text";
        linkInput.name = "social_section_line";
        linkInput.placeholder = "Enter Link";
        linkInput.classList.add("form-control", "form-control-lg", "f14", "o-cust-form-control", "o-cust-layout");
        // linkInput.style.marginBottom = "15px";

        linkCell.appendChild(linkInput);

        // Create the Delete button cell
        const deleteCell = document.createElement("td");
        const deleteButton = document.createElement("button");
        deleteButton.classList.add("btn");
        deleteButton.style.padding = "5px 0px 5px 0px";
        deleteButton.style.float = "right";

        // Add delete icon
        const deleteIcon = document.createElement("i");
        deleteIcon.classList.add("fa", "fa-trash");
        deleteIcon.style.fontSize = "1.5rem";
        deleteIcon.style.color = "#000000";
        deleteButton.appendChild(deleteIcon);

        // Add event listener to delete the row
        deleteButton.addEventListener("click", function () {
            tableBody.removeChild(newRow);
        });

        deleteCell.appendChild(deleteButton);

        // Append cells to the new row
        newRow.appendChild(socialMediaCell);
        newRow.appendChild(linkCell);
        newRow.appendChild(deleteCell);

        return newRow;
    }

    // Add the first row automatically on page load
    if (tableBody) {
        tableBody.appendChild(createRow());
    }

    // Add a Line Button Functionality
    const addLineButton = document.querySelector("button[name='add_social_media']");
    if (addLineButton) {
        addLineButton.addEventListener("click", function () {
            tableBody.appendChild(createRow());
        });
    }

    // Tooltip functionality
    const tooltipIcons = document.querySelectorAll('.tooltip-icon');

    tooltipIcons.forEach(function (icon) {
        const tooltip = icon.querySelector('.tooltip-content');
        if (tooltip) {
            // Show tooltip on mouseover
            icon.addEventListener('mouseover', function () {
                tooltip.style.display = 'block';
            });

            // Hide tooltip on mouseout
            icon.addEventListener('mouseout', function () {
                tooltip.style.display = 'none';
            });
        }
    });
});
