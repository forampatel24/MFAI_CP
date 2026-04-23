import math

def calculate_confidence(decision, pass_score, fail_score):
    """
    Scaled softmax to avoid extreme 100% confidence
    """

    # SCALE DOWN scores (IMPORTANT)
    scale = 10   # <-- adjust this

    p = pass_score / scale
    f = fail_score / scale

    max_score = max(p, f)

    exp_pass = math.exp(p - max_score)
    exp_fail = math.exp(f - max_score)

    total = exp_pass + exp_fail

    prob_pass = (exp_pass / total) * 100
    prob_fail = (exp_fail / total) * 100

    confidence = prob_pass if decision == "PASS" else prob_fail

    return confidence, prob_pass, prob_fail