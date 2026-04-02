import pandas as pd
from rules import evaluate_rules
from utils import make_decision
from confidence import calculate_confidence
from stability import calculate_stability

# Load dataset (FIXED PATH WARNING)
data = pd.read_csv(r"C:\Foram\ENG_SY\SEM2\MFAI\CP\MFAI_CP\data\student-mat.csv", sep=";")

print("\nDataset Loaded Successfully!\n")

# -------------------------------
# REMOVE PERSONAL / IRRELEVANT COLUMNS
# -------------------------------
drop_cols = [
    "school", "sex", "address", "famsize", "Pstatus",
    "Mjob", "Fjob", "guardian", "reason"
]

data = data.drop(columns=drop_cols)

# -------------------------------
# CONVERT YES/NO TO 1/0
# -------------------------------
binary_cols = [
    "schoolsup", "famsup", "paid", "activities",
    "higher", "internet", "romantic"
]

for col in binary_cols:
    data[col] = data[col].map({"yes": 1, "no": 0})

# -------------------------------
# CONVERT ABSENCES → ATTENDANCE
# -------------------------------
data["attendance"] = 100 - data["absences"]
data = data.drop(columns=["absences"])

# -------------------------------
# RENAME GRADES FOR CLARITY
# -------------------------------
data = data.rename(columns={
    "G1": "grade1",
    "G2": "grade2",
    "G3": "final_grade"
})

# -------------------------------
# SHOW CLEAN DATA
# -------------------------------
print("\nCleaned Dataset:\n")
print(data.head())

# -----------------------------------
# APPLY RULES TO ONE SAMPLE ROW
# -----------------------------------

sample = data.iloc[350]

rules = evaluate_rules(sample)
decision = make_decision(rules)
confidence, weights = calculate_confidence(rules, decision)
stability, unchanged, total, impact = calculate_stability(sample)

# -----------------------------------
# CLEAN FORMATTED OUTPUT (REPORT STYLE)
# -----------------------------------

print("\n================ AI DECISION REPORT ================\n")

# INPUT SUMMARY
print("INPUT SUMMARY:")
print("--------------------------------------------------")
print(f"Grade 1 (G1)      : {sample['grade1']}")
print(f"Grade 2 (G2)      : {sample['grade2']}")
print(f"Final Grade (G3)  : {sample['final_grade']}")
print(f"Attendance        : {sample['attendance']}%")
print(f"Failures          : {sample['failures']}")
print("--------------------------------------------------")

# RULE EXPLANATION
print("\nRULE EVALUATION:")
print("--------------------------------------------------")

rule_names = {
    "R1_final_pass": "Final Grade ≥ 10 (Pass)",
    "R2_final_excellent": "Final Grade ≥ 15 (Excellent)",
    "R3_mid_term_good": "Mid-Term ≥ 10",
    "R4_first_term_good": "First-Term ≥ 10",
    "R5_improving_trend": "Performance Improving",
    "R6_consistent_performance": "Consistent Marks",
    "R7_low_failures": "Low Failures (≤1)",
    "R8_high_failures": "High Failures (>2)",
    "R9_good_attendance": "Good Attendance ≥75%",
    "R10_good_studytime": "Study Time ≥3",
    "R11_support": "Support Available",
    "R12_low_alcohol": "Low Alcohol",
    "R13_low_social": "Low Social Activity"
}

for rule, status in rules.items():
    print(f"{rule_names.get(rule, rule):35} : {'✔' if status else '✘'}")

# FINAL RESULT
print("\n--------------------------------------------------")
print("FINAL RESULT:")
print("--------------------------------------------------")
print(f"Decision         : {decision}")
print(f"Confidence       : {confidence:.2f}%")
print(f"Stability        : {stability:.2f}%")
print("--------------------------------------------------")

# INTERPRETATION
print("\nINTERPRETATION:")
if stability > 80:
    print("• Decision is highly stable.")
elif stability > 60:
    print("• Decision is moderately stable.")
else:
    print("• Decision is sensitive to changes.")

if confidence > 75:
    print("• Strong rule support.")
elif confidence > 50:
    print("• Moderate support.")
else:
    print("• Weak support.")

# SENSITIVITY
print("\nSENSITIVITY:")
if all(v == 0 for v in impact.values()):
    print("• No feature changed decision → Highly stable")
else:
    for feature, count in impact.items():
        if count > 0:
            print(f"• {feature} influenced decision {count} times")