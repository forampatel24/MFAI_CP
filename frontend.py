import streamlit as st
import pandas as pd

from rules import evaluate_rules
from utils import make_decision
from confidence import calculate_confidence
from stability import calculate_stability

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(page_title="AI Decision System", layout="wide")

st.title("🎓 Student Performance Decision System")
st.markdown("Rule-based Explainable AI with Confidence & Stability")

# -----------------------------------
# LOAD DATA
# -----------------------------------
@st.cache_data
def load_data():
    data = pd.read_csv(r"C:\Foram\ENG_SY\SEM2\MFAI\CP\MFAI_CP\data\student-mat.csv", sep=";")

    # -------------------------------
    # DROP IRRELEVANT COLUMNS
    # -------------------------------
    drop_cols = [
        "school", "sex", "address", "famsize", "Pstatus",
        "Mjob", "Fjob", "guardian", "reason"
    ]
    data = data.drop(columns=drop_cols)

    # -------------------------------
    # CLEAN ALL OBJECT COLUMNS FIRST
    # -------------------------------
    for col in data.columns:
        if data[col].dtype == "object":
            data[col] = data[col].astype(str).str.strip().str.lower()

    # -------------------------------
    # CONVERT YES/NO TO 1/0
    # -------------------------------
    binary_cols = [
        "schoolsup", "famsup", "paid", "activities",
        "higher", "internet", "romantic"
    ]

    for col in binary_cols:
        if col in data.columns:
            data[col] = data[col].map({"yes": 1, "no": 0})

   
    data[binary_cols] = data[binary_cols].fillna(0)

    # -------------------------------
    # ATTENDANCE
    # -------------------------------
    data["attendance"] = 100 - data["absences"]
    data = data.drop(columns=["absences"])

    # -------------------------------
    # RENAME
    # -------------------------------
    data = data.rename(columns={
        "G1": "grade1",
        "G2": "grade2",
        "G3": "final_grade"
    })

    # -------------------------------
    # FINAL TYPE SAFETY (CRITICAL)
    # -------------------------------
    data = data.apply(pd.to_numeric, errors='coerce')
    data = data.fillna(0)
    data = data.infer_objects(copy=False)

    return data


data = load_data()

# -----------------------------------
# SHOW DATASET
# -----------------------------------
st.subheader("📊 Dataset View")
st.dataframe(data, width="stretch")

# -----------------------------------
# ROW SELECTION
# -----------------------------------
st.subheader("🔍 Select Student Row")

row_index = st.number_input(
    "Enter Row Index",
    min_value=0,
    max_value=len(data) - 1,
    value=0
)

sample = data.iloc[row_index]

st.write("### Selected Student Data")

st.dataframe(sample.to_frame().T, width="stretch")

# -----------------------------------
# RUN BUTTON
# -----------------------------------
if st.button("🚀 Run Analysis"):

    rules = evaluate_rules(sample)
    decision = make_decision(rules)
    confidence, weights = calculate_confidence(rules, decision)
    stability, unchanged, total, impact = calculate_stability(sample)

    # -----------------------------------
    # OUTPUT
    # -----------------------------------
    st.subheader("📄 AI Decision Report")

    col1, col2, col3 = st.columns(3)

    col1.metric("Decision", decision)
    col2.metric("Confidence", f"{confidence:.2f}%")
    col3.metric("Stability", f"{stability:.2f}%")

    # -----------------------------------
    # RULES
    # -----------------------------------
    st.write("### 📌 Rule Evaluation")

    rule_names = {
        "R1_final_pass": "Final Grade ≥ 10",
        "R2_final_excellent": "Final Grade ≥ 15",
        "R3_mid_term_good": "Mid-Term ≥ 10",
        "R4_first_term_good": "First-Term ≥ 10",
        "R5_improving_trend": "Improving Trend",
        "R6_consistent_performance": "Consistency",
        "R7_low_failures": "Low Failures",
        "R8_high_failures": "High Failures",
        "R9_good_attendance": "Good Attendance",
        "R10_good_studytime": "Study Time ≥ 3",
        "R11_support": "Support Available",
        "R12_low_alcohol": "Low Alcohol",
        "R13_low_social": "Low Social Activity"
    }

    for rule, value in rules.items():
        st.write(f"{rule_names.get(rule, rule)} → {'✔' if value else '✘'}")

    # -----------------------------------
    # INTERPRETATION
    # -----------------------------------
    st.write("### 🧠 Interpretation")

    if stability > 80:
        st.success("Highly Stable Decision")
    elif stability > 60:
        st.warning("Moderately Stable Decision")
    else:
        st.error("Sensitive Decision")

    if confidence > 75:
        st.success("Strong Rule Support")
    elif confidence > 50:
        st.warning("Moderate Support")
    else:
        st.error("Weak Support")

    # -----------------------------------
    # SENSITIVITY
    # -----------------------------------
    st.write("### ⚠️ Sensitivity Analysis")

    for feature, count in impact.items():
        if count > 0:
            st.write(f"{feature} influenced decision {count} times")