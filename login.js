// Select the form
const form = document.querySelector("form");

// Form Submit Event
form.addEventListener("submit", function(event) {

    // Prevent page refresh
    //event.preventDefault();

    // Get input values
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    // Validation
    if (username === "") {
        alert("Please enter your username.");
        event.preventDefault();
        return;
    }

    if (password === "") {
        alert("Please enter your password.");
        event.preventDefault();
        return;
    }

    if (password.length < 8) {
        alert("Password must contain at least 8 characters.");
        event.preventDefault();
        return;
    }

    // Login Success
    // Login Success
const approve = confirm("Do you approve this login?");

if (!approve) {
    alert("Login Rejected!");
    event.preventDefault();
    return;
}

alert("Login Approved!");
// Form will now submit to Flask automatically
    
    // Redirect to Dashboard
   
});