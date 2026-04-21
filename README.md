# 💳 Credit Card Fraud Detection System



https://github.com/user-attachments/assets/7f238e5d-9c08-4c0d-9b96-e093e3912ce2


A full-stack application that predicts whether a financial transaction is **fraudulent or not** using a Machine Learning model.

---

##  What This Project Does

* Takes transaction details as input
* Sends data to a backend API
* Uses a trained ML model to predict fraud
* Displays the result in a web interface

---

## 📁 Project Structure

```text
backend/        → FastAPI + ML model
frontend/       → Streamlit UI
notebook/       → Model training
docker-compose.yaml
```

---

#  Run with Docker Compose (Recommended)

### 1. Clone the repository

```bash
git clone <your-repo-link>
cd <repo-folder>
```

---

### 2. Create Docker network (one-time)

```bash
docker network create AIservice
```

---

### 3. Start the project

```bash
docker-compose up --build
```

---

### 4. Open in browser

* Frontend → http://localhost:8501
* Backend → http://localhost:8000

---

#  Run with Docker (Manual Method)

##  Backend

```bash
cd backend
docker build -t fraud-backend .
docker run -p 8000:8000 fraud-backend
```

---

##  Frontend

```bash
cd frontend
docker build -t fraud-frontend .
docker run -p 8501:8501 fraud-frontend
```

---

###  Important

If running manually, update the frontend API URL to:

```text
http://localhost:8000/predict
```

---

#  Run Without Docker

## Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

---

## Frontend

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

---

##  How It Works

1. User enters transaction details
2. Frontend sends data to backend
3. Backend loads trained model (`credit_fraud.pkl`)
4. Model predicts fraud or not
5. Result is displayed

---

##  Usage

1. Open the web app
2. Enter transaction details
3. Click **Detection Result**
4. View prediction

---

##  License

This project is for educational purposes.
