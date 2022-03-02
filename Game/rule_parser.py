
class DefaultRuleParser:
    @staticmethod
    def parse_rule(rule):
        cond_tokens = rule.split(";")

        def f(x):
            chk = {
                "EQ": int.__eq__,
                "LT": int.__lt__,
                "GT": int.__gt__
            }
            return all(map(lambda rule_tuple: chk[rule_tuple[0]](x, int(rule_tuple[1])),  map(lambda s: s.split(":"), cond_tokens)))

        return f
