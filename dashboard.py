import streamlit as st
import sqlite3
import pandas as pd
import pickle
import uuid
import matplotlib.pyplot as plt

conn = sqlite3.connect("hospital.db", check_same_thread=False)
cursor = conn.cursor()

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

def get_bed_stats():
    total = cursor.execute("SELECT COUNT(*) FROM beds").fetchone()[0]
    allocated = cursor.execute("SELECT COUNT(*) FROM patients WHERE discharged = 0").fetchone()[0]
    available = total - allocated
    return total, allocated, available

def predict_stay(input_data):
    df = pd.DataFrame([input_data])
    return round(model.predict(df)[0], 1)

def admit_patient(data):
    predicted_stay = predict_stay({
        "age": data["age"],
        "acuity_score": data["acuity_score"],
        "needs_icu": int(data["needs_icu"]),
        "needs_isolation": int(data["needs_isolation"]),
        "needs_ventilator": int(data["needs_ventilator"])
    })

    cursor.execute("""
        INSERT INTO patients (patient_id, name, age, gender, acuity_score, diagnosis, department,
        needs_icu, needs_isolation, needs_ventilator, predicted_stay, discharged)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
    """, (
        data["patient_id"], data["name"], data["age"], data["gender"], data["acuity_score"],
        data["diagnosis"], data["department"], int(data["needs_icu"]),
        int(data["needs_isolation"]), int(data["needs_ventilator"]), predicted_stay
    ))

    conn.commit()
    return predicted_stay

def discharge_patient(pid):
    cursor.execute("UPDATE patients SET discharged = 1 WHERE patient_id = ?", (pid,))
    conn.commit()

def show_dashboard():
    st.title("Hospital Bed Management Dashboard")

    total, allocated, available = get_bed_stats()
    st.metric("Total Beds", total)
    st.metric("Allocated Beds", allocated)
    st.metric("Available Beds", available)

    st.header("Admit New Patient")

    name = st.text_input("Name")
    age = st.number_input("Age", 0, 120)
    gender = st.selectbox("Gender", ["Male", "Female"])
    acuity = st.slider("Acuity Score", 1, 10)
    diagnosis = st.selectbox("Diagnosis", [
        "Pneumonia", "Cardiac Arrest", "Fracture", "COVID-19",
        "Stroke", "Infection", "Cancer", "Other"])
    department = st.selectbox("Department", [
        "Emergency", "Cardiology", "Orthopedics", "ICU",
        "Oncology", "General Medicine", "Pulmonology"])
    needs_icu = st.checkbox("Needs ICU")
    needs_isolation = st.checkbox("Needs Isolation")
    needs_ventilator = st.checkbox("Needs Ventilator")

    if st.button("Admit Patient"):
        pid = str(uuid.uuid4())[:8]
        stay = admit_patient({
            "patient_id": pid,
            "name": name,
            "age": age,
            "gender": gender,
            "acuity_score": acuity,
            "diagnosis": diagnosis,
            "department": department,
            "needs_icu": needs_icu,
            "needs_isolation": needs_isolation,
            "needs_ventilator": needs_ventilator
        })
        st.success(f"Patient admitted. Predicted stay: {stay} days")

    st.header("Discharge Patient")
    patients = cursor.execute("SELECT patient_id, name FROM patients WHERE discharged = 0").fetchall()
    if patients:
        patient_map = {f"{name} ({pid})": pid for pid, name in patients}
        selected = st.selectbox("Select patient to discharge", list(patient_map.keys()))
        if st.button("Discharge"):
            discharge_patient(patient_map[selected])
            st.success("Patient discharged successfully")

    st.header("Visualizations")
    df = pd.read_sql("SELECT * FROM patients WHERE discharged = 0", conn)
    if not df.empty:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Patients by Department")
            dept_counts = df["department"].value_counts()
            st.bar_chart(dept_counts)

        with col2:
            st.subheader("Patients by Diagnosis")
            diag_counts = df["diagnosis"].value_counts()
            st.bar_chart(diag_counts)

if __name__ == "__main__":
    show_dashboard()
