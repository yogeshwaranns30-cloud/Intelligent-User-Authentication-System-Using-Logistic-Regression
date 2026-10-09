// =====================================
// Trusted Device Management JavaScript
// =====================================

// Welcome Message
window.onload = function () {
    alert("Welcome to Trusted Device Management");
};

// Change Trusted Device
document.getElementById("changeDeviceBtn").addEventListener("click", function () {

    let confirmChange = confirm("Do you want to change your trusted device?");

    if (confirmChange) {
        alert("Trusted Device Change Request Submitted.");
    }

});

// Remove Trusted Device
document.getElementById("removeDeviceBtn").addEventListener("click", function () {

    let confirmRemove = confirm("Are you sure you want to remove the trusted device?");

    if (confirmRemove) {
        alert("Trusted Device Removed Successfully.");
    }

});

// View Device History
document.getElementById("historyBtn").addEventListener("click", function () {

    alert(
        "Device History\n\n" +
        "✔ Samsung Galaxy S24 Ultra - Verified\n" +
        "✔ OnePlus 11 - Removed"
    );

});

// Back to Dashboard
document.getElementById("dashboardBtn").addEventListener("click", function () {

    window.location.href = "dashboard.html";

});

// ===============================
// Security Information
// ===============================

const trustedDevice = true;
const notificationEnabled = true;
const aiProtection = true;
const emergencyLock = false;

console.log("Trusted Device :", trustedDevice);
console.log("Push Notification :", notificationEnabled);
console.log("AI Protection :", aiProtection);
console.log("Emergency Banking Lock :", emergencyLock);

// ===============================
// Device Status
// ===============================

let deviceStatus = "Verified";

if (deviceStatus === "Verified") {

    console.log("Trusted Device Status : VERIFIED");

} else {

    alert("Warning! Device is not verified.");

}

// ===============================
// Device Fingerprint
// ===============================

let fingerprint = "FP-45879231";

console.log("Device Fingerprint :", fingerprint);

// ===============================
// Last Login
// ===============================

let lastLogin = "Today - 10:45 AM";

console.log("Last Login :", lastLogin);

// ===============================
// AI Monitoring
// ===============================

let aiRiskScore = 18;

if (aiRiskScore < 40) {

    console.log("AI Risk : LOW");

}
else if (aiRiskScore >= 40 && aiRiskScore <= 70) {

    console.log("AI Risk : MEDIUM");

}
else {

    console.log("AI Risk : HIGH");

}

// ===============================
// Security Alert
// ===============================

let suspiciousLogin = false;

if (suspiciousLogin) {

    alert("⚠ Suspicious Login Detected!");

}
else {

    console.log("No Suspicious Activity Detected.");

}