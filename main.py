from parser.Symbol import Symbol



a, b, c, d = Symbol.symbols("a b c d", sb_type = Symbol.Variable)
K, L, Q = Symbol.symbols("K L alpha", sb_type = Symbol.Constant)

expr = a * b * c * d * a * b * c * d


res = expr.node.gradient_product_rule()

print(res.expand())
res.print()