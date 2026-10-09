// =========================================
// Secure Banking Authentication
// Security Alert JavaScript
// =========================================

// Welcome Message
window.onload = function () {

    alert("Security Alert Received on Trusted Mobile");

};

// ==============================
// YES Button
// ==============================

document.getElementById("yesBtn").addEventListener("click", function () {

    let approve = confirm("Do you approve this login request?");

    if (approve) {

        alert("Login request approved.\n\nSecurity verification is in progress...");

        // Next Module (Future)
        // AI Risk Analysis will start here

        window.location.href = "dashboard.html";

    }

});

// ==============================
// NO Button
// ==============================

document.getElementById("noBtn").addEventListener("click", function () {

    let reject = confirm("Reject this login request and activate Emergency Banking Lock?");

    if (reject) {

        alert("Emergency Banking Lock Activated.");

        alert("Online Banking Frozen.");

        alert("Net Banking Temporarily Disabled.");

        alert("Bank Security Team Notified.");

        // Future
        // Backend will freeze the account

    }

});

// ==============================
// Console Messages
// ==============================

console.log("Trusted Mobile Approval Module Loaded");

console.log("Waiting for User Approval...");

// ==============================
// Future Integration
// ==============================

// Firebase Push Notification
// Flask Backend
// AI Risk Analysis
// MySQL Database
// Security Logs