import pandas as pd
from rules import evaluate_rules
from utils import make_decision
from confidence import calculate_confidence
from stability import calculate_stability

# Load dataset
data = pd.read_csv("C:\Foram\ENG_SY\SEM2\MFAI\CP\MFAI_CP\data\student-mat.csv", sep=";")

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

print("\n--- RULE EVALUATION (Sample Case) ---\n")

# Take first row as example
sample = data.iloc[1]

# Apply rules
rules = evaluate_rules(sample)

# Print rule results
for rule, status in rules.items():
    print(f"{rule} : {'Satisfied' if status else 'Not Satisfied'}")


# -----------------------------------
# FINAL DECISION
# -----------------------------------

decision = make_decision(rules)

print("\nFinal Decision:", decision)

# -----------------------------------
# CONFIDENCE CALCULATION
# -----------------------------------

confidence, weights = calculate_confidence(rules, decision)

print(f"Confidence Score: {confidence:.2f}%")

# -----------------------------------
# STABILITY ANALYSIS
# -----------------------------------

stability, unchanged, total, impact = calculate_stability(sample)

print(f"\nStability Score: {stability:.2f}%")
print(f"Unchanged Decisions: {unchanged}/{total}")

print("\nSensitivity Insights:")

for feature, count in impact.items():
    if count > 0:
        print(f"{feature} influenced decision {count} times")