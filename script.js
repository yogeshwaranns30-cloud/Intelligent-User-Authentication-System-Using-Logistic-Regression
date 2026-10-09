// Get the form
const form = document.querySelector("form");

// Form Submit Event
form.addEventListener("submit", function (event) {

    // Prevent form submission
    //event.preventDefault();

    // Get values
    const fullName = document.getElementById("fullname").value.trim();
    const email = document.getElementById("email").value.trim();
    const mobile = document.getElementById("mobile").value.trim();
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    // Check Empty Fields
    if (
        fullName === "" ||
        email === "" ||
        mobile === "" ||
        username === "" ||
        password === "" ||
        confirmPassword === ""
    ) {
        alert("Please fill all the fields.");
        return;
    }

    // Email Validation
    const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;

    if (!email.match(emailPattern)) {
        alert("Please enter a valid email address.");
        return;
    }

    // Mobile Number Validation
    if (mobile.length !== 10 || isNaN(mobile)) {
        alert("Mobile number must contain exactly 10 digits.");
        return;
    }

    // Password Length
    if (password.length < 8) {
        alert("Password must contain at least 8 characters.");
        return;
    }

    // Confirm Password
    if (password !== confirmPassword) {
        alert("Passwords do not match.");
        return;
    }

    // Success
    alert("Validation Successful! Registering...");
    form.submit();
});