# stability.py

import random
from rules import extract_facts, get_rules
from utils import make_decision
from confidence import calculate_confidence


# -----------------------------------
# CONTROLLED PERTURBATION
# -----------------------------------
def perturb_input(row):
    new_row = row.copy()

    changed = False  # track if anything changed

    # -------------------------------
    # FINAL GRADE
    # -------------------------------
    if random.random() < 0.4:
        new_row["final_grade"] = random.choice([5, 9, 12, 16])
        changed = True

    # -------------------------------
    # MID & FIRST GRADE
    # -------------------------------
    if random.random() < 0.4:
        new_row["grade2"] = random.choice([5, 9, 12, 16])
        changed = True

    if random.random() < 0.4:
        new_row["grade1"] = random.choice([5, 9, 12, 16])
        changed = True

    # -------------------------------
    # ATTENDANCE
    # -------------------------------
    if random.random() < 0.5:
        new_row["attendance"] = random.choice([40, 60, 85])
        changed = True

    # -------------------------------
    # FAILURES
    # -------------------------------
    if random.random() < 0.4:
        new_row["failures"] = random.choice([0, 2, 3])
        changed = True

    # -------------------------------
    # STUDY TIME
    # -------------------------------
    if random.random() < 0.4:
        new_row["studytime"] = random.choice([1, 2, 3, 4])
        changed = True

    # -------------------------------
    # LIFESTYLE
    # -------------------------------
    if random.random() < 0.4:
        new_row["goout"] = random.choice([1, 3, 5])
        changed = True

    if random.random() < 0.4:
        new_row["Dalc"] = random.choice([1, 3, 5])
        changed = True

    # -------------------------------
    # SUPPORT
    # -------------------------------
    if random.random() < 0.3:
        new_row["schoolsup"] = random.choice([0, 1])
        changed = True

    if random.random() < 0.3:
        new_row["famsup"] = random.choice([0, 1])
        changed = True

    # -------------------------------
    # FORCE CHANGE (IMPORTANT)
    # -------------------------------
    if not changed:
        # force one meaningful category jump
        feature = random.choice([
            "final_grade",
            "attendance",
            "studytime"
        ])

        if feature == "final_grade":
            new_row["final_grade"] = random.choice([5, 9, 12, 16])

        elif feature == "attendance":
            new_row["attendance"] = random.choice([40, 60, 85])

        elif feature == "studytime":
            new_row["studytime"] = random.choice([1, 2, 3, 4])

    return new_row


# -----------------------------------
# ROBUSTNESS ANALYSIS (IMPROVED)
# -----------------------------------
def calculate_robustness(original_row, iterations=100):

    rules = get_rules()

    # Original evaluation
    original_facts = extract_facts(original_row)
    decision, _, pass_score, fail_score = make_decision(original_facts, rules)
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

        new_facts = extract_facts(perturbed)
        new_decision, _, p_score, f_score = make_decision(new_facts, rules)

        new_confidence, _, _ = calculate_confidence(new_decision, p_score, f_score)

        # ---------------------------
        # Decision Stability
        # ---------------------------
        if new_decision == decision:
            unchanged += 1

        # ---------------------------
        # Confidence Change
        # ---------------------------
        confidence_changes.append(abs(new_confidence - base_confidence))

        # ---------------------------
        # FACT-LEVEL SENSITIVITY
        # ---------------------------
        if new_decision != decision:

            for key in feature_impact:

                # Compare original vs perturbed feature
                if new_decision != decision and perturbed[key] != original_row[key]:
                    feature_impact[key] += 1

            # Bonus: detect fact-level change
            fact_changes = sum(
                1 for f in original_facts
                if original_facts[f] != new_facts[f]
            )

    decision_flips = iterations - unchanged

    robustness = (1 - (decision_flips / iterations)) * 100

    avg_conf_change = (
        sum(confidence_changes) / len(confidence_changes)
        if confidence_changes else 0
    )

    return robustness, avg_conf_change, feature_impact