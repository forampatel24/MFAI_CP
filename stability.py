import random
from rules import evaluate_rules
from utils import make_decision


# -----------------------------------
# PERTURB INPUT (REALISTIC VARIATION)
# -----------------------------------
def perturb_input(row):
    new_row = row.copy()

    # Academic variations (IMPORTANT)
    new_row["final_grade"] += random.uniform(-3, 3)
    new_row["grade2"] += random.uniform(-3, 3)
    new_row["grade1"] += random.uniform(-3, 3)

    # Attendance
    new_row["attendance"] += random.uniform(-15, 15)

    # Failures
    new_row["failures"] += random.choice([-1, 0, 1])

    # Study behavior
    new_row["studytime"] += random.choice([-1, 0, 1])

    # Lifestyle
    new_row["goout"] += random.choice([-1, 0, 1])
    new_row["Dalc"] += random.choice([-1, 0, 1])

    # Support (flip sometimes)
    if random.random() < 0.3:
        new_row["schoolsup"] = 1 - new_row["schoolsup"]
    if random.random() < 0.3:
        new_row["famsup"] = 1 - new_row["famsup"]

    # -------------------------------
    # CLAMP VALUES (VERY IMPORTANT)
    # -------------------------------
    new_row["final_grade"] = max(0, min(20, new_row["final_grade"]))
    new_row["grade2"] = max(0, min(20, new_row["grade2"]))
    new_row["grade1"] = max(0, min(20, new_row["grade1"]))

    new_row["attendance"] = max(0, min(100, new_row["attendance"]))
    new_row["failures"] = max(0, new_row["failures"])

    new_row["studytime"] = max(1, min(4, new_row["studytime"]))
    new_row["goout"] = max(1, min(5, new_row["goout"]))
    new_row["Dalc"] = max(1, min(5, new_row["Dalc"]))

    return new_row


# -----------------------------------
# STABILITY CALCULATION
# -----------------------------------
def calculate_stability(original_row, iterations=100):

    original_rules = evaluate_rules(original_row)
    original_decision = make_decision(original_rules)

    unchanged = 0

    # Track feature sensitivity
    feature_impact = {
        "final_grade": 0,
        "grade2": 0,
        "grade1": 0,
        "attendance": 0,
        "failures": 0,
        "studytime": 0,
        "goout": 0,
        "Dalc": 0
    }

    for _ in range(iterations):

        perturbed = perturb_input(original_row)

        rules = evaluate_rules(perturbed)
        new_decision = make_decision(rules)

        if new_decision == original_decision:
            unchanged += 1
        else:
            # Track what changed most
            for key in feature_impact:
                if abs(perturbed[key] - original_row[key]) > 0:
                    feature_impact[key] += 1

    stability = (unchanged / iterations) * 100

    return stability, unchanged, iterations, feature_impact