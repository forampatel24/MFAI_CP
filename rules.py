def evaluate_rules(row):
    rules = {}

    # -------------------------------
    # CORE ACADEMIC (G1, G2, G3)
    # -------------------------------
    rules["R1_final_pass"] = row["final_grade"] >= 10
    rules["R2_final_excellent"] = row["final_grade"] >= 15

    rules["R3_mid_term_good"] = row["grade2"] >= 10
    rules["R4_first_term_good"] = row["grade1"] >= 10

    rules["R5_improving_trend"] = row["grade2"] >= row["grade1"]
    rules["R6_consistent_performance"] = abs(row["grade2"] - row["grade1"]) <= 2

    # -------------------------------
    # FAILURES
    # -------------------------------
    rules["R7_low_failures"] = row["failures"] <= 1
    rules["R8_high_failures"] = row["failures"] > 2

    # -------------------------------
    # ATTENDANCE
    # -------------------------------
    rules["R9_good_attendance"] = row["attendance"] >= 75

    # -------------------------------
    # STUDY
    # -------------------------------
    rules["R10_good_studytime"] = row["studytime"] >= 3

    # -------------------------------
    # SUPPORT
    # -------------------------------
    rules["R11_support"] = row["schoolsup"] == 1 or row["famsup"] == 1

    # -------------------------------
    # LIFESTYLE
    # -------------------------------
    rules["R12_low_alcohol"] = row["Dalc"] <= 2
    rules["R13_low_social"] = row["goout"] <= 3

    rules["R14_very_low_final"] = row["final_grade"] < 8

    rules["R15_very_low_mid"] = row["grade2"] < 8
    rules["R16_poor_attendance"] = row["attendance"] < 50
    rules["R17_no_study"] = row["studytime"] == 1
    rules["R18_high_risk_lifestyle"] = row["goout"] >= 4 and row["Dalc"] >= 4

    return rules