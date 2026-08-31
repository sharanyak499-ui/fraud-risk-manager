# 🛡️ Fraud Risk Manager

### AI-Powered Real-Time Transaction Fraud Detection

Fraud Risk Manager is a real-time transaction intelligence and fraud detection system that combines a rule-based risk engine with a Random Forest machine learning model.

The system analyzes transaction behavior, calculates a risk score from 0–100, predicts fraud probability, and recommends one of three actions:

- ✅ APPROVE — Low risk
- ⚠️ REVIEW — Medium risk
- 🚨 BLOCK — High risk

---

## 🚀 Live Demo

**Dashboard:**  
https://fraud-risk-manager-h2ew.onrender.com

**API Documentation:**  
https://fraud-risk-manager-h2ew.onrender.com/docs

**Health Check:**  
https://fraud-risk-manager-h2ew.onrender.com/health

---

## 🚀 Key Features

- Real-time transaction risk analysis
- Rule-based fraud detection
- Random Forest fraud classification
- ML fraud probability prediction
- Risk score from 0–100
- LOW / MEDIUM / HIGH risk classification
- APPROVE / REVIEW / BLOCK decisions
- Transaction velocity detection
- User transaction behavior analysis
- User average transaction amount analysis
- SQLite transaction storage
- Fraud alert dashboard
- Risk distribution visualization
- ML feature importance
- REST API using FastAPI
- Duplicate transaction protection
- Automated API tests
- Health monitoring endpoint

---

## 🧠 How It Works

A transaction passes through multiple layers of analysis:

```text
Transaction
     |
     v
Input Validation
     |
     v
Rule-Based Risk Engine
     |
     +-- Transaction Amount
     +-- Location Change
     +-- New Device
     +-- Failed Login Attempts
     +-- Transaction Velocity
     +-- User Behavioral History
     |
     v
Random Forest ML Model
     |
     v
ML Fraud Probability
     |
     v
Combined Risk Score
     |
     v
Risk Decision
     |
     +-- LOW    → APPROVE
     +-- MEDIUM → REVIEW
     +-- HIGH   → BLOCK
     |
     v
SQLite Database
     |
     v
Dashboard / REST API

---

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI
- **Machine Learning:** Scikit-learn, Random Forest
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **Testing:** Pytest
- **Deployment:** Render
- **Version Control:** Git & GitHub

---

## 📁 Project Structure

```text
fraud-risk-manager/
│
├── app/
│   ├── ml/
│   │   ├── fraud_dataset.csv
│   │   ├── fraud_model.pkl
│   │   ├── train_model.py
│   │   ├── generate_dataset.py
│   │   ├── feature_importance.py
│   │   └── model_info.py
│   │
│   ├── models/
│   │   └── transaction.py
│   │
│   ├── services/
│   │   ├── database.py
│   │   ├── ml_engine.py
│   │   └── risk_engine.py
│   │
│   ├── static/
│   │   ├── index.html
│   │   └── style.css
│   │
│   └── main.py
│
├── tests/
│   └── test_fraud_manager.py
│
├── requirements.txt
├── Procfile
└── README.md