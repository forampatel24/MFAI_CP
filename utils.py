def make_decision(rules):

    # Hard fail
    if rules["R8_high_failures"]:
        return "FAIL"

    score = 0

    # Academic (MOST IMPORTANT)
    if rules["R1_final_pass"]:
        score += 2
    if rules["R2_final_excellent"]:
        score += 1
    if rules["R3_mid_term_good"]:
        score += 1
    if rules["R4_first_term_good"]:
        score += 1

    # Trend
    if rules["R5_improving_trend"]:
        score += 0.5
    if rules["R6_consistent_performance"]:
        score += 0.5

    # Failures
    if rules["R7_low_failures"]:
        score += 1

    # Attendance
    if rules["R9_good_attendance"]:
        score += 1

    # Study
    if rules["R10_good_studytime"]:
        score += 0.5

    # Support
    if rules["R11_support"]:
        score += 0.5

    # Lifestyle
    if rules["R12_low_alcohol"]:
        score += 0.5
    if rules["R13_low_social"]:
        score += 0.5

    return "PASS" if score >= 5 else "FAIL"