import streamlit as st
import pandas as pd

from rules import extract_facts, get_rules
from utils import make_decision
from confidence import calculate_confidence
from stability import calculate_robustness

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(page_title="Bulk Student Analysis", layout="wide")

st.title("📊 Bulk Student Performance Analysis System")
st.markdown("Upload a dataset to analyze all students using Explainable AI")

# -----------------------------------
# FILE UPLOAD
# -----------------------------------
uploaded_file = st.file_uploader("📁 Upload Student CSV File", type=["csv"])

# -----------------------------------
# PROCESS FILE
# -----------------------------------
if uploaded_file is not None:

    data = pd.read_csv(uploaded_file, sep=";")

    # -----------------------------------
    # CLEANING (same as original)
    # -----------------------------------
    drop_cols = [
        "school", "sex", "address", "famsize", "Pstatus",
        "Mjob", "Fjob", "guardian", "reason"
    ]
    data = data.drop(columns=drop_cols)

    for col in data.columns:
        if data[col].dtype == "object":
            data[col] = data[col].astype(str).str.strip().str.lower()

    binary_cols = [
        "schoolsup", "famsup", "paid", "activities",
        "higher", "internet", "romantic"
    ]

    for col in binary_cols:
        data[col] = data[col].map({"yes": 1, "no": 0})

    data[binary_cols] = data[binary_cols].fillna(0)

    data["attendance"] = 100 - data["absences"]
    data = data.drop(columns=["absences"])

    data = data.rename(columns={
        "G1": "grade1",
        "G2": "grade2",
        "G3": "final_grade"
    })

    data = data.apply(pd.to_numeric, errors='coerce')
    data = data.fillna(0)

    st.success("✅ File loaded and cleaned successfully!")

    # -----------------------------------
    # RUN ANALYSIS
    # -----------------------------------
    if st.button("🚀 Analyze All Students"):

        rules = get_rules()
        results = []

        progress = st.progress(0)

        for i, row in data.iterrows():

            facts = extract_facts(row)

            decision, _, pass_score, fail_score = make_decision(facts, rules)

            confidence, _, _ = calculate_confidence(
                decision,
                pass_score,
                fail_score
            )

            robustness, _, _ = calculate_robustness(row, iterations=30)

            results.append({
                "Student_ID": i,
                "Final_Result": decision,
                "Confidence (%)": round(confidence, 2),
                "Stability (%)": round(robustness, 2),


                "Grade1": row["grade1"],
                "Grade2": row["grade2"],
                "Final_Grade": row["final_grade"],
                "Attendance (%)": row["attendance"],
                "Failures": row["failures"]
            })

            progress.progress((i + 1) / len(data))

        results_df = pd.DataFrame(results)

        # -----------------------------------
        # SUMMARY DASHBOARD
        # -----------------------------------
        st.subheader("📈 Summary Overview")

        col1, col2, col3 = st.columns(3)

        total = len(results_df)
        pass_count = (results_df["Final_Result"] == "PASS").sum()
        fail_count = (results_df["Final_Result"] == "FAIL").sum()

        col1.metric("Total Students", total)
        col2.metric("Passed", pass_count)
        col3.metric("Failed", fail_count)

        # -----------------------------------
        # VISUALIZATION
        # -----------------------------------
        st.subheader("📊 Performance Distribution")
        st.bar_chart(results_df["Final_Result"].value_counts())

        # -----------------------------------
        # FILTERS
        # -----------------------------------
        st.subheader("🔍 Filter Results")

        filter_option = st.selectbox(
            "Select Category",
            ["All", "PASS", "FAIL", "Low Confidence (<60%)"]
        )

        filtered_df = results_df.copy()

        if filter_option == "PASS":
            filtered_df = results_df[results_df["Final_Result"] == "PASS"]

        elif filter_option == "FAIL":
            filtered_df = results_df[results_df["Final_Result"] == "FAIL"]

        elif filter_option == "Low Confidence (<60%)":
            filtered_df = results_df[results_df["Confidence (%)"] < 60]

        # -----------------------------------
        # DISPLAY TABLE
        # -----------------------------------
        st.subheader("📋 Detailed Results")
        st.dataframe(filtered_df, use_container_width=True)

        # -----------------------------------
        # HIGH RISK STUDENTS
        # -----------------------------------
        st.subheader("⚠️ Students Needing Attention")

        risky = results_df[
            (results_df["Final_Result"] == "FAIL") |
            (results_df["Confidence (%)"] < 60)
        ]

        if len(risky) > 0:

            display_cols = [
                "Student_ID",
                "Final_Result",
                "Confidence (%)",
                "Grade1",
                "Grade2",
                "Final_Grade",
                "Attendance (%)",
                "Failures"
            ]

            st.dataframe(risky[display_cols], use_container_width=True)

        else:
            st.success("No high-risk students identified")

        # -----------------------------------
        # DOWNLOAD RESULTS
        # -----------------------------------
        st.subheader("⬇️ Download Results")

        csv = results_df.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="student_analysis_results.csv",
            mime="text/csv"
        )