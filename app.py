import streamlit as st
import pandas as pd

from rules import extract_facts, get_rules
from utils import make_decision
from confidence import calculate_confidence
from stability import calculate_robustness

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(page_title="Student Analysis System", layout="wide")

st.title("🎓 Student Performance Analysis")
st.caption("Explainable AI using Logic, Confidence & Stability")

# -----------------------------------
# MODE SELECTOR
# -----------------------------------
st.sidebar.title("⚙️ Settings")

mode = st.sidebar.radio(
    "Select Analysis Mode",
    ["Single Student", "Bulk Analysis"]
)
st.sidebar.markdown("---")
st.sidebar.info(
    "Use this tool to analyze student performance.\n\n"
    "• Single Student → Detailed explanation\n"
    "• Bulk Analysis → Entire dataset insights"
)

# =========================================================
# ================= SINGLE STUDENT MODE ====================
# =========================================================
if mode == "Single Student":

    st.markdown("Explainable AI using Logic, Confidence & Stability")

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

    st.subheader("📊 Dataset")
    st.dataframe(data, use_container_width=True)

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

        st.subheader("📄 AI Decision Report")

        col1, col2, col3 = st.columns(3)

        col1.metric("Decision", decision)
        col2.metric("Confidence", f"{confidence:.2f}%")
        col3.metric("Stability", f"{robustness:.2f}%")

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

        st.write("### 🔁 Stability of Decision")

        if robustness > 80:
            st.success("The decision is very stable. Small changes will not affect it.")
        elif robustness > 60:
            st.warning("The decision is somewhat stable but may change.")
        else:
            st.error("The decision is unstable and sensitive to changes.")

        st.write(f"Average confidence variation during testing: {avg_conf_change:.2f}")

        st.write("### ⚠️ What influenced this decision?")

        important = {k: v for k, v in impact.items() if v > 0}

        if not important:
            st.write("No specific feature had strong impact.")
        else:
            for feature, count in important.items():
                st.write(f"• {feature} influenced decision ({count} times)")

        st.write("### 💡 Suggestion")

        if decision == "FAIL":
            st.write("Improving attendance, reducing failures, and increasing study time can improve results.")
        else:
            st.write("Maintain current performance and consistency to sustain success.")


# =========================================================
# ================= BULK MODE ==============================
# =========================================================
else:

    st.markdown("Upload a dataset to analyze all students")

    uploaded_file = st.file_uploader("📁 Upload Student CSV File", type=["csv"])

    if uploaded_file is not None:

        data = pd.read_csv(uploaded_file, sep=";")

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

        st.success("✅ File loaded successfully!")

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