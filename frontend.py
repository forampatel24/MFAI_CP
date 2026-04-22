import streamlit as st
import pandas as pd

from rules import extract_facts, get_rules
from utils import make_decision
from confidence import calculate_confidence
from stability import calculate_robustness

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(page_title="Explainable AI System", layout="wide")

st.title("🎓 Student Performance Analysis System")
st.markdown("Explainable AI using Logic, Confidence & Stability")

# -----------------------------------
# LOAD DATA
# -----------------------------------
@st.cache_data
def load_data():
    data = pd.read_csv(
        r"C:\Foram\ENG_SY\SEM2\MFAI\CP\MFAI_CP\data\student-mat.csv",
        sep=";"
    )

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

    return data


data = load_data()

# -----------------------------------
# DATA VIEW
# -----------------------------------
st.subheader("📊 Dataset")
st.dataframe(data, use_container_width=True)

# -----------------------------------
# ROW SELECTION
# -----------------------------------
st.subheader("🔍 Select Student")

row_index = st.number_input(
    "Enter Student Index",
    min_value=0,
    max_value=len(data) - 1,
    value=0
)

sample = data.iloc[row_index]

st.write("### Selected Student Data")
st.dataframe(sample.to_frame().T, use_container_width=True)

# -----------------------------------
# RULE NAME MAPPING
# -----------------------------------
rule_map = {
    "A": "Final Grade ≥ 10 (Pass)",
    "B": "Final Grade ≥ 15 (Excellent)",
    "C": "Mid-Term ≥ 10",
    "D": "First-Term ≥ 10",
    "E": "Improving Performance",
    "F": "Consistent Marks",
    "G": "Low Failures (≤1)",
    "H": "High Failures (>2)",
    "I": "Good Attendance (≥75%)",
    "J": "Study Time ≥ 3",
    "K": "Support Available",
    "L": "Low Alcohol Consumption",
    "M": "Low Social Activity",
    "N": "Very Low Final Grade",
    "O": "Very Low Mid-Term",
    "P": "Poor Attendance",
    "Q": "No Study",
    "R": "High Risk Lifestyle"
}


def translate_rule(expr):
    for key, value in rule_map.items():
        expr = expr.replace(key, value)
    return expr


# -----------------------------------
# RUN ANALYSIS
# -----------------------------------
if st.button("🚀 Run Analysis"):

    facts = extract_facts(sample)
    rules = get_rules()

    decision, triggered, pass_score, fail_score = make_decision(facts, rules)

    confidence, _, _ = calculate_confidence(
        decision,
        pass_score,
        fail_score
    )

    robustness, avg_conf_change, impact = calculate_robustness(sample)

    # -----------------------------------
    # RESULTS
    # -----------------------------------
    st.subheader("📄 AI Decision Report")

    col1, col2, col3 = st.columns(3)

    col1.metric("Decision", decision)
    col2.metric("Confidence", f"{confidence:.2f}%")
    col3.metric("Stability", f"{robustness:.2f}%")

    # -----------------------------------
    # WHY DECISION
    # -----------------------------------
    st.write("### 🧠 Why this decision?")

    if not triggered:
        st.warning("No strong conditions satisfied.")
    else:
        for outcome, expr in triggered:
            readable = translate_rule(expr)

            if outcome == "PASS":
                st.success(f"✔ {readable}")
            else:
                st.error(f"✘ {readable}")

    # -----------------------------------
    # INTERPRETATION
    # -----------------------------------
    st.write("### 📊 Interpretation")

    if decision == "PASS":
        st.success("The student is likely to PASS.")
    else:
        st.error("The student is at risk of FAILING.")

    if confidence > 75:
        st.info("The system is highly confident in this decision.")
    elif confidence > 50:
        st.warning("The decision is moderately certain.")
    else:
        st.error("The decision is uncertain and should be reviewed.")

    # -----------------------------------
    # STABILITY / ROBUSTNESS
    # -----------------------------------
    st.write("### 🔁 Stability of Decision")

    if robustness > 80:
        st.success("The decision is very stable. Small changes will not affect it.")
    elif robustness > 60:
        st.warning("The decision is somewhat stable but may change.")
    else:
        st.error("The decision is unstable and sensitive to changes.")

    st.write(f"Average confidence variation during testing: {avg_conf_change:.2f}")

    # -----------------------------------
    # FEATURE IMPACT
    # -----------------------------------
    st.write("### ⚠️ What influenced this decision?")

    important = {k: v for k, v in impact.items() if v > 0}

    if not important:
        st.write("No specific feature had strong impact.")
    else:
        for feature, count in important.items():
            st.write(f"• {feature} influenced decision ({count} times)")

    # -----------------------------------
    # SUGGESTION
    # -----------------------------------
    st.write("### 💡 Suggestion")

    if decision == "FAIL":
        st.write("Improving attendance, reducing failures, and increasing study time can improve results.")
    else:
        st.write("Maintain current performance and consistency to sustain success.")