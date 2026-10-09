// =========================================
// SecureBank Guard
// Security Logs JavaScript
// =========================================

// Welcome Message
window.onload = function () {

    alert("Welcome to Security Logs");

    console.log("Security Logs Module Loaded");

};

// =========================================
// Back to Dashboard
// =========================================

document.getElementById("dashboardBtn").addEventListener("click", function () {

    window.location.href = "dashboard.html";

});

// =========================================
// Security Statistics
// =========================================

let totalLogins = 18;
let approvedLogins = 15;
let rejectedLogins = 3;

console.log("Total Logins : " + totalLogins);
console.log("Approved Logins : " + approvedLogins);
console.log("Rejected Logins : " + rejectedLogins);

// =========================================
// Recent Activity
// =========================================

let recentActivity = "Unknown Device Login Attempt";

console.log("Recent Activity : " + recentActivity);

// =========================================
// Last Login Status
// =========================================

let loginStatus = "Approved";

if (loginStatus === "Approved") {

    console.log("Last Login Status : SUCCESS");

}
else {

    console.log("Last Login Status : BLOCKED");

}

// =========================================
// Security Monitoring
// =========================================

let suspiciousActivity = false;

if (suspiciousActivity) {

    alert("Warning! Suspicious Activity Detected.");

}
else {

    console.log("No Suspicious Activity Found.");

}

// =========================================
// Auto Refresh Simulation
// =========================================

setTimeout(function () {

    console.log("Checking for new security logs...");

}, 5000);

// =========================================
// Future Backend Integration
// =========================================

// Flask Backend
// MySQL Database
// Firebase Notification
// AI Risk Analysis
// OTP Verification
// Face Verification
// Emergency Banking Lock

console.log("Future Backend Integration Ready");