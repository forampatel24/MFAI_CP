def calculate_confidence(rules, decision):

    weights = {
    "R1_final_pass": 1.0,
    "R2_final_excellent": 0.8,
    "R3_mid_term_good": 0.8,
    "R4_first_term_good": 0.7,
    "R5_improving_trend": 0.6,
    "R6_consistent_performance": 0.6,
    "R7_low_failures": 0.9,
    "R9_good_attendance": 0.8,
    "R10_good_studytime": 0.6,
    "R11_support": 0.5,
    "R12_low_alcohol": 0.5,
    "R13_low_social": 0.5
    }

    total_weight = sum(weights.values())
    satisfied_weight = 0

    for rule, value in rules.items():
        if value and rule in weights:
            satisfied_weight += weights[rule]

    confidence = (satisfied_weight / total_weight) * 100

    return confidence, weights