$(document).ready(function() {
    console.log("Registration JS Loaded!");
    
    const form = document.getElementById('register-form');
    const submitButton = document.getElementById('register-submit-btn');

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
            event.preventDefault(); // Prevent form sumbission if it's invalid. 
            console.log("Form submission prevented due to invalidity")
        }
    });
});
