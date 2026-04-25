from MFAI_CP.fol_engine import FOLEngine


def fol_inference(data, student_index):
    student = data.iloc[student_index]

    engine = FOLEngine()

    # -------------------------------
    # ADD FACTS (Predicates)
    # -------------------------------
    engine.add_fact("FinalGrade", student["final_grade"])
    engine.add_fact("Attendance", student["attendance"])
    engine.add_fact("Failures", student["failures"])
    engine.add_fact("StudyTime", student["studytime"])

    avg_grade = data["final_grade"].mean()
    avg_att = data["attendance"].mean()
    avg_fail = data["failures"].mean()

    # -------------------------------
    # ADD RULES (REAL FOL STYLE)
    # -------------------------------

    engine.add_rule(
        lambda f: f["FinalGrade"] < avg_grade,
        f"Below average grade ({student['final_grade']} vs {avg_grade:.2f})",
        "∀x (FinalGrade(x) < AvgGrade → BelowAverage(x))"
    )

    engine.add_rule(
        lambda f: f["Attendance"] < avg_att,
        f"Low attendance ({student['attendance']} vs {avg_att:.2f})",
        "∀x (Attendance(x) < AvgAttendance → LowAttendance(x))"
    )

    engine.add_rule(
        lambda f: f["Failures"] > avg_fail,
        f"High failures ({student['failures']} vs {avg_fail:.2f})",
        "∀x (Failures(x) > AvgFailures → HighFailure(x))"
    )

    engine.add_rule(
        lambda f: f["Attendance"] < 50 and f["StudyTime"] <= 2,
        "Risk pattern: low attendance + low study",
        "∀x (Attendance(x)<50 ∧ StudyTime(x)≤2 → AtRisk(x))"
    )

    engine.add_rule(
        lambda f: f["FinalGrade"] < 8 and f["Failures"] > 1,
        "High risk student",
        "∀x (FinalGrade(x)<8 ∧ Failures(x)>1 → HighRisk(x))"
    )

    # -------------------------------
    # RUN INFERENCE
    # -------------------------------
    results = engine.infer()

    if not results:
        results.append({
            "result": "Student is within normal range across all parameters",
            "fol": "∀x (Normal(x))"
        })

    return results