import streamlit as st
import json
import requests as re

st.set_page_config(page_title="Fraud Detection", page_icon="💳", layout="centered")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">

<style>

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3 {
    font-family: 'Montserrat', sans-serif !important;
    color: #38bdf8 !important;
}

.stApp {
    background: linear-gradient(135deg, #14213d, #6930c3);
    color: #e2e8f0;
}

input, .stNumberInput input {
    background-color: #1e293b !important;
    color: white !important;
    border-radius: 10px !important;
    border: 1px solid #334155;
}

.stButton > button {
    background: linear-gradient(90deg, #c9184a, #ef233c);
    color: black;
    font-weight: 600;
    font-family: 'Poppins', sans-serif;
    border-radius: 12px;
    padding: 10px;
}

.stAlert {
    border-radius: 14px !important;
    padding: 15px !important;
}

div[data-testid="stExpander"] {
    background-color: #1e293b;
    border-radius: 12px;
    border: 1px solid #334155;
}

div[data-testid="stExpander"] summary {
    font-size: 18px;
    font-weight: 600;
    color: #38bdf8;
}

div[data-testid="stExpander"] summary:hover {
    color: #fb6f92;
}

div[data-testid="stExpander"] div[role="region"] {
    padding: 15px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='text-align: center;'> Fraud Transaction Detection</h1>
""", unsafe_allow_html=True)
st.markdown("""<div style=
            'color: #98c1d9;background-color: #001524; border: 2px solid #0077b6; border-radius: 12px; padding: 15px;' >
            <h2 style='text-align: left;'>How it works</h2>
 The Architecture of this project is divided into 3 parts:<br>
            - <strong>Frontend:</strong> The User inputs Transaction details. Written in Streamlit.<br>
            - <strong>Backend:</strong> Processes data and handles requests.<br>
            - <strong>ML model:</strong> Pridicts Fraud based on input features.
<br>
            <br>
            The model is served via FastAPI to detect fraudulent transactions.<br>
            It analyzes:<br>
            - Transaction Time<br>
            - Transaction Type<br>
            - Amount<br>
            - Account Balances
            </div>
""", unsafe_allow_html=True)
st.write("")

with st.expander("Architecture Diagram"):
    st.image("Architecture.png", use_container_width=True)   

st.markdown("## Enter Transaction Details")

col1, col2 = st.columns(2)

with col1:
    sender_name = st.text_input("Sender ID")
    step = st.slider("Transaction Time (hours)", 0, 100)

    types = st.selectbox(
        "Transaction Type",
        (0, 1, 2, 3, 4),
        format_func=lambda x: ["Cash In", "Cash Out", "Debit", "Payment", "Transfer"][x]
    )

    amount = st.number_input("Amount ($)", min_value=0, max_value=110000)

with col2:
    receiver_name = st.text_input("Receiver ID")

    oldbalanceorg = st.number_input("Sender Balance Before", min_value=0, max_value=110000)
    newbalanceorg = st.number_input("Sender Balance After", min_value=0, max_value=110000)

    oldbalancedest = st.number_input("Receiver Balance Before", min_value=0, max_value=110000)
    newbalancedest = st.number_input("Receiver Balance After", min_value=0, max_value=110000)

type_map = {
    0: "Cash In",
    1: "Cash Out",
    2: "Debit",
    3: "Payment",
    4: "Transfer"
}
x = type_map[types]

isflaggedfraud = 1 if amount >= 200000 else 0

if st.button(" Run Detection"):

    if sender_name == '' or receiver_name == '':
        st.error(" Please enter Sender and Receiver IDs")

    else:
        values = {
            "step": step,
            "types": types,
            "amount": amount,
            "oldbalanceorig": oldbalanceorg,
            "newbalanceorig": newbalanceorg,
            "oldbalancedest": oldbalancedest,
            "newbalancedest": newbalancedest,
            "isflaggedfraud": isflaggedfraud
        }

        st.markdown("## Transaction Summary")

        st.info(f"""
        **Sender:** {sender_name}  
        **Receiver:** {receiver_name}  

        - Time: {step} hours  
        - Type: {x}  
        - Amount: ${amount}  

        **Balances:**
        - Sender Before: ${oldbalanceorg} → After: ${newbalanceorg}  
        - Receiver Before: ${oldbalancedest} → After: ${newbalancedest}  

        **System Flag:** {isflaggedfraud}
        """)

        try:
            res = re.post("http://localhost:8001/predict", json=values)
            resp = res.json()

            result = resp[0].lower()

            st.markdown("## Detection Result")

            if result == "fraudulent":
                st.markdown("""
                <div style='padding:20px; border-radius:14px; background:#7f1d1d; color:white; text-align:center; font-family:Poppins;'>
                    <h2> FRAUD DETECTED</h2>
                </div>
                """, unsafe_allow_html=True)

            elif result == "not fraudulent":
                st.markdown("""
                <div style='padding:20px; border-radius:14px; background:#14532d; color:white; text-align:center; font-family:Poppins;'>
                    <h2> SAFE TRANSACTION</h2>
                </div>
                """, unsafe_allow_html=True)

            else:
                st.warning(f"Unexpected result: {result}")

        except Exception as e:
            st.error(f" API Error: {e}")
