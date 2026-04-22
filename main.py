import pandas as pd

from rules import extract_facts, get_rules
from utils import make_decision
from confidence import calculate_confidence
from stability import calculate_robustness


# -------------------------------
# LOAD DATA
# -------------------------------
data = pd.read_csv(
    r"C:\Foram\ENG_SY\SEM2\MFAI\CP\MFAI_CP\data\student-mat.csv",
    sep=";"
)

print("\nDataset Loaded Successfully!\n")


# -------------------------------
# CLEANING
# -------------------------------
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

print("\nCleaned Dataset:\n")
print(data.head())


# -------------------------------
# SELECT SAMPLE
# -------------------------------
sample = data.iloc[350]


# -------------------------------
# NEW AI PIPELINE
# -------------------------------

facts = extract_facts(sample)
rules = get_rules()

decision, triggered, pass_score, fail_score = make_decision(facts, rules)

confidence, p_pass, p_fail = calculate_confidence(
    decision,
    pass_score,
    fail_score
)

robustness, avg_conf_change, impact = calculate_robustness(sample)


# -------------------------------
# REPORT
# -------------------------------

print("\n================ AI DECISION REPORT ================\n")

# INPUT
print("INPUT SUMMARY:")
print("--------------------------------------------------")
print(f"Grade 1           : {sample['grade1']}")
print(f"Grade 2           : {sample['grade2']}")
print(f"Final Grade       : {sample['final_grade']}")
print(f"Attendance        : {sample['attendance']}%")
print(f"Failures          : {sample['failures']}")
print("--------------------------------------------------")


# -------------------------------
# LOGICAL FACTS
# -------------------------------
print("\nLOGICAL FACTS:")
print("--------------------------------------------------")

for key, value in facts.items():
    print(f"{key} : {'✔' if value else '✘'}")


# -------------------------------
# TRIGGERED RULES
# -------------------------------
print("\nTRIGGERED RULES:")
print("--------------------------------------------------")

if not triggered:
    print("No rules triggered")
else:
    for outcome, expr in triggered:
        print(f"{outcome}  ←  {expr}")


# -------------------------------
# SCORES
# -------------------------------
print("\nEVIDENCE SCORES:")
print("--------------------------------------------------")
print(f"PASS Score        : {pass_score:.2f}")
print(f"FAIL Score        : {fail_score:.2f}")


# -------------------------------
# FINAL RESULT
# -------------------------------
print("\nFINAL RESULT:")
print("--------------------------------------------------")
print(f"Decision          : {decision}")
print(f"Confidence        : {confidence:.2f}%")
print(f"P(PASS)           : {p_pass:.2f}%")
print(f"P(FAIL)           : {p_fail:.2f}%")
print(f"Robustness        : {robustness:.2f}%")
print("--------------------------------------------------")


# -------------------------------
# INTERPRETATION
# -------------------------------
print("\nINTERPRETATION:")

if robustness > 80:
    print("• Decision is highly robust.")
elif robustness > 60:
    print("• Decision is moderately robust.")
else:
    print("• Decision is sensitive to changes.")

if confidence > 75:
    print("• Strong probabilistic support.")
elif confidence > 50:
    print("• Moderate support.")
else:
    print("• Weak support.")

print(f"• Avg Confidence Change: {avg_conf_change:.2f}")


# -------------------------------
# FEATURE SENSITIVITY
# -------------------------------
print("\nFEATURE SENSITIVITY:")

if all(v == 0 for v in impact.values()):
    print("• No feature influenced decision → Highly stable")
else:
    for feature, count in impact.items():
        if count > 0:
            print(f"• {feature} influenced decision {count} times")