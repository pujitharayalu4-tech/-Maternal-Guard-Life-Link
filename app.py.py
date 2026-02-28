import streamlit as st
import pandas as pd
import os
import joblib
import smtplib
from email.mime.text import MIMEText

# Page config
st.set_page_config(page_title="Maternal-Guard & Life-Link", layout="centered")

st.title("🩺 Maternal-Guard & 🩸 Life-Link")
st.write("AI-driven maternal care & emergency donor network")

# Load ML model
model = joblib.load("model.pkl")

# Risk prediction
def predict_risk(age, systolic_bp, diastolic_bp, heart_rate, oxygen_level, temperature):
    result = model.predict([[age, systolic_bp, diastolic_bp, heart_rate, oxygen_level, temperature]])[0]
    mapping = {0: "Low Risk", 1: "Mid Risk", 2: "High Risk"}
    return mapping[result]

# SOS notification (email demo)
def send_sos_notification(patient_name, risk_level):
    sender = "ambatimeghana774@gmail.com"
    recipient = "pujitharayalu4@gmail.com"
    subject = "🚨 SOS Alert - Maternal Risk Detected"
    body = f"Patient {patient_name} is {risk_level}. Immediate attention required."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("your_email@example.com", "your_password")  # replace securely
            server.sendmail(sender, [recipient], msg.as_string())
        return True
    except Exception as e:
        st.error(f"Failed to send SOS notification: {e}")
        return False

# ---------------- Maternal Risk Assessment ----------------
st.header("Maternal Risk Assessment")

with st.form("risk_form"):
    patient_name = st.text_input("Patient Name")
    age = st.number_input("Age", min_value=15, max_value=50)
    systolic_bp = st.number_input("Systolic BP (mmHg)", min_value=80, max_value=200)
    diastolic_bp = st.number_input("Diastolic BP (mmHg)", min_value=50, max_value=130)
    heart_rate = st.number_input("Heart Rate (bpm)", min_value=40, max_value=180)
    oxygen_level = st.number_input("Oxygen Level (%)", min_value=70, max_value=100)
    temperature = st.number_input("Temperature (°C)", min_value=35.0, max_value=42.0, step=0.1)

    predict_button = st.form_submit_button("Predict Risk")

if predict_button:
    result = predict_risk(age, systolic_bp, diastolic_bp, heart_rate, oxygen_level, temperature)
    st.subheader(f"🩺 Risk Level: {result}")

    if result == "High Risk":
        st.error("⚠ High Risk Detected — SOS Required")
        if st.button("🚨 Send SOS Notification"):
            if send_sos_notification(patient_name, result):
                st.success("✅ SOS notification sent successfully!")

# ---------------- Donor Registration ----------------
st.header("Add Donor Manually")

with st.form("donor_form"):
    donor_id = st.number_input("Donor ID", min_value=1)
    donor_age = st.number_input("Donor Age", min_value=18, max_value=65)
    gender = st.selectbox("Gender", ["Male", "Female"])
    blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
    city = st.text_input("City")
    eligible = st.selectbox("Eligible to Donate?", ["Yes", "No"])

    save_donor = st.form_submit_button("Save Donor")

if save_donor:
    donor_data = {
        "Donor_ID": donor_id,
        "Age": donor_age,
        "Gender": gender,
        "Blood_Group": blood_group,
        "City": city,
        "Eligible": eligible
    }
    df = pd.DataFrame([donor_data])
    if os.path.exists("donors.csv"):
        df.to_csv("donors.csv", mode="a", header=False, index=False)
    else:
        df.to_csv("donors.csv", index=False)
    st.success("✅ Donor saved successfully!")

# ---------------- Donor Listing ----------------
st.header("Registered Donors")
if os.path.exists("donors.csv"):
    donors_df = pd.read_csv("donors.csv")
    st.dataframe(donors_df)
else:
    st.info("No donors registered yet.")

# ---------------- Donor Matching ----------------
st.header("Donor Matching System")
if os.path.exists("donors.csv"):
    patient_blood_group = st.selectbox("Patient Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
    patient_city = st.text_input("Patient City")

    if st.button("Find Matching Donors"):
        donors_df = pd.read_csv("donors.csv")
        matches = donors_df[
            (donors_df["Blood_Group"] == patient_blood_group) &
            (donors_df["City"].str.lower() == patient_city.lower()) &
            (donors_df["Eligible"] == "Yes")
        ]
        if not matches.empty:
            st.success("✅ Matching donors found:")
            st.dataframe(matches)
        else:
            st.warning("No matching donors available.")
