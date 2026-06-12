"""
Improved Parser - Cleaner, Scalable, Maintainable
"""

import re
from utils.error_handler import InvalidExpressionError


class Parser:

    # Central definitions (VERY IMPORTANT)
    FUNCTIONS = {
        'sin', 'cos', 'tan',
        'asin', 'acos', 'atan',
        'sinh', 'cosh', 'tanh',
        'log', 'ln', 'sqrt',
        'factorial', 'exp'
    }

    CONSTANTS = {'PI', 'E', 'X'}

    def parse(self, expression: str, custom_functions: dict = None) -> str:
        if not expression or not isinstance(expression, str):
            raise InvalidExpressionError("Expression must be a non-empty string")

        expr = expression.strip()

        # Step 0: Expand user-defined custom functions
        if custom_functions:
            expr = self._expand_custom_functions(expr, custom_functions)

        # Step 1: Replace exponent operator
        expr = expr.replace("^", "**")

        # Step 2: Factorial handling
        expr = self._parse_factorials(expr)

        # Step 3: Implicit multiplication
        expr = self._handle_implicit_multiplication(expr)

        # Step 4: Complex numbers
        expr = self._handle_complex(expr)

        # Step 5: Casing normalization
        expr = self._normalize_casing(expr)

        return expr

    # ---------------------------
    # NORMALIZATION
    # ---------------------------
    def _normalize_casing(self, expr):
        expr = re.sub(r'\bpi\b', 'PI', expr, flags=re.IGNORECASE)
        expr = re.sub(r'\be\b', 'E', expr, flags=re.IGNORECASE)
        for func in self.FUNCTIONS:
            expr = re.sub(rf'\b{func}\b', func, expr, flags=re.IGNORECASE)
        return expr

    # ---------------------------
    # IMPLICIT MULTIPLICATION
    # ---------------------------
    def _handle_implicit_multiplication(self, expr):
        patterns = [
            (r'(\d+(?:\.\d+)?)\s*\(', r'\1*('),
            (r'\)\s*(\d+(?:\.\d+)?)', r')*\1'),
            (r'\)\s*\(', r')*('),
            (r'(\d+(?:\.\d+)?)\s*([a-zA-Z_])', r'\1*\2'),
            (r'\)\s*([a-zA-Z_])', r')*\1'),
            (r'\b(PI|E|X)\s*\(', r'\1*('),
            (r'\b(PI|E|X)\s+(PI|E|X|sin|cos|tan|asin|acos|atan|sinh|cosh|tanh|log|ln|sqrt|factorial|exp)\b', r'\1*\2'),
        ]

        for pattern, repl in patterns:
            expr = re.sub(pattern, repl, expr, flags=re.IGNORECASE)

        return expr

    # ---------------------------
    # COMPLEX NUMBER SUPPORT
    # ---------------------------
    def _handle_complex(self, expr):
        expr = re.sub(r'(\d+(?:\.\d+)?)\s*i\b', r'\1*1j', expr)
        expr = re.sub(r'\bi\b', '1j', expr)
        return expr

    # ---------------------------
    # FACTORIAL HANDLING
    # ---------------------------
    def _parse_factorials(self, expr):
        while '!' in expr:
            idx = expr.find('!')

            if idx == 0:
                raise InvalidExpressionError("Invalid factorial placement")

            start = idx - 1

            # Case: parenthesis
            if expr[start] == ')':
                start = self._find_matching_paren(expr, start)

                # Include function name before '('
                func_start = start - 1
                while func_start >= 0 and expr[func_start].isalnum():
                    func_start -= 1

                operand_start = func_start + 1

            else:
                while start >= 0 and (expr[start].isalnum() or expr[start] == '.'):
                    start -= 1
                operand_start = start + 1

            operand = expr[operand_start:idx]

            if not operand:
                raise InvalidExpressionError("Invalid factorial operand")

            expr = (
                expr[:operand_start]
                + f"factorial({operand})"
                + expr[idx + 1:]
            )

        return expr

    def _find_matching_paren(self, expr, end_idx):
        count = 1
        i = end_idx - 1

        while i >= 0:
            if expr[i] == ')':
                count += 1
            elif expr[i] == '(':
                count -= 1

            if count == 0:
                return i

            i -= 1

        raise InvalidExpressionError("Mismatched parentheses")

    def _expand_custom_functions(self, expr, custom_functions):
        if not custom_functions:
            return expr
            
        for _ in range(5):
            old_expr = expr
            for name, data in custom_functions.items():
                args = data["args"]
                body = data["body"]
                pattern = rf'\b{re.escape(name)}\s*\('
                
                while True:
                    match = re.search(pattern, expr)
                    if not match:
                        break
                    
                    start_idx = match.start()
                    open_paren_idx = match.end() - 1
                    
                    count = 1
                    close_paren_idx = -1
                    for i in range(open_paren_idx + 1, len(expr)):
                        if expr[i] == '(':
                            count += 1
                        elif expr[i] == ')':
                            count -= 1
                        if count == 0:
                            close_paren_idx = i
                            break
                    
                    if close_paren_idx == -1:
                        break
                        
                    args_str = expr[open_paren_idx + 1:close_paren_idx]
                    
                    arg_vals = []
                    current_arg = []
                    paren_level = 0
                    for char in args_str:
                        if char == '(':
                            paren_level += 1
                            current_arg.append(char)
                        elif char == ')':
                            paren_level -= 1
                            current_arg.append(char)
                        elif char == ',' and paren_level == 0:
                            arg_vals.append("".join(current_arg).strip())
                            current_arg = []
                        else:
                            current_arg.append(char)
                    if current_arg:
                        arg_vals.append("".join(current_arg).strip())
                    
                    if len(arg_vals) != len(args):
                        raise InvalidExpressionError(f"Function {name} expects {len(args)} arguments, got {len(arg_vals)}")
                    
                    substituted_body = body
                    for arg_name, arg_val in zip(args, arg_vals):
                        substituted_body = re.sub(rf'\b{re.escape(arg_name)}\b', f"({arg_val})", substituted_body)
                    
                    expr = expr[:start_idx] + f"({substituted_body})" + expr[close_paren_idx + 1:]
            if expr == old_expr:
                break
        return expr