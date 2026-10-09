from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import sqlite3
import os
import secrets
from dotenv import load_dotenv
from twilio.rest import Client
from risk_model import predict_risk

load_dotenv()

app = Flask(__name__)
app.secret_key = "securebanking123"
VOICE_FOLDER = "voice_samples"

if not os.path.exists(VOICE_FOLDER):
    os.makedirs(VOICE_FOLDER)

def send_sms(mobile, message):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

    client = Client(account_sid, auth_token)

    client.messages.create(
        body=message,
        from_=twilio_number,
        to="+919360278108"
    )


def init_db():

    print(os.path.abspath("database.db"))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            email TEXT NOT NULL,
            mobile TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            trusted_device TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Add voice verification columns if they do not exist
    cursor.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in cursor.fetchall()]

    if "voice_sample" not in columns:
        cursor.execute(
        "ALTER TABLE users ADD COLUMN voice_sample TEXT"
    )

    if "voice_enrolled" not in columns:
        cursor.execute(
        "ALTER TABLE users ADD COLUMN voice_enrolled INTEGER DEFAULT 0"
    )
    

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bank_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            account_holder_name TEXT NOT NULL,
            account_number TEXT NOT NULL,
            bank_name TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trusted_devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            device_name TEXT NOT NULL,
            device_type TEXT NOT NULL,
            device_id TEXT NOT NULL,
            os_version TEXT NOT NULL,
            status TEXT DEFAULT 'Active',
            created_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            receiver_name TEXT NOT NULL,
            receiver_account TEXT NOT NULL,
            amount REAL NOT NULL,
            risk_percentage REAL,
            authentication_method TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS auth_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


# =========================
# HOME
# =========================

@app.route("/")
def home():
    return redirect(url_for("login"))


# =========================
# REGISTRATION
# =========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        mobile = request.form["mobile"]
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users
            (fullname, email, mobile, username, password)
            VALUES (?, ?, ?, ?, ?)
        """, (
            fullname,
            email,
            mobile,
            username,
            password
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("index.html")


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM users
            WHERE username=? AND password=?
        """, (
            username,
            password
        ))

        user = cursor.fetchone()

        if user:

            user_id = user[0]

            # Create login authentication request
            token = secrets.token_urlsafe(32)

            cursor.execute("""
                INSERT INTO auth_requests
                (user_id, token, status)
                VALUES (?, ?, 'pending')
            """, (
                user_id,
                token
            ))

            conn.commit()
            conn.close()

            # Store login information in session
            session["pending_user"] = username
            session["pending_token"] = token

            # Go directly to waiting / trusted approval page
            return redirect(url_for("waiting"))

        else:

            conn.close()

            return "Invalid Username or Password"

    return render_template("login.html")



# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")
def dashboard():

    if "username" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        username=session["username"]
    )


# =========================
# TRANSFER MONEY + RISK ANALYSIS
# =========================

# =========================
# TRANSFER MONEY
# =========================

@app.route("/transfer", methods=["GET", "POST"])
def transfer():

    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        receiver_name = request.form["receiver_name"]
        receiver_account = request.form["receiver_account"]

        try:
            amount = float(request.form["amount"])
        except ValueError:
            return "Invalid amount"

        if amount <= 0:
            return "Amount must be greater than 0"

        # Get current user
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM users WHERE username=?",
            (session["username"],)
        )

        user = cursor.fetchone()

        if not user:
            conn.close()
            return "User not found"

        user_id = user[0]

        # =====================================
        # TRANSACTION AUTHENTICATION DECISION
        # =====================================

        if amount < 10000:

            authentication_method = "Standard Authentication"

            # Save transaction as pending
            cursor.execute("""
                INSERT INTO transactions
                (
                    user_id,
                    receiver_name,
                    receiver_account,
                    amount,
                    risk_percentage,
                    authentication_method,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                receiver_name,
                receiver_account,
                amount,
                None,
                authentication_method,
                "Pending"
            ))

            transaction_id = cursor.lastrowid

            conn.commit()
            conn.close()

            return render_template(
                "otp-verification.html",
                transaction_id=transaction_id,
                amount=amount,
                receiver_name=receiver_name,
                receiver_account=receiver_account
            )

        else:

            authentication_method = "Voice Verification"

            # Save transaction as pending
            cursor.execute("""
                INSERT INTO transactions
                (
                    user_id,
                    receiver_name,
                    receiver_account,
                    amount,
                    risk_percentage,
                    authentication_method,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                receiver_name,
                receiver_account,
                amount,
                None,
                authentication_method,
                "Pending"
            ))

            transaction_id = cursor.lastrowid

            conn.commit()
            conn.close()

            return render_template(
                "voice-verification.html",
                transaction_id=transaction_id,
                amount=amount,
                receiver_name=receiver_name,
                receiver_account=receiver_account
            )

    return render_template("transfer.html")


