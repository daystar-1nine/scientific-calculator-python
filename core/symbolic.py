"""
Symbolic math engine for differentiation and expression simplification.
"""

import ast
import re

# Operators mapping back to calculator syntax
OP_MAP = {
    ast.Add: "+",
    ast.Sub: "-",
    ast.Mult: "*",
    ast.Div: "/",
    ast.Pow: "^"
}

def parse_to_ast(expr_str):
    # Standard python ast parse
    # Replace caret with double asterisk for parsing
    py_expr = expr_str.replace("^", "**")
    node = ast.parse(py_expr, mode='eval')
    return node.body

def contains_var(node, var):
    if isinstance(node, ast.Name):
        return node.id == var
    elif isinstance(node, ast.BinOp):
        return contains_var(node.left, var) or contains_var(node.right, var)
    elif isinstance(node, ast.UnaryOp):
        return contains_var(node.operand, var)
    elif isinstance(node, ast.Call):
        return any(contains_var(arg, var) for arg in node.args)
    return False

def diff_node(node, var):
    if isinstance(node, ast.Constant):
        return ast.Constant(value=0.0)
    elif hasattr(ast, 'Num') and isinstance(node, getattr(ast, 'Num')):
        return ast.Constant(value=0.0)
    elif isinstance(node, ast.Name):
        if node.id == var:
            return ast.Constant(value=1.0)
        return ast.Constant(value=0.0)
    elif isinstance(node, ast.BinOp):
        if isinstance(node.op, ast.Add):
            return ast.BinOp(left=diff_node(node.left, var), op=ast.Add(), right=diff_node(node.right, var))
        elif isinstance(node.op, ast.Sub):
            return ast.BinOp(left=diff_node(node.left, var), op=ast.Sub(), right=diff_node(node.right, var))
        elif isinstance(node.op, ast.Mult):
            # Product rule: u'v + uv'
            part1 = ast.BinOp(left=diff_node(node.left, var), op=ast.Mult(), right=node.right)
            part2 = ast.BinOp(left=node.left, op=ast.Mult(), right=diff_node(node.right, var))
            return ast.BinOp(left=part1, op=ast.Add(), right=part2)
        elif isinstance(node.op, ast.Div):
            # Quotient rule: (u'v - uv') / v^2
            u_prime_v = ast.BinOp(left=diff_node(node.left, var), op=ast.Mult(), right=node.right)
            u_v_prime = ast.BinOp(left=node.left, op=ast.Mult(), right=diff_node(node.right, var))
            numerator = ast.BinOp(left=u_prime_v, op=ast.Sub(), right=u_v_prime)
            denominator = ast.BinOp(left=node.right, op=ast.Pow(), right=ast.Constant(value=2.0))
            return ast.BinOp(left=numerator, op=ast.Div(), right=denominator)
        elif isinstance(node.op, ast.Pow):
            # Power rule: u^n -> n * u^(n-1) * u' (if exponent is constant)
            # Exponential rule: a^u -> a^u * ln(a) * u' (if base is constant)
            base_has_var = contains_var(node.left, var)
            exp_has_var = contains_var(node.right, var)
            
            if base_has_var and not exp_has_var:
                # u^n -> n * u^(n-1) * u'
                n_minus_1 = ast.BinOp(left=node.right, op=ast.Sub(), right=ast.Constant(value=1.0))
                u_pow = ast.BinOp(left=node.left, op=ast.Pow(), right=n_minus_1)
                coeff = ast.BinOp(left=node.right, op=ast.Mult(), right=u_pow)
                return ast.BinOp(left=coeff, op=ast.Mult(), right=diff_node(node.left, var))
            elif not base_has_var and exp_has_var:
                # a^u -> a^u * ln(a) * u'
                ln_a = ast.Call(func=ast.Name(id='ln', ctx=ast.Load()), args=[node.left], keywords=[])
                factor = ast.BinOp(left=node, op=ast.Mult(), right=ln_a)
                return ast.BinOp(left=factor, op=ast.Mult(), right=diff_node(node.right, var))
            elif base_has_var and exp_has_var:
                # General rule: (e^(v * ln(u)))'
                # Let's simplify and return general formula: u^v * (v' * ln(u) + v * u' / u)
                ln_u = ast.Call(func=ast.Name(id='ln', ctx=ast.Load()), args=[node.left], keywords=[])
                term1 = ast.BinOp(left=diff_node(node.right, var), op=ast.Mult(), right=ln_u)
                
                u_prime_over_u = ast.BinOp(left=diff_node(node.left, var), op=ast.Div(), right=node.left)
                term2 = ast.BinOp(left=node.right, op=ast.Mult(), right=u_prime_over_u)
                
                factor = ast.BinOp(left=term1, op=ast.Add(), right=term2)
                return ast.BinOp(left=node, op=ast.Mult(), right=factor)
            else:
                return ast.Constant(value=0.0)

    elif isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.USub):
            return ast.UnaryOp(op=ast.USub(), operand=diff_node(node.operand, var))
        elif isinstance(node.op, ast.UAdd):
            return ast.UnaryOp(op=ast.UAdd(), operand=diff_node(node.operand, var))

    elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        func_name = node.func.id.lower()
        u = node.args[0]
        u_prime = diff_node(u, var)
        
        if func_name == 'sin':
            # cos(u) * u'
            cos_u = ast.Call(func=ast.Name(id='cos', ctx=ast.Load()), args=[u], keywords=[])
            return ast.BinOp(left=cos_u, op=ast.Mult(), right=u_prime)
        elif func_name == 'cos':
            # -sin(u) * u'
            neg_sin_u = ast.UnaryOp(op=ast.USub(), operand=ast.Call(func=ast.Name(id='sin', ctx=ast.Load()), args=[u], keywords=[]))
            return ast.BinOp(left=neg_sin_u, op=ast.Mult(), right=u_prime)
        elif func_name == 'tan':
            # u' / (cos(u)^2)
            cos_u = ast.Call(func=ast.Name(id='cos', ctx=ast.Load()), args=[u], keywords=[])
            cos_u_sq = ast.BinOp(left=cos_u, op=ast.Pow(), right=ast.Constant(value=2.0))
            return ast.BinOp(left=u_prime, op=ast.Div(), right=cos_u_sq)
        elif func_name in ['ln', 'log']:
            # u' / u
            return ast.BinOp(left=u_prime, op=ast.Div(), right=u)
        elif func_name == 'exp':
            # exp(u) * u'
            return ast.BinOp(left=node, op=ast.Mult(), right=u_prime)
        elif func_name == 'sqrt':
            # u' / (2 * sqrt(u))
            denom = ast.BinOp(left=ast.Constant(value=2.0), op=ast.Mult(), right=node)
            return ast.BinOp(left=u_prime, op=ast.Div(), right=denom)
            
    return ast.Constant(value=0.0)

