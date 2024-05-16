$(document).ready(function() {
    console.log("Registration JS Loaded!");
    
    const form = document.getElementById('register-form');
    const submitButton = document.getElementById('register-submit-btn');

    form.addEventListener('input', function() {
        if (form.checkValidity()) {
            console.log(form.checkValidity())
            submitButton.disabled = false;

        } else {
            submitButton.disabled = true;
        }
    }); 
});