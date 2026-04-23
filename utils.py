# utils.py

def evaluate_expression(expression, facts):
    """
    Evaluate logical expression using facts safely
    """

    expr = expression.replace("AND", "and") \
                     .replace("OR", "or") \
                     .replace("NOT", "not")

    try:
        return eval(expr, {"__builtins__": None}, facts)
    except Exception as e:
        return False


# -----------------------------------
# INFERENCE
# -----------------------------------
def infer(facts, rules):
    """
    Evaluate all rules and return triggered ones
    """

    triggered = []

    for outcome, expression in rules:
        if evaluate_expression(expression, facts):
            triggered.append((outcome, expression))

    return triggered


# -----------------------------------
# IMPROVED SCORING SYSTEM
# -----------------------------------
def compute_strength(expr):
    """
    Better rule strength calculation
    """

    and_count = expr.count("AND")
    or_count = expr.count("OR")
    not_count = expr.count("NOT")

    # AND = strong constraint
    # OR = weaker
    # NOT = slight complexity

    return (and_count * 2) + (or_count * 1) + (not_count * 0.5) + 1


def score_rules(facts, rules):
    """
    Improved scoring using:
    - rule strength
    - partial penalties
    - balanced reasoning
    """

    pass_score = 0
    fail_score = 0

    for outcome, expr in rules:

        result = evaluate_expression(expr, facts)
        strength = compute_strength(expr)

        if outcome == "PASS":
            if result:
                pass_score += strength
            else:
                fail_score += strength * 0.4   # softer penalty

        elif outcome == "FAIL":
            if result:
                fail_score += strength
            else:
                pass_score += strength * 0.4   # softer penalty

    return pass_score, fail_score


# -----------------------------------
# FINAL DECISION
# -----------------------------------
def make_decision(facts, rules):
    """
    Final decision using logical inference + improved scoring
    """

    triggered = infer(facts, rules)

    pass_score, fail_score = score_rules(facts, rules)

    # Decision logic
    if fail_score > pass_score:
        decision = "FAIL"
    elif pass_score > fail_score:
        decision = "PASS"
    else:
        decision = "FAIL"  # conservative fallback

    return decision, triggered, pass_score, fail_score