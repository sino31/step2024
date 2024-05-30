from utils import is_valid_parenthesis, find_the_matching_parenthesis

def evaluate_plus_and_minus(tokens):
    answer = 0
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                raise SyntaxError("Invalid syntax")
        index += 1
    return answer

def evaluate_multiply_and_devide(tokens):
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS' or tokens[index - 1]['type'] == 'MINUS':
                index += 1
                continue
            elif tokens[index - 1]['type'] == 'MULTIPLY':
                result = tokens[index - 2]['number'] * tokens[index]['number']
            elif tokens[index - 1]['type'] == 'DEVIDE':
                if tokens[index]['type'] == 0:
                    raise ZeroDivisionError("division by zero")
                result = tokens[index - 2]['number'] / tokens[index]['number']
            else:
                raise SyntaxError("Invalid syntax")
            tokens[index - 2] = {'type': 'NUMBER', 'number': result}
            del tokens[index - 1 : index + 1]
            index -= 1
        index += 1

# Evaluate inside parentheses recursively.
def evaluate_parenthesis(tokens):
    index = 0
    if not is_valid_parenthesis(tokens):
        raise SyntaxError("Unbalanced parentheses")
    while index < len(tokens):
        if tokens[index]['type'] == 'LEFT_PARENTHESIS':
            closing_index = find_the_matching_parenthesis(tokens, index + 1) # Find the index of the matching closing parenthesis.
            parenthesis_tokens = tokens[index + 1 : closing_index] # Extract the tokens within the parentheses.
            answer = evaluate(parenthesis_tokens) # Recursively evaluate the expression inside the parentheses.
            # Replace the entire parenthesis expression with the evaluated result.
            tokens[index] = {'type': 'NUMBER', 'number': answer}
            del tokens[index + 1 : closing_index + 1]
        index += 1

# Evaluate abs() and int() and round()
def evaluate_abs_int_round(tokens):
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'ABS':
                answer = abs(tokens[index]['number'])
            elif tokens[index - 1]['type'] == 'INT':
                answer = int(tokens[index]['number'])
            elif tokens[index - 1]['type'] == 'ROUND':
                answer = round(tokens[index]['number'])
            else:
                index += 1
                continue
            tokens[index - 1] = {'type': 'NUMBER', 'number': answer}
            del tokens[index]
        index += 1



def evaluate(tokens):
    tokens.insert(0, {'type': 'PLUS'})          # 1. Insert a dummy '+' token at the beginning
    evaluate_parenthesis(tokens)                # 2. Evaluate inside parenthesis
    evaluate_abs_int_round(tokens)              # 3. Evaluate abs() and int() and round()
    evaluate_multiply_and_devide(tokens)        # 4. Evaluate '*' and '/' operations first, and update tokens
    answer = evaluate_plus_and_minus(tokens)    # 5. Evaluate "+" and "-" operations
    return answer