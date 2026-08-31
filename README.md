# 🛡️ Fraud Risk Manager

### AI-Powered Real-Time Transaction Fraud Detection

Fraud Risk Manager is a real-time transaction intelligence and fraud detection system that combines a rule-based risk engine with a Random Forest machine learning model.

The system analyzes transaction behavior, calculates a risk score from 0–100, predicts fraud probability, and recommends one of three actions:

- ✅ APPROVE — Low risk
- ⚠️ REVIEW — Medium risk
- 🚨 BLOCK — High risk

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
- Automated API tests
- Health monitoring endpoint

---

## 🧠 How It Works

A transaction passes through multiple layers of analysis:

```text
Transaction
     │
     ▼
Input Validation
     │
     ▼
Rule-Based Risk Engine
     │
     ├── Transaction Amount
     ├── Location Change
     ├── New Device
     ├── Failed Login Attempts
     ├── Transaction Velocity
     └── User Behavioral History
     │
     ▼
Random Forest ML Model
     │
     ▼
ML Fraud Probability
     │
     ▼
Combined Risk Score
     │
     ▼
┌───────────────┐
│ Risk Decision │
├───────────────┤
│ LOW → APPROVE │
│ MEDIUM → REVIEW│
│ HIGH → BLOCK  │
└───────────────┘
     │
     ▼
SQLite Database
     │
     ▼
Dashboard / API