# =========================
# BANK DETAILS
# =========================

@app.route("/bank-details", methods=["GET", "POST"])
def bank_details():

    if "username" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE username=?",
        (session["username"],)
    )

    user = cursor.fetchone()

    if request.method == "POST":

        account_holder_name = request.form["account_holder_name"]
        account_number = request.form["account_number"]
        bank_name = request.form["bank_name"]

        cursor.execute("""
            INSERT INTO bank_details
            (user_id, account_holder_name, account_number, bank_name)
            VALUES (?, ?, ?, ?)
        """, (
            user[0],
            account_holder_name,
            account_number,
            bank_name
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("dashboard"))

    conn.close()

    return render_template("bank-details.html")


# =========================
# TRUSTED DEVICE
# =========================

@app.route("/trusted-device", methods=["GET", "POST"])
def trusted_device():

    if "username" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE username=?",
        (session["username"],)
    )

    user = cursor.fetchone()

    if request.method == "POST":

        device_name = request.form["device_name"]
        device_type = request.form["device_type"]
        device_id = request.form["device_id"]
        os_version = request.form["os_version"]

        current_date = datetime.now().strftime("%Y-%m-%d")

        cursor.execute("""
            INSERT INTO trusted_devices
            (user_id, device_name, device_type, device_id, os_version, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user[0],
            device_name,
            device_type,
            device_id,
            os_version,
            current_date
        ))

        conn.commit()

    cursor.execute("""
        SELECT id,
               device_name,
               device_type,
               device_id,
               os_version,
               status,
               created_at
        FROM trusted_devices
        WHERE user_id=?
    """, (
        user[0],
    ))

    devices = cursor.fetchall()

    conn.close()

    return render_template(
        "trusted-device.html",
        devices=devices
    )


# =========================
# WAITING
# =========================

@app.route("/waiting")
def waiting():

    if "pending_user" not in session:
        return redirect(url_for("login"))

    return render_template("waiting.html")


# =========================
# APPROVE LOGIN + AI RISK ANALYSIS
# =========================

@app.route("/approve-login")
def approve_login():

    if "pending_user" not in session:
        return redirect(url_for("login"))

    username = session["pending_user"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Get user details
    cursor.execute("""
        SELECT id
        FROM users
        WHERE username=?
    """, (
        username,
    ))

    user = cursor.fetchone()

    if not user:
        conn.close()
        return "User not found"

    user_id = user[0]

    # =====================================
    # LOGIN SECURITY DATA
    # =====================================

    # Demo login attempt count
    login_attempts = 1

    # Check current login time
    current_hour = datetime.now().hour

    # 1 = unusual time
    # 0 = normal time
    unusual_time = 1 if current_hour < 6 or current_hour >= 23 else 0

    # Check trusted device
    cursor.execute("""
        SELECT id
        FROM trusted_devices
        WHERE user_id=? AND status='Active'
    """, (
        user_id,
    ))

    trusted_device = cursor.fetchone()

    # 0 = trusted device
    # 1 = unknown device
    unknown_device = 0 if trusted_device else 1

    # =====================================
    # LOGISTIC REGRESSION RISK ANALYSIS
    # =====================================

    risk_percentage = predict_risk(
        login_attempts,
        unusual_time,
        unknown_device
    )

    print("Login Risk:", risk_percentage, "%")

    # Store risk result in session
    session["risk_percentage"] = risk_percentage

    # Complete login
    session["username"] = username

    session.pop("pending_user", None)
    session.pop("pending_token", None)

    # Check bank details
    cursor.execute("""
        SELECT id
        FROM bank_details
        WHERE user_id=?
    """, (
        user_id,
    ))

    bank = cursor.fetchone()

    conn.close()

    # =====================================
    # GO TO NEXT STAGE
    # =====================================

    if bank:
        return redirect(url_for("dashboard"))

    return redirect(url_for("bank_details"))
# =========================
# DENY LOGIN
# =========================

@app.route("/deny-login")
def deny_login():

    session.pop("pending_user", None)

    return redirect(url_for("security_alert"))


# =========================
# SECURITY ALERT
# =========================

@app.route("/security-alert")
def security_alert():

    return render_template("security-alert.html")


# =========================
# SECURITY LOGS
# =========================

@app.route("/security-logs")
def security_logs():

    if "username" not in session:
        return redirect(url_for("login"))

    return render_template("security-logs.html")


# =========================
# REMOVE DEVICE
# =========================

@app.route("/remove-device/<int:device_id>")
def remove_device(device_id):

    if "username" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM trusted_devices WHERE id=?",
        (device_id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("trusted_device"))


@app.route("/verify-otp", methods=["POST"])
def verify_otp():

    if "username" not in session:
        return redirect(url_for("login"))

    transaction_id = request.form["transaction_id"]
    entered_otp = request.form["otp"]
    print("Entered OTP:", entered_otp)
    # Demo OTP
    correct_otp = "123456"

    if entered_otp != correct_otp:
        return "Invalid OTP. Please try again."

    # Update transaction authentication status
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE transactions
        SET status=?
        WHERE id=? AND user_id=(
            SELECT id FROM users WHERE username=?
        )
    """, (
        "OTP Verified",
        transaction_id,
        session["username"]
    ))

    conn.commit()
    conn.close()

    return render_template(
        "transaction-permission.html",
        transaction_id=transaction_id
    )
