# utils.py

def evaluate_expression(expression, facts):
    """
    Evaluate logical expression using facts
    """

    expr = expression.replace("AND", "and") \
                     .replace("OR", "or") \
                     .replace("NOT", "not")

    try:
        return eval(expr, {}, facts)
    except Exception:
        return False


def infer(facts, rules):
    """
    Evaluate all rules and return triggered ones
    """

    triggered = []

    for outcome, expression in rules:
        if evaluate_expression(expression, facts):
            triggered.append((outcome, expression))

    return triggered


def score_rules(facts, rules):
    """
    Improved scoring using BOTH satisfied and unsatisfied rules
    """

    pass_score = 0
    fail_score = 0

    for outcome, expr in rules:

        # Evaluate rule
        result = evaluate_expression(expr, facts)

        # Rule strength
        strength = expr.count("AND") + 1

        if outcome == "PASS":
            if result:
                pass_score += strength
            else:
                fail_score += strength * 0.5   # penalty

        elif outcome == "FAIL":
            if result:
                fail_score += strength
            else:
                pass_score += strength * 0.5   # penalty

    return pass_score, fail_score

def make_decision(facts, rules):
    """
    Final decision using logical inference + rule strength
    """

    triggered = infer(facts, rules)

    pass_score, fail_score = score_rules(facts, rules)

    # Decision logic
    if fail_score > pass_score:
        decision = "FAIL"
    elif pass_score > fail_score:
        decision = "PASS"
    else:
        decision = "FAIL"  # safe fallback

    return decision, triggered, pass_score, fail_score