import streamlit as st
import sqlite3
import pandas as pd
import re
from datetime import date
from model import predict_health

# Database Connection
conn = sqlite3.connect("patient.db", check_same_thread=False)
cursor = conn.cursor()

st.set_page_config(
    page_title="Health Prediction Application",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Health Prediction Application")
st.write("AI/ML Based Health Risk Assessment System")

# ================= ADD PATIENT =================

st.subheader("➕ Add Patient")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Full Name")

    dob = st.date_input(
        "Date of Birth",
        value=date(2003, 1, 1),
        min_value=date(1950, 1, 1),
        max_value=date.today()
    )

    email = st.text_input("Email Address")

with col2:
    glucose = st.number_input(
        "Glucose",
        min_value=0.0,
        value=100.0
    )

    haemoglobin = st.number_input(
        "Haemoglobin",
        min_value=0.0,
        value=13.0
    )

    cholesterol = st.number_input(
        "Cholesterol",
        min_value=0.0,
        value=180.0
    )

if st.button("Predict & Save"):

    if not name.strip():
        st.error("Name is required")

    elif not re.match(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
        email
    ):
        st.error("Please enter a valid email address")

    else:

        remarks = predict_health(
            glucose,
            haemoglobin,
            cholesterol
        )

        cursor.execute("""
        INSERT INTO patients
        (
            name,
            dob,
            email,
            glucose,
            haemoglobin,
            cholesterol,
            remarks
        )
        VALUES (?,?,?,?,?,?,?)
        """,
        (
            name,
            str(dob),
            email,
            glucose,
            haemoglobin,
            cholesterol,
            remarks
        ))

        conn.commit()

        st.success("Patient Saved Successfully")
        st.info(f"Prediction Result: {remarks}")

# ================= VIEW RECORDS =================

st.subheader("📋 Patient Records")

df = pd.read_sql_query(
    "SELECT * FROM patients",
    conn
)

st.dataframe(
    df,
    use_container_width=True
)

# ================= SEARCH =================

st.subheader("🔍 Search Patient")

search_name = st.text_input(
    "Search Patient by Name"
)

if search_name:

    filtered_df = df[
        df["name"].astype(str).str.contains(
            search_name,
            case=False,
            na=False
        )
    ]

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# ================= UPDATE =================

st.subheader("✏️ Update Remarks")

update_id = st.number_input(
    "Patient ID",
    min_value=1,
    step=1
)

new_remarks = st.text_area(
    "New Remarks"
)

if st.button("Update Record"):

    cursor.execute(
        """
        UPDATE patients
        SET remarks=?
        WHERE id=?
        """,
        (new_remarks, update_id)
    )

    conn.commit()

    st.success("Record Updated Successfully")
    st.rerun()

# ================= DELETE =================

st.subheader("🗑️ Delete Record")

delete_id = st.number_input(
    "Delete Patient ID",
    min_value=1,
    step=1,
    key="delete"
)

if st.button("Delete Record"):

    cursor.execute(
        """
        DELETE FROM patients
        WHERE id=?
        """,
        (delete_id,)
    )

    conn.commit()

    st.success("Record Deleted Successfully")
    st.rerun()

# ================= EXPORT =================

st.subheader("📥 Export Records")

csv = df.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="patients.csv",
    mime="text/csv"
)

# ================= ANALYTICS =================

if not df.empty:

    st.subheader("📊 Health Analytics")

    chart_df = pd.DataFrame({
        "Metric": [
            "Average Glucose",
            "Average Haemoglobin",
            "Average Cholesterol"
        ],
        "Value": [
            df["glucose"].mean(),
            df["haemoglobin"].mean(),
            df["cholesterol"].mean()
        ]
    })

    st.bar_chart(
        chart_df.set_index("Metric")
    )