@app.route("/verify-voice", methods=["POST"])
def verify_voice():

    if "username" not in session:
        return redirect(url_for("login"))

    transaction_id = request.form["transaction_id"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Check transaction
    cursor.execute("""
        SELECT receiver_name, receiver_account, amount
        FROM transactions
        WHERE id=?
        AND user_id=(
            SELECT id FROM users WHERE username=?
        )
    """, (
        transaction_id,
        session["username"]
    ))

    transaction = cursor.fetchone()

    if not transaction:
        conn.close()
        return "Transaction not found"

    # Demo voice verification
    voice_verified = True

    if voice_verified:

        cursor.execute("""
            UPDATE transactions
            SET status=?
            WHERE id=?
            AND user_id=(
                SELECT id FROM users WHERE username=?
            )
        """, (
            "Voice Verified",
            transaction_id,
            session["username"]
        ))

        conn.commit()
        conn.close()

        return render_template(
            "transaction-permission.html",
            transaction_id=transaction_id
        )

    conn.close()

    return "Voice Verification Failed"
@app.route("/voice-enrollment")
def voice_enrollment():

    if "username" not in session:
        return redirect(url_for("login"))

    return render_template("voice-enrollment.html")
@app.route("/save-voice", methods=["POST"])
def save_voice():

    if "username" not in session:
        return redirect(url_for("login"))

    voice_data = request.form.get("voice_data")

    if not voice_data:
        return "Voice data not received"

    import base64

    try:

        header, encoded_data = voice_data.split(",", 1)

        audio_bytes = base64.b64decode(encoded_data)

        username = session["username"]

        filename = username + "_voice.webm"

        filepath = os.path.join(
            VOICE_FOLDER,
            filename
        )

        with open(filepath, "wb") as file:
            file.write(audio_bytes)

    except Exception as e:

        return "Voice save failed: " + str(e)

    return """
    <h2>✅ Voice Enrollment Successful</h2>
    <p>Your demo voice sample has been saved.</p>
    <a href="/dashboard">Go to Dashboard</a>
    """
@app.route("/complete-transaction", methods=["POST"])
def complete_transaction():

    if "username" not in session:
        return redirect(url_for("login"))

    transaction_id = request.form["transaction_id"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Get transaction details
    cursor.execute("""
        SELECT receiver_name, receiver_account, amount
        FROM transactions
        WHERE id=?
    """, (
        transaction_id,
    ))

    transaction = cursor.fetchone()

    if not transaction:
        conn.close()
        return "Transaction not found"

    receiver_name = transaction[0]
    receiver_account = transaction[1]
    amount = transaction[2]

    # Get current user
    cursor.execute("""
        SELECT id
        FROM users
        WHERE username=?
    """, (
        session["username"],
    ))

    user = cursor.fetchone()

    if not user:
        conn.close()
        return "User not found"

    user_id = user[0]

    # Complete transaction
    cursor.execute("""
        UPDATE transactions
        SET status=?
        WHERE id=? AND user_id=?
    """, (
        "Success",
        transaction_id,
        user_id
    ))

    conn.commit()
    conn.close()

    return render_template(
        "transaction-success.html",
        receiver_name=receiver_name,
        receiver_account=receiver_account,
        amount=amount
    )


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# =========================
# INITIALIZE DATABASE
# =========================

init_db()


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":
    app.run(debug=True)