import pandas as pd

from rules import extract_facts, get_rules
from utils import make_decision
from confidence import calculate_confidence
from stability import calculate_robustness


# -------------------------------
# RULE EXPLANATIONS
# -------------------------------
rule_explanations = {

    # PASS RULES
    "A AND I AND G": "Good final grade, attendance, and low failures",
    "B AND I": "Excellent final grade and strong attendance",
    "A AND C AND D": "Strong performance across all exams",
    "A AND E AND F": "Improving and consistent performance",
    "A AND J AND I": "Good study effort and attendance",
    "A AND K AND G": "Support system with low failures",
    "A AND X AND Y": "Average attendance and moderate study",
    "A AND G AND X": "Low failures with moderate attendance",
    "A AND C AND I": "Strong mid-term and attendance",
    "A AND D AND G": "Good base and low failures",
    "A AND L AND M": "Healthy lifestyle maintained",
    "A AND F AND I": "Consistent performance with attendance",

    # FAIL RULES
    "H": "Too many failures",
    "N": "Final grade is critically low",
    "P AND H": "Poor attendance and failures",
    "Q AND N": "No study and very low performance",
    "R": "Risky lifestyle",
    "NOT A AND O": "Weak academic performance overall",
    "NOT I AND H": "Low attendance and high failures",
    "NOT J AND N": "Low study effort and low final grade",
    "P AND Q": "Poor attendance and no study",
    "O AND NOT D": "Weak mid-term and weak base",
    "P AND Y": "Low attendance despite moderate study",
    "Z AND NOT J": "Failures with insufficient study"
}


# -------------------------------
# LOAD & CLEAN DATA
# -------------------------------
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

    binary_cols = [
        "schoolsup", "famsup", "paid", "activities",
        "higher", "internet", "romantic"
    ]

    for col in binary_cols:
        data[col] = data[col].map({"yes": 1, "no": 0})

    data["attendance"] = 100 - data["absences"]
    data = data.drop(columns=["absences"])

    data = data.rename(columns={
        "G1": "grade1",
        "G2": "grade2",
        "G3": "final_grade"
    })

    return data


# -------------------------------
# ANALYSIS FUNCTION
# -------------------------------
def analyze_student(sample):

    facts = extract_facts(sample)
    rules = get_rules()

    decision, triggered, pass_score, fail_score = make_decision(facts, rules)

    confidence, p_pass, p_fail = calculate_confidence(
        decision, pass_score, fail_score
    )

    robustness, avg_conf_change, impact = calculate_robustness(sample)

    print("\n================ AI DECISION REPORT ================\n")

    print("📥 INPUT SUMMARY")
    print("--------------------------------------------------")
    print(f"Grade 1     : {sample['grade1']}")
    print(f"Grade 2     : {sample['grade2']}")
    print(f"Final Grade : {sample['final_grade']}")
    print(f"Attendance  : {sample['attendance']}%")
    print(f"Failures    : {sample['failures']}")
    print("--------------------------------------------------")

    print("\n📌 TRIGGERED RULES")
    print("--------------------------------------------------")

    if not triggered:
        print("No rules triggered")
    else:
        for outcome, expr in triggered:
            explanation = rule_explanations.get(expr, expr)
            print(f"{outcome} → {explanation}")

    print("\n📊 SCORES")
    print("--------------------------------------------------")
    print(f"PASS Score : {pass_score:.2f}")
    print(f"FAIL Score : {fail_score:.2f}")

    print("\n🎯 FINAL RESULT")
    print("--------------------------------------------------")
    print(f"Decision     : {decision}")
    print(f"Confidence   : {confidence:.2f}%")
    print(f"P(PASS)      : {p_pass:.2f}%")
    print(f"P(FAIL)      : {p_fail:.2f}%")
    print(f"Stability    : {robustness:.2f}%")

    print("\n📉 INTERPRETATION")

    if robustness > 80:
        print("• Highly stable decision")
    elif robustness > 60:
        print("• Moderately stable decision")
    else:
        print("• Sensitive decision")

    print(f"• Avg Confidence Change: {avg_conf_change:.2f}%")

    print("\n⚠️ FEATURE IMPACT")

    important = {k: v for k, v in impact.items() if v > 0}

    if not important:
        print("• No feature significantly affected decision")
    else:
        for feature, count in sorted(important.items(), key=lambda x: -x[1]):
            print(f"• {feature} → {count} times")


# -------------------------------
# MAIN LOOP (CLI)
# -------------------------------
def main():
    data = load_data()

    print("\n✅ Dataset Loaded!")
    print(f"Total Students: {len(data)}")

    while True:
        print("\n----------------------------------")
        user_input = input(
            "Enter student index (0 to {}), or 'q' to quit: ".format(len(data) - 1)
        )

        if user_input.lower() == 'q':
            print("👋 Exiting...")
            break

        if not user_input.isdigit():
            print("❌ Invalid input. Enter a number.")
            continue

        index = int(user_input)

        if index < 0 or index >= len(data):
            print("❌ Index out of range.")
            continue

        sample = data.iloc[index]
        analyze_student(sample)


# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":
    main()