import streamlit as st
import requests
import json

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Credit Card Fraud Detection",
    page_icon="💳",
    layout="wide"
)

# -----------------------------
# CUSTOM STYLING
# -----------------------------
st.markdown("""
    <style>
    .main-title {
        font-size: 38px;
        font-weight: bold;
        color: #1f4e79;
        margin-bottom: 10px;
    }
    .sub-text {
        font-size: 18px;
        color: #444;
        margin-bottom: 20px;
    }
    .result-box {
        padding: 20px;
        border-radius: 12px;
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        margin-top: 20px;
    }
    .fraud {
        background-color: #ffe6e6;
        color: #b30000;
        border: 2px solid #ff4d4d;
    }
    .safe {
        background-color: #e6ffe6;
        color: #006600;
        border: 2px solid #33cc33;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown('<div class="main-title">💳 Credit Card Fraud Detection System</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-text">Enter transaction details below to predict whether the transaction is <b>fraudulent</b> or <b>not fraudulent</b>.</div>',
    unsafe_allow_html=True
)

# -----------------------------
# OPTIONAL IMAGE
# -----------------------------
try:
    st.image("image.png", use_container_width=True)
except:
    pass

# -----------------------------
# SIDEBAR INFO
# -----------------------------
st.sidebar.title("📌 Instructions")
st.sidebar.info("""
Fill in the transaction details carefully.

This system uses a trained Machine Learning model to classify the transaction as:
- **Fraudulent**
- **Not Fraudulent**
""")

st.sidebar.markdown("---")
st.sidebar.subheader("Transaction Type Mapping")
st.sidebar.write("""
- **0** → Cash In  
- **1** → Cash Out  
- **2** → Debit  
- **3** → Payment  
- **4** → Transfer  
""")

# -----------------------------
# MAIN INPUT SECTION
# -----------------------------
st.subheader("📝 Transaction Details")

col1, col2 = st.columns(2)

with col1:
    sender_name = st.text_input("Sender ID / Name")
    receiver_name = st.text_input("Receiver ID / Name")
    step = st.number_input("Transaction Time Step / Hour", min_value=1, max_value=1000, value=1)
    
    transaction_options = {
        0: "Cash In",
        1: "Cash Out",
        2: "Debit",
        3: "Payment",
        4: "Transfer"
    }
    types = st.selectbox(
        "Transaction Type",
        options=list(transaction_options.keys()),
        format_func=lambda x: f"{x} - {transaction_options[x]}"
    )

with col2:
    amount = st.number_input("Transaction Amount ($)", min_value=0.0, value=1000.0, step=100.0)
    oldbalanceorig = st.number_input("Sender Balance Before Transaction ($)", min_value=0.0, value=5000.0, step=100.0)
    newbalanceorig = st.number_input("Sender Balance After Transaction ($)", min_value=0.0, value=4000.0, step=100.0)
    oldbalancedest = st.number_input("Recipient Balance Before Transaction ($)", min_value=0.0, value=2000.0, step=100.0)
    newbalancedest = st.number_input("Recipient Balance After Transaction ($)", min_value=0.0, value=3000.0, step=100.0)

# -----------------------------
# FRAUD FLAG LOGIC
# -----------------------------
# You can keep this simple logic or later make it smarter
if amount >= 200000:
    isflaggedfraud = 1
else:
    isflaggedfraud = 0

st.markdown("---")

# -----------------------------
# SMART RISK HINTS
# -----------------------------
st.subheader("⚠️ Risk Hints")

risk_points = []

if amount > 100000:
    risk_points.append("High transaction amount detected.")
if types in [1, 4]:
    risk_points.append("Cash Out / Transfer transactions are often more fraud-prone.")
if oldbalanceorig == newbalanceorig and amount > 0:
    risk_points.append("Sender balance did not change despite transaction amount.")
if newbalancedest == oldbalancedest and amount > 0:
    risk_points.append("Recipient balance did not change despite transaction amount.")
if isflaggedfraud == 1:
    risk_points.append("System auto-flagged this transaction due to large amount.")

if risk_points:
    for point in risk_points:
        st.warning(point)
else:
    st.success("No immediate suspicious transaction pattern detected from basic rules.")

# -----------------------------
# PREDICTION BUTTON
# -----------------------------
st.markdown("---")
predict_button = st.button("🔍 Predict Fraud Status", use_container_width=True)

# -----------------------------
# PREDICTION LOGIC
# -----------------------------
if predict_button:
    if sender_name.strip() == "" or receiver_name.strip() == "":
        st.error("Please enter both Sender and Receiver ID / Name.")
    else:
        values = {
            "step": int(step),
            "types": int(types),
            "amount": float(amount),
            "oldbalanceorig": float(oldbalanceorig),
            "newbalanceorig": float(newbalanceorig),
            "oldbalancedest": float(oldbalancedest),
            "newbalancedest": float(newbalancedest),
            "isflaggedfraud": float(isflaggedfraud)
        }

        st.subheader("📄 Transaction Summary")
        st.write(f"""
        **Sender:** {sender_name}  
        **Receiver:** {receiver_name}  
        **Transaction Type:** {transaction_options[types]}  
        **Transaction Amount:** ${amount:,.2f}  
        **Transaction Step / Hour:** {step}  
        **Sender Balance Before:** ${oldbalanceorig:,.2f}  
        **Sender Balance After:** ${newbalanceorig:,.2f}  
        **Recipient Balance Before:** ${oldbalancedest:,.2f}  
        **Recipient Balance After:** ${newbalancedest:,.2f}  
        **System Fraud Flag:** {isflaggedfraud}
        """)

        try:
            # Docker internal backend URL
            response = requests.post(
                "http://backend.docker:8000/predict",
                json=values,
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                prediction = result.get("prediction", "Unknown")

                st.subheader("🧠 Prediction Result")

                if prediction.lower() == "fraudulent":
                    st.markdown(
                        f'<div class="result-box fraud">🚨 FRAUD ALERT: This transaction is predicted to be <b>FRAUDULENT</b>.</div>',
                        unsafe_allow_html=True
                    )
                elif prediction.lower() == "not fraudulent":
                    st.markdown(
                        f'<div class="result-box safe">✅ SAFE: This transaction is predicted to be <b>NOT FRAUDULENT</b>.</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.warning(f"Unexpected response from model: {prediction}")

            else:
                st.error(f"Backend error: {response.status_code}")
                try:
                    st.json(response.json())
                except:
                    st.write(response.text)

        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the backend API. Make sure the FastAPI backend is running.")
        except requests.exceptions.Timeout:
            st.error("The backend took too long to respond.")
        except Exception as e:
            st.error(f"Unexpected error occurred: {str(e)}")