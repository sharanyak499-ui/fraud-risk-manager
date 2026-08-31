# Fraud Risk Manager

### AI-Powered Real-Time Transaction Fraud Detection

Fraud Risk Manager is a real-time transaction intelligence system that combines rule-based risk analysis with a machine learning model to identify potentially fraudulent transactions.

## Features

- Real-time transaction risk analysis
- Rule-based fraud detection
- Random Forest machine learning model
- Fraud probability prediction
- Risk score from 0 to 100
- LOW, MEDIUM and HIGH risk classification
- APPROVE, REVIEW and BLOCK decisions
- Transaction history using SQLite
- User transaction velocity detection
- User average transaction amount analysis
- ML feature importance visualization
- Fraud alert dashboard
- Health monitoring endpoint
- REST API with FastAPI
- Interactive web dashboard

## Technology Stack

- Python
- FastAPI
- SQLite
- Pandas
- Scikit-learn
- Joblib
- Pydantic
- HTML
- CSS
- JavaScript
- Random Forest Classifier

## Machine Learning

The fraud detection model uses the following transaction features:

- Transaction amount
- Location change
- New device
- Failed login attempts
- Transaction velocity

The current model achieves approximately 94.25% test accuracy on the generated dataset.

## Risk Engine

The system combines multiple risk signals including:

- Transaction amount
- Location changes
- New device detection
- Failed login attempts
- Transaction velocity
- User transaction history
- User average transaction amount
- Machine learning fraud prediction

The final risk score determines the transaction decision:

| Risk Level | Decision |
|------------|----------|
| LOW | APPROVE |
| MEDIUM | REVIEW |
| HIGH | BLOCK |

## API Endpoints

### Health Check

GET `/health`

Returns the health status of the application, ML model and database.

### Analyze Transaction

POST `/check-risk`

Analyzes a transaction and returns:

- Risk score
- Risk level
- Decision
- Risk factors
- ML prediction
- Fraud probability

### Transaction History

GET `/transactions`

Returns previously analyzed transactions.

### Transaction Lookup

GET `/transactions/{transaction_id}`

Returns details of a specific transaction.

### ML Model Information

GET `/model-info`

Returns the ML model type and feature importance.

## Running the Project

Create and activate the virtual environment:

```text
python -m venv .venv
.venv\Scripts\activate

## Dashboard Screenshots

### Fraud Risk Dashboard
![Fraud Risk Dashboard](Screenshot%202026-08-31%20190029.png)

### Transaction Risk Analysis
![Transaction Risk Analysis](Screenshot%202026-08-31%20190048.png)

### Transaction History
![Transaction History](Screenshot%202026-08-31%20190108.png)
## Running the Project

Create and activate the virtual environment:

```text
python -m venv .venv
.venv\Scripts\activate
