🏥 Hospital Bed Management Dashboard

Made with ❤️ by Nipun Singh

See here - https://hospital-bed-management-dashboard.streamlit.app/

This project is an end-to-end **Machine Learning-powered Hospital Bed Management System** that predicts patient stay durations, dynamically allocates hospital beds, and visualizes critical statistics via an interactive Streamlit dashboard.

🚀 Features

- 📊 **ML Prediction** of patient stay using real hospital data.
- 🛏️ **Dynamic Bed Allocation** based on real-time admissions.
- ✅ **Patient Admission & Discharge System**
- 📈 **Visual Analytics**: ICU/Isolation/Ventilator needs, utilization rate, department distribution, and more.
- 🔍 **Filter & Track** patients based on diagnosis, department, and resource needs.
- 🧠 **Trained ML Model** (Linear Regression) included.
- 🗃️ **SQLite Database Integration** for persistence.
- 📦 **Deploy-ready** using Streamlit Cloud or any other platform.

📂 Files

- `dashboard.py` – Main Streamlit app
- `model.pkl` – Trained ML model for stay prediction
- `hospital.db` – SQLite database for patient & bed data
- `hospital_data.csv` – Sample data used for model training and simulation
- `requirements.txt` – Python package dependencies

🛠️ Tech Stack

- Python, Streamlit
- SQLite
- Pandas, NumPy, Scikit-learn
- Matplotlib (for graphs)

🧠 Machine Learning

- Model: **Linear Regression**
- Trained on real/simulated hospital data
- Predicts: `length_of_stay_days` based on:
  - Age
  - Acuity Score
  - Diagnosis
  - Department
  - Resource needs (ICU, Ventilator, Isolation)

🌐 Deployment

Easily deploy to [Streamlit Cloud](https://streamlit.io/cloud) or run locally:
```bash
streamlit run dashboard.py

