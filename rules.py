# rules.py

def extract_facts(row):
    """
    Convert student data into propositional logic facts
    """

    facts = {
        # -------------------------------
        # ACADEMIC
        # -------------------------------
        "A": row["final_grade"] >= 10,   # pass
        "B": row["final_grade"] >= 15,   # excellent
        "C": row["grade2"] >= 10,
        "D": row["grade1"] >= 10,
        "E": row["grade2"] >= row["grade1"],  # improving
        "F": abs(row["grade2"] - row["grade1"]) <= 2,  # consistent

        # -------------------------------
        # FAILURES
        # -------------------------------
        "G": row["failures"] <= 1,
        "Z": row["failures"] == 2,
        "H": row["failures"] > 2,

        # -------------------------------
        # ATTENDANCE
        # -------------------------------
        "I": row["attendance"] >= 75,
        "X": 50 <= row["attendance"] < 75,
        "P": row["attendance"] < 50,

        # -------------------------------
        # STUDY
        # -------------------------------
        "J": row["studytime"] >= 3,
        "Y": row["studytime"] == 2,
        "Q": row["studytime"] == 1,

        # -------------------------------
        # SUPPORT
        # -------------------------------
        "K": row["schoolsup"] == 1 or row["famsup"] == 1,

        # -------------------------------
        # LIFESTYLE
        # -------------------------------
        "L": row["Dalc"] <= 2,
        "M": row["goout"] <= 3,
        "R": row["goout"] >= 4 and row["Dalc"] >= 4,

        # -------------------------------
        # CRITICAL FAIL CONDITIONS
        # -------------------------------
        "N": row["final_grade"] < 8,
        "O": row["grade2"] < 8
    }

    return facts


def get_rules():
    """
    Logical rules (Propositional Logic)
    """

    rules = [

        # ===============================
        # STRONG PASS CONDITIONS
        # ===============================
        ("PASS", "A AND I AND G"),              # basic strong condition
        ("PASS", "B AND I"),                    # excellent student
        ("PASS", "A AND C AND D"),              # all exams good
        ("PASS", "A AND E AND F"),              # improving & consistent
        ("PASS", "A AND J AND I"),              # studies well + attendance
        ("PASS", "A AND K AND G"),
        ("PASS", "A AND X AND Y"),  # average but still stable
        ("PASS", "A AND G AND X"),  # moderate failures but decent attendance
        # support + low failures

        # ===============================
        # MODERATE PASS CONDITIONS
        # ===============================
        ("PASS", "A AND C AND I"),              # mid + final good
        ("PASS", "A AND D AND G"),              # first term + low failures
        ("PASS", "A AND L AND M"),              # good lifestyle
        ("PASS", "A AND F AND I"),              # consistency + attendance

        # ===============================
        # FAIL CONDITIONS (STRONG)
        # ===============================
        ("FAIL", "H"),                          # high failures
        ("FAIL", "N"),                          # very low final
        ("FAIL", "P AND H"),                    # poor attendance + failures
        ("FAIL", "Q AND N"),                    # no study + bad grade
        ("FAIL", "R"),                          # bad lifestyle

        # ===============================
        # FAIL CONDITIONS (MODERATE)
        # ===============================
        ("FAIL", "NOT A AND O"),                # weak overall performance
        ("FAIL", "NOT I AND H"),                # low attendance + failures
        ("FAIL", "NOT J AND N"),                # low study + bad final
        ("FAIL", "P AND Q"),                    # poor attendance + no study
        ("FAIL", "O AND NOT D"),
        ("FAIL", "P AND Y"),  # low attendance even with moderate study
        ("FAIL", "Z AND NOT J"),  # borderline failures + low study
        # weak mid + weak base

    ]

    return rules