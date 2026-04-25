class FOLEngine:
    def __init__(self):
        self.facts = {}
        self.rules = []

    def add_fact(self, name, value):
        self.facts[name] = value

    def add_rule(self, condition, conclusion, fol_repr):
        self.rules.append({
            "condition": condition,
            "conclusion": conclusion,
            "fol": fol_repr
        })

    def infer(self):
        results = []

        for rule in self.rules:
            if rule["condition"](self.facts):
                results.append({
                    "result": rule["conclusion"],
                    "fol": rule["fol"]
                })

        return results