"""
Evaluates mathematical expressions and returns results.
"""


import ast
import operator
from utils.error_handler import (
    CalculatorError,
    InvalidExpressionError,
    DivisionByZeroError,
    MathOperationError
)


from core.functions import ScientificFunctions
from core.parser import Parser


class Evaluator:
    def __init__(self):
        self.parser = Parser()
        # Map AST operators to functions
        self.operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: self.safe_pow,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos,
        }

    def safe_pow(self, base, exponent):
        if base == 0 and exponent < 0:
            raise DivisionByZeroError("Division by zero")
        
        try:
            # Check for extremely large exponents to avoid hangs
            if abs(exponent) > 1e6:
                raise MathOperationError("Power calculation overflow")
            
            # Check size using logarithmic approximation
            if base != 0:
                import math
                exp_real = exponent.real if isinstance(exponent, complex) else exponent
                if exp_real * math.log10(abs(base)) > 10000:
                    raise MathOperationError("Power calculation overflow")
            
            result = operator.pow(base, exponent)
            return result
        except OverflowError:
            raise MathOperationError("Power calculation overflow")
        except ZeroDivisionError:
            raise DivisionByZeroError("Division by zero")
        except Exception as e:
            if isinstance(e, CalculatorError):
                raise
            raise MathOperationError(str(e))

    def evaluate(self, expression, mode="RAD", variables=None):
        """
        Parses and evaluates the mathematical expression safely.
        """
        if not expression or not isinstance(expression, str):
            raise InvalidExpressionError("Expression must be a non-empty string")
        
        parsed_expression = self.parser.parse(expression)
        
        try:
            node = ast.parse(parsed_expression, mode='eval')
            return self._eval(node.body, mode, variables)
        except SyntaxError:
            raise InvalidExpressionError("Syntax error in expression")
        except ZeroDivisionError:
            raise DivisionByZeroError("Division by zero")
        except RecursionError:
            raise InvalidExpressionError("Expression too deeply nested")
        except CalculatorError:
            raise
        except Exception as e:
            raise InvalidExpressionError(str(e))

    def _eval(self, node, mode, variables=None):
        if isinstance(node, ast.Constant):  # Python 3.8+
            if not isinstance(node.value, (int, float, complex)) or isinstance(node.value, bool):
                raise InvalidExpressionError("Unsupported constant value")
            return node.value
        elif hasattr(ast, 'Num') and isinstance(node, getattr(ast, 'Num')):  # Python < 3.8 fallback
            return node.n
        elif isinstance(node, ast.BinOp):
            left = self._eval(node.left, mode, variables)
            right = self._eval(node.right, mode, variables)
            op_type = type(node.op)
            if op_type not in self.operators:
                raise InvalidExpressionError(f"Unsupported operator: {op_type.__name__}")
            if op_type == ast.Div and right == 0:
                raise DivisionByZeroError("Division by zero")
            try:
                return self.operators[op_type](left, right)
            except ZeroDivisionError:
                raise DivisionByZeroError("Division by zero")
            except Exception as e:
                raise MathOperationError(str(e))
        elif isinstance(node, ast.UnaryOp):
            operand = self._eval(node.operand, mode, variables)
            op_type = type(node.op)
            if op_type not in self.operators:
                raise InvalidExpressionError(f"Unsupported unary operator: {op_type.__name__}")
            return self.operators[op_type](operand)
        elif isinstance(node, ast.Name):
            name = node.id.upper()
            if variables and node.id in variables:
                return variables[node.id]
            if variables and name in variables:
                return variables[name]
            if variables and node.id.lower() in variables:
                return variables[node.id.lower()]
                
            if name == 'PI':
                from utils.constants import PI
                return PI
            elif name == 'E':
                from utils.constants import E
                return E
            raise InvalidExpressionError(f"Unknown variable: {node.id}")
        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise InvalidExpressionError("Invalid function call")
            func_name = node.func.id.lower()
            
            if func_name == 'diff':
                if len(node.args) != 2:
                    raise InvalidExpressionError("Function diff expects exactly 2 arguments: diff(expression, value)")
                expr_node = node.args[0]
                x_val = self._eval(node.args[1], mode, variables)
                if isinstance(x_val, complex):
                    if x_val.imag != 0:
                        raise MathOperationError("Differentiation point must be a real number")
                    x_val = x_val.real
                
                h = 1e-6
                vars_plus = {**(variables or {}), 'x': x_val + h, 'X': x_val + h}
                vars_minus = {**(variables or {}), 'x': x_val - h, 'X': x_val - h}
                
                try:
                    f_plus = self._eval(expr_node, mode, vars_plus)
                    f_minus = self._eval(expr_node, mode, vars_minus)
                    return (f_plus - f_minus) / (2 * h)
                except Exception as e:
                    raise MathOperationError(f"Derivative evaluation error: {str(e)}")
            
            elif func_name == 'integrate':
                if len(node.args) != 3:
                    raise InvalidExpressionError("Function integrate expects exactly 3 arguments: integrate(expression, start, end)")
                expr_node = node.args[0]
                start_val = self._eval(node.args[1], mode, variables)
                end_val = self._eval(node.args[2], mode, variables)
                
                if isinstance(start_val, complex) or isinstance(end_val, complex):
                    if (isinstance(start_val, complex) and start_val.imag != 0) or (isinstance(end_val, complex) and end_val.imag != 0):
                        raise MathOperationError("Integration bounds must be real numbers")
                    start_val = start_val.real if isinstance(start_val, complex) else start_val
                    end_val = end_val.real if isinstance(end_val, complex) else end_val
                
                N = 1000
                h = (end_val - start_val) / N
                
                def f(t):
                    vars_t = {**(variables or {}), 'x': t, 'X': t}
                    return self._eval(expr_node, mode, vars_t)
                
                try:
                    total = f(start_val) + f(end_val)
                    odd_sum = 0.0
                    for i in range(1, N, 2):
                        odd_sum += f(start_val + i * h)
                    even_sum = 0.0
                    for i in range(2, N - 1, 2):
                        even_sum += f(start_val + i * h)
                    
                    result = (h / 3.0) * (total + 4.0 * odd_sum + 2.0 * even_sum)
                    if isinstance(result, complex):
                        if abs(result.imag) < 1e-15:
                            result = result.real
                    return result
                except Exception as e:
                    raise MathOperationError(f"Integration evaluation error: {str(e)}")
            
            # Evaluate arguments
            args = [self._eval(arg, mode, variables) for arg in node.args]
            if len(args) != 1:
                raise InvalidExpressionError(f"Function {func_name} expects exactly 1 argument")
            
            val = args[0]
            try:
                if func_name == 'sin':
                    return ScientificFunctions.sin(val, mode)
                elif func_name == 'cos':
                    return ScientificFunctions.cos(val, mode)
                elif func_name == 'tan':
                    return ScientificFunctions.tan(val, mode)
                elif func_name == 'asin':
                    return ScientificFunctions.asin(val, mode)
                elif func_name == 'acos':
                    return ScientificFunctions.acos(val, mode)
                elif func_name == 'atan':
                    return ScientificFunctions.atan(val, mode)
                elif func_name == 'sinh':
                    return ScientificFunctions.sinh(val)
                elif func_name == 'cosh':
                    return ScientificFunctions.cosh(val)
                elif func_name == 'tanh':
                    return ScientificFunctions.tanh(val)
                elif func_name == 'exp':
                    return ScientificFunctions.exp(val)
                elif func_name == 'log':
                    return ScientificFunctions.log(val)
                elif func_name == 'ln':
                    return ScientificFunctions.ln(val)
                elif func_name == 'sqrt':
                    return ScientificFunctions.sqrt(val)
                elif func_name == 'factorial':
                    return ScientificFunctions.factorial(val)
                else:
                    raise InvalidExpressionError(f"Unknown function: {func_name}")
            except CalculatorError:
                raise
            except Exception as e:
                raise MathOperationError(str(e))
        else:
            raise InvalidExpressionError(f"Unsupported expression structure: {type(node).__name__}")