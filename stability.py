# stability.py

import random
from rules import extract_facts, get_rules
from utils import make_decision
from confidence import calculate_confidence


# -----------------------------------
# MONTE CARLO PERTURBATION
# -----------------------------------
def perturb_input(row):
    new_row = row.copy()

    # Academic variation
    new_row["final_grade"] += random.uniform(-3, 3)
    new_row["grade2"] += random.uniform(-3, 3)
    new_row["grade1"] += random.uniform(-3, 3)

    # Attendance
    new_row["attendance"] += random.uniform(-15, 15)

    # Failures
    new_row["failures"] += random.choice([-1, 0, 1])

    # Study
    new_row["studytime"] += random.choice([-1, 0, 1])

    # Lifestyle
    new_row["goout"] += random.choice([-1, 0, 1])
    new_row["Dalc"] += random.choice([-1, 0, 1])

    # Support flip
    if random.random() < 0.3:
        new_row["schoolsup"] = 1 - new_row["schoolsup"]
    if random.random() < 0.3:
        new_row["famsup"] = 1 - new_row["famsup"]

    # Clamp values
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
# ROBUSTNESS ANALYSIS
# -----------------------------------
def calculate_robustness(original_row, iterations=100):

    rules = get_rules()

    # Original evaluation
    facts = extract_facts(original_row)
    decision, _, pass_score, fail_score = make_decision(facts, rules)
    base_confidence, _, _ = calculate_confidence(decision, pass_score, fail_score)

    unchanged = 0
    confidence_changes = []

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

        facts_p = extract_facts(perturbed)
        new_decision, _, p_score, f_score = make_decision(facts_p, rules)

        new_confidence, _, _ = calculate_confidence(new_decision, p_score, f_score)

        # Decision stability
        if new_decision == decision:
            unchanged += 1

        # Confidence variation
        confidence_changes.append(abs(new_confidence - base_confidence))

        # Feature sensitivity
        if new_decision != decision:
            for key in feature_impact:
                if abs(perturbed[key] - original_row[key]) > 0:
                    feature_impact[key] += 1

    robustness = (unchanged / iterations) * 100
    avg_conf_change = (
        sum(confidence_changes) / len(confidence_changes)
        if confidence_changes else 0
    )

    return robustness, avg_conf_change, feature_impact