def calculate_confidence(decision, pass_score, fail_score):
    """
    Compute conditional probability with smoothing
    """

    epsilon = 1e-6
    total = pass_score + fail_score

    if total == 0:
        return 0, 0, 0

    prob_pass = (pass_score + epsilon) / (total + 2 * epsilon)
    prob_fail = (fail_score + epsilon) / (total + 2 * epsilon)

    prob_pass *= 100
    prob_fail *= 100

    confidence = prob_pass if decision == "PASS" else prob_fail

    return confidence, prob_pass, prob_fail