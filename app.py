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

    rule_explanations = {

        # PASS RULES
        "A AND I AND G": "Student has good final grade, good attendance, and low failures",
        "B AND I": "Student has excellent final grade and strong attendance",
        "A AND C AND D": "Student performed well across all exams",
        "A AND E AND F": "Student is improving and consistent",
        "A AND J AND I": "Student studies well and maintains good attendance",
        "A AND K AND G": "Student has support and low failures",
        "A AND X AND Y": "Student has average attendance and moderate study effort",
        "A AND G AND X": "Student has low failures and acceptable attendance",
        "A AND C AND I": "Student has strong mid-term and attendance",
        "A AND D AND G": "Student has good base and low failures",
        "A AND L AND M": "Student maintains a healthy lifestyle",
        "A AND F AND I": "Student is consistent and attends regularly",

        # FAIL RULES
        "H": "Student has too many failures",
        "N": "Final grade is critically low",
        "P AND H": "Poor attendance combined with failures",
        "Q AND N": "No study effort and very low performance",
        "R": "Risky lifestyle affecting performance",
        "NOT A AND O": "Weak overall academic performance",
        "NOT I AND H": "Low attendance and high failures",
        "NOT J AND N": "Low study effort and very low final grade",
        "P AND Q": "Poor attendance and no study",
        "O AND NOT D": "Weak mid-term and weak base",
        "P AND Y": "Low attendance despite moderate study",
        "Z AND NOT J": "Moderate failures and insufficient study"
    }


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

        # -----------------------------------
        # WHY DECISION (CLEAN + DEDUPLICATED)
        # -----------------------------------
        st.write("### 🧠 Why this decision?")

        pass_explanations = set()
        fail_explanations = set()

        for outcome, expr in triggered:

            explanation = rule_explanations.get(expr, expr)

            if outcome == "PASS":
                pass_explanations.add(explanation)
            else:
                fail_explanations.add(explanation)



        # PASS SECTION
        # PASS
        if pass_explanations:
            st.markdown("#### ✅ Conditions Supporting PASS")
            for e in pass_explanations:
                st.markdown(f"- {e}")

        # FAIL
        if fail_explanations:
            st.markdown("#### ❌ Conditions Supporting FAIL")
            for e in fail_explanations:
                st.markdown(f"- {e}")

        if not pass_explanations and not fail_explanations:
            st.warning("No strong rules were triggered for this student.")

        # -----------------------------------
        # SUGGESTION
        # -----------------------------------
        st.write("### 💡 Suggestion")

        if decision == "FAIL":
            st.write("Improving attendance, reducing failures, and increasing study time can improve results.")
        else:
            st.write("Maintain current performance and consistency to sustain success.")

        # -----------------------------------
        # EVIDENCE
        # -----------------------------------
        st.write("### 📊 Evidence Summary")
        st.write(f"PASS Score: {pass_score:.2f}")
        st.write(f"FAIL Score: {fail_score:.2f}")

        st.write("### 📉 Confidence Sensitivity")

        if avg_conf_change < 5:
            st.success(f"Very stable confidence ({avg_conf_change:.2f}%)")
        elif avg_conf_change < 15:
            st.warning(f"Moderate sensitivity ({avg_conf_change:.2f}%)")
        else:
            st.error(f"High sensitivity ({avg_conf_change:.2f}%)")

        # -----------------------------------
        # FEATURE IMPACT (STABILITY)
        # -----------------------------------
        st.write("### ⚠️ What affected the decision during stability testing?")

        important = {k: v for k, v in impact.items() if v > 0}

        if not important:
            st.write("No feature significantly affected the decision.")
        else:
            for feature, count in sorted(important.items(), key=lambda x: -x[1]):
                st.write(f"• {feature} influenced the decision {count} times")


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