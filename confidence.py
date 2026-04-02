def calculate_confidence(rules, decision):

    weights = {
        # PASS rules
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
        "R13_low_social": 0.5,

        # FAIL rules
        "R8_high_failures": 1.0,
        "R14_very_low_final": 1.0,
        "R15_very_low_mid": 0.9,
        "R16_poor_attendance": 0.9,
        "R17_no_study": 0.7,
        "R18_high_risk_lifestyle": 0.7
    }

    # Define rule types
    pass_rules = {
        "R1_final_pass", "R2_final_excellent", "R3_mid_term_good",
        "R4_first_term_good", "R5_improving_trend", "R6_consistent_performance",
        "R7_low_failures", "R9_good_attendance", "R10_good_studytime",
        "R11_support", "R12_low_alcohol", "R13_low_social"
    }

    fail_rules = {
        "R8_high_failures", "R14_very_low_final", "R15_very_low_mid",
        "R16_poor_attendance", "R17_no_study", "R18_high_risk_lifestyle"
    }

    pass_support = 0
    fail_support = 0

    for rule, value in rules.items():

        weight = weights.get(rule, 0)

        # PASS RULES
        if rule in pass_rules:
            if value:
                pass_support += weight
            else:
                fail_support += weight

        # FAIL RULES
        elif rule in fail_rules:
            if value:
                fail_support += weight
            else:
                pass_support += weight

    total_support = pass_support + fail_support

    if total_support == 0:
        return 0, weights

    if decision == "PASS":
        confidence = (pass_support / total_support) * 100
    else:
        confidence = (fail_support / total_support) * 100

    return confidence, weights