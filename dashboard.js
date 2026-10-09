// ===============================
// Secure Banking Dashboard
// ===============================

// Welcome Message
window.onload = function () {
    alert("Welcome to Secure Banking Dashboard!");
};

// Quick Action Buttons
const buttons = document.querySelectorAll("button");

// Transfer Money
buttons[0].addEventListener("click", function () );

// Transaction History
buttons[1].addEventListener("click", function () {
    alert("Transaction History Module will be available soon.");
});

// Add Beneficiary
buttons[2].addEventListener("click", function () {
    alert("Add Beneficiary Module will be available soon.");
});

// Trusted Device
buttons[3].addEventListener("click", function () {
   window.location.href = "/trusted-device";
});
//Security Logs
buttons[4].addEventListener("click", function () {
    window.location.href = "/security-logs";
});
// Logout Button
buttons[5].addEventListener("click", function () {

    let confirmLogout = confirm("Are you sure you want to logout?");

    if (confirmLogout) {

        alert("Logout Successful!");

        window.location.href = "/logout";
    }

});

// Security Status
console.log("Security Status : Protected");

// AI Risk Score
let riskScore = 18;

if (riskScore < 40) {

    console.log("Risk Level : LOW");

}
else if (riskScore >= 40 && riskScore <= 70) {

    console.log("Risk Level : MEDIUM");

}
else {

    console.log("Risk Level : HIGH");

}

// Current Login Location
let locationName = "Chennai, India";

console.log("Current Login : " + locationName);

// Last Login Time
let lastLogin = "Today - 10:45 AM";

console.log("Last Login : " + lastLogin);

// Security Alert
let suspiciousActivity = false;

if (suspiciousActivity) {

    alert("⚠ Suspicious Login Detected!");

}
else {

    console.log("No suspicious activity detected.");

}