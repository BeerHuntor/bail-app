$(document).ready(function() {
    console.log("Registration JS Loaded!");

    // Form validation logic
    const form = document.getElementById('register-form');
    const submitButton = document.getElementById('register-submit-btn');

    if (form) {
        console.log("Form detected");
        form.addEventListener('input', function() {
            console.log("Form input detected");
            if (form.checkValidity()) {
                console.log("Form is valid");
                submitButton.disabled = false;
            } else {
                console.log("Form is invalid");
                submitButton.disabled = true;
            }
        });

        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault(); // Prevent form submission if it's invalid.
                console.log("Form submission prevented due to invalid form");
            }
        });

        // Script to show the modal if there are form errors
        console.log("Checking for errorlist...");
        const errorList = $(".errorlist");
        if (errorList.length) {
            console.log("Error list found, showing modal");
            $('#reg-modal').modal('show');
        } else {
            console.log("No error list found");
        }
    } else {
        console.log("Form not found");
    }
});
