"""
Parses user input expressions before evaluation.
"""


import re
from utils.error_handler import InvalidExpressionError


class Parser:
    def parse(self, expression: str) -> str:
        """
        Cleans and normalizes the expression, resolving implicit multiplication and factorials.
        """
        if not expression or not isinstance(expression, str):
            raise InvalidExpressionError("Expression must be a non-empty string")
        
        # 1. Strip spaces but keep necessary spacing for words
        expression = expression.strip()
        
        # 2. Exponentiation caret replacement
        expression = expression.replace('^', '**')
        
        # 3. Resolve factorial exclamation marks (!) to factorial(...) calls
        expression = self._parse_factorials(expression)
        
        # 4. Implicit multiplication
        # Number followed by parenthesis: e.g., 2(3) -> 2*(3)
        expression = re.sub(r'(\d+(?:\.\d+)?)\s*\(', r'\1*(', expression)
        
        # Parenthesis followed by number: e.g., (3)2 -> (3)*2
        expression = re.sub(r'\)\s*(\d+(?:\.\d+)?)', r')*\1', expression)
        
        # Parenthesis followed by parenthesis: e.g., (2)(3) -> (2)*(3)
        expression = re.sub(r'\)\s*\(', r')*(', expression)
        
        # Number followed by constant or function: e.g., 2PI -> 2*PI, 2sin -> 2*sin
        expression = re.sub(r'(\d+(?:\.\d+)?)\s*([a-zA-Z_])', r'\1*\2', expression)
        
        # Parenthesis followed by constant or function: e.g., (3)PI -> (3)*PI, (3)sin -> (3)*sin
        expression = re.sub(r'\)\s*([a-zA-Z_])', r')*\1', expression)
        
        # Constant/variable followed by parenthesis: e.g., PI(3) -> PI*(3), x(3) -> x*(3)
        expression = re.sub(r'\b(PI|E|X)\s*\(', r'\1*(', expression, flags=re.IGNORECASE)
        
        # Constant/variable followed by constant/variable/function: e.g., PI E -> PI*E, x sin(x) -> x*sin(x)
        expression = re.sub(r'\b(PI|E|X)\s+(PI|E|X|sin|cos|tan|asin|acos|atan|sinh|cosh|tanh|log|ln|sqrt|factorial|exp)\b', r'\1*\2', expression, flags=re.IGNORECASE)
        
        # 4.5. Complex numbers imaginary unit 'i' (case-sensitive to avoid clashing with uppercase variable 'I')
        expression = re.sub(r'(\d+(?:\.\d+)?)\s*i\b', r'\1*1j', expression)
        expression = re.sub(r'\bi\b', '1j', expression)
        
        # 5. Casing normalization (done at the end so word boundaries \b match correctly after operators are inserted)
        expression = re.sub(r'\bpi\b', 'PI', expression, flags=re.IGNORECASE)
        expression = re.sub(r'\be\b', 'E', expression, flags=re.IGNORECASE)
        for func in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh', 'log', 'ln', 'sqrt', 'factorial', 'exp']:
            expression = re.sub(rf'\b{func}\b', func, expression, flags=re.IGNORECASE)
        
        return expression

    def _parse_factorials(self, expression: str) -> str:
        """
        Scans backwards from each '!' to convert it to a 'factorial(...)' call.
        """
        while '!' in expression:
            idx = expression.find('!')
            if idx == 0:
                raise InvalidExpressionError("Invalid placement of factorial operator")
            
            start_idx = idx - 1
            # Case 1: Parenthesized operand or function call: e.g., (3+2)! or sin(PI)!
            if expression[start_idx] == ')':
                paren_count = 1
                start_idx -= 1
                while start_idx >= 0 and paren_count > 0:
                    if expression[start_idx] == ')':
                        paren_count += 1
                    elif expression[start_idx] == '(':
                        paren_count -= 1
                     
                    # If we matched the parenthesis, check if there's a function name before it
                    if paren_count == 0:
                        break
                    start_idx -= 1
                
                if paren_count > 0:
                    raise InvalidExpressionError("Mismatched parentheses in factorial")
                
                # Check if it's a function call (e.g. sin(pi)!) by scanning alphanumeric chars before '('
                start_idx -= 1
                while start_idx >= 0 and expression[start_idx].isalnum():
                    start_idx -= 1
                
                operand_start = start_idx + 1
                operand = expression[operand_start:idx]
                expression = expression[:operand_start] + f"factorial({operand})" + expression[idx+1:]
            
            # Case 2: Simple variable, constant, or numeric operand: e.g., 5! or PI!
            else:
                while start_idx >= 0 and (expression[start_idx].isalnum() or expression[start_idx] == '.'):
                    start_idx -= 1
                operand_start = start_idx + 1
                if operand_start == idx:
                    raise InvalidExpressionError("Invalid operand for factorial")
                operand = expression[operand_start:idx]
                expression = expression[:operand_start] + f"factorial({operand})" + expression[idx+1:]
                
        return expression