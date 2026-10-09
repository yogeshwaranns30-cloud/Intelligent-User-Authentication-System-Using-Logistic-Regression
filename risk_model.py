import numpy as np
from sklearn.linear_model import LogisticRegression


# ==========================================
# LOGIN SECURITY TRAINING DATA
# ==========================================

# Features:
# 1. Login Attempts
# 2. Unusual Login Time
# 3. Unknown Device

# 0 = Normal
# 1 = Suspicious

X = np.array([
    [1, 0, 0],
    [1, 0, 0],
    [2, 0, 0],
    [2, 0, 0],
    [1, 1, 0],
    [2, 1, 0],
    [2, 1, 1],
    [3, 1, 1],
    [4, 1, 1],
    [5, 1, 1]
])


y = np.array([
    0,
    0,
    0,
    0,
    0,
    0,
    1,
    1,
    1,
    1
])


# ==========================================
# CREATE LOGISTIC REGRESSION MODEL
# ==========================================

model = LogisticRegression()

model.fit(X, y)


# ==========================================
# RISK PREDICTION FUNCTION
# ==========================================

def predict_risk(login_attempts, unusual_time, unknown_device):

    data = np.array([
        [login_attempts, unusual_time, unknown_device]
    ])

    probability = model.predict_proba(data)[0][1]

    risk_percentage = round(probability * 100, 2)

    return risk_percentage