def is_val(node, val):
    if isinstance(node, ast.Constant) and node.value == val:
        return True
    if hasattr(ast, 'Num') and isinstance(node, getattr(ast, 'Num')) and node.n == val:
        return True
    return False

def get_val(node):
    if isinstance(node, ast.Constant):
        return node.value
    if hasattr(ast, 'Num') and isinstance(node, getattr(ast, 'Num')):
        return node.n
    return None

def is_const(node):
    return isinstance(node, ast.Constant) or (hasattr(ast, 'Num') and isinstance(node, getattr(ast, 'Num')))

def simplify_node(node):
    if isinstance(node, ast.BinOp):
        left = simplify_node(node.left)
        right = simplify_node(node.right)
        
        # Constant folding
        if is_const(left) and is_const(right):
            lval = get_val(left)
            rval = get_val(right)
            try:
                if isinstance(node.op, ast.Add):
                    return ast.Constant(value=lval + rval)
                elif isinstance(node.op, ast.Sub):
                    return ast.Constant(value=lval - rval)
                elif isinstance(node.op, ast.Mult):
                    return ast.Constant(value=lval * rval)
                elif isinstance(node.op, ast.Div) and rval != 0:
                    return ast.Constant(value=lval / rval)
                elif isinstance(node.op, ast.Pow):
                    return ast.Constant(value=lval ** rval)
            except Exception:
                pass

        if isinstance(node.op, ast.Add):
            if is_val(left, 0.0):
                return right
            if is_val(right, 0.0):
                return left
        elif isinstance(node.op, ast.Sub):
            if is_val(right, 0.0):
                return left
            if is_val(left, 0.0):
                return ast.UnaryOp(op=ast.USub(), operand=right)
            # check structural equivalence
            if ast.dump(left) == ast.dump(right):
                return ast.Constant(value=0.0)
        elif isinstance(node.op, ast.Mult):
            if is_val(left, 0.0) or is_val(right, 0.0):
                return ast.Constant(value=0.0)
            if is_val(left, 1.0):
                return right
            if is_val(right, 1.0):
                return left
            # constant scaling propagation, e.g. 3 * (2 * x) -> 6 * x
            if is_const(left) and isinstance(right, ast.BinOp) and isinstance(right.op, ast.Mult) and is_const(right.left):
                return ast.BinOp(left=ast.Constant(value=get_val(left) * get_val(right.left)), op=ast.Mult(), right=right.right)
            if is_const(right) and isinstance(left, ast.BinOp) and isinstance(left.op, ast.Mult) and is_const(left.right):
                return ast.BinOp(left=left.left, op=ast.Mult(), right=ast.Constant(value=get_val(left.right) * get_val(right)))
            if is_const(right) and isinstance(left, ast.BinOp) and isinstance(left.op, ast.Mult) and is_const(left.left):
                return ast.BinOp(left=ast.Constant(value=get_val(left.left) * get_val(right)), op=ast.Mult(), right=left.right)
        elif isinstance(node.op, ast.Div):
            if is_val(left, 0.0):
                return ast.Constant(value=0.0)
            if is_val(right, 1.0):
                return left
            if ast.dump(left) == ast.dump(right):
                return ast.Constant(value=1.0)
        elif isinstance(node.op, ast.Pow):
            if is_val(right, 0.0):
                return ast.Constant(value=1.0)
            if is_val(right, 1.0):
                return left
            if is_val(left, 0.0):
                return ast.Constant(value=0.0)
            if is_val(left, 1.0):
                return ast.Constant(value=1.0)

        return ast.BinOp(left=left, op=node.op, right=right)

    elif isinstance(node, ast.UnaryOp):
        operand = simplify_node(node.operand)
        if isinstance(node.op, ast.USub) and isinstance(operand, ast.UnaryOp) and isinstance(operand.op, ast.USub):
            return operand.operand # -(-x) -> x
        if is_val(operand, 0.0):
            return ast.Constant(value=0.0)
        return ast.UnaryOp(op=node.op, operand=operand)

    elif isinstance(node, ast.Call):
        args = [simplify_node(arg) for arg in node.args]
        return ast.Call(func=node.func, args=args, keywords=node.keywords)

    return node

def node_to_str(node):
    if isinstance(node, ast.Constant):
        val = node.value
        if isinstance(val, float) and val.is_integer():
            return str(int(val))
        return str(val)
    elif hasattr(ast, 'Num') and isinstance(node, getattr(ast, 'Num')):
        val = node.n
        if isinstance(val, float) and val.is_integer():
            return str(int(val))
        return str(val)
    elif isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.BinOp):
        op = OP_MAP.get(type(node.op), "?")
        left_str = node_to_str(node.left)
        right_str = node_to_str(node.right)
        
        def needs_paren(child, parent_op):
            if isinstance(child, ast.BinOp):
                if parent_op in [ast.Mult, ast.Div, ast.Pow] and type(child.op) in [ast.Add, ast.Sub]:
                    return True
                if parent_op == ast.Pow and type(child.op) in [ast.Mult, ast.Div]:
                    return True
            if isinstance(child, ast.UnaryOp):
                if parent_op in [ast.Mult, ast.Div, ast.Pow]:
                    return True
            return False

        if needs_paren(node.left, type(node.op)):
            left_str = f"({left_str})"
        if needs_paren(node.right, type(node.op)):
            right_str = f"({right_str})"
            
        if op == "^":
            return f"{left_str}{op}{right_str}"
        return f"{left_str} {op} {right_str}"
    elif isinstance(node, ast.UnaryOp):
        op = "-" if isinstance(node.op, ast.USub) else "+"
        operand_str = node_to_str(node.operand)
        if isinstance(node.operand, ast.BinOp):
            operand_str = f"({operand_str})"
        return f"{op}{operand_str}"
    elif isinstance(node, ast.Call):
        args_str = ", ".join(node_to_str(arg) for arg in node.args)
        return f"{node.func.id}({args_str})"
    return "?"

def differentiate(expr_str, var='x'):
    try:
        # Preprocess expression (implicit multiplication, caret replacement etc.)
        ast_node = parse_to_ast(expr_str)
        raw_diff = diff_node(ast_node, var)
        
        # Iteratively simplify until no changes occur (up to 3 times)
        simplified = raw_diff
        for _ in range(3):
            simplified = simplify_node(simplified)
            
        return node_to_str(simplified)
    except Exception as e:
        return f"Error: {str(e)}"
