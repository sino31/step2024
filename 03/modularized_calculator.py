#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        # Check for invalid numbers with leading zeros (e.g., '01', '0123')
        if number == 0 and index + 1 < len(line) and line[index + 1].isdigit():
            raise SyntaxError("Leading zeros are not allowed")
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

# read "*"
def read_multiply(line, index):
    token = {'type': 'MULTIPLY'}
    return token, index + 1

# read "/"
def read_devide(line, index):
    token = {'type': 'DEVIDE'}
    return token, index + 1

# read "("
def read_left_parenthesis(line, index):
    token = {'type': 'LEFT_PARENTHESIS'}
    return token, index + 1

# read ")"
def read_right_parenthesis(line, index):
    token = {'type': 'RIGHT_PARENTHESIS'}
    return token, index + 1

# read "abs"
def read_abs(line, index):
    token = {'type': 'ABS'}
    return token, index + 3

# read "int"
def read_int(line, index):
    token = {'type': 'INT'}
    return token, index + 3

# read "round"
def read_round(line, index):
    token = {'type': 'ROUND'}
    return token, index + 5


def handle_negative_numbers(line, tokens, index):
    (next_token, next_index) = read_number(line, index + 1)
    next_token['number'] *= -1
    tokens.append(next_token)
    return next_index

def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            # Skip '+' if it is immediately after another operator (e.g., '+1', '+313')
            if index > 0 and line[index - 1] in '+-*/':
                index += 1
            else:
                (token, index) = read_plus(line, index)
        elif line[index] == '-':
            if index > 0 and line[index - 1] in '+-*/(' and index + 1 < len(line) and line[index + 1].isdigit():
                # Handle negative numbers
                next_index = handle_negative_numbers(line, tokens, index)
                index = next_index
                continue
            else:
                read_minus(line, index)
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_multiply(line, index)
        elif line[index] == '/':
            (token, index) = read_devide(line, index)
        elif line[index] == '(':
            (token, index) = read_left_parenthesis(line, index)
        elif line[index] == ')':
            (token, index) = read_right_parenthesis(line, index)
        elif index + 3 < len(line) and line[index : index + 3] == "abs":
            (token, index) = read_abs(line, index)
        elif index + 3 < len(line) and line[index : index + 3] == "int":
            (token, index) = read_int(line, index)
        elif index + 5 < len(line) and line[index : index + 5] == "round":
            (token, index) = read_round(line, index)
        elif line[index] == ' ': # Skip ' '
            index += 1
            continue
        else:
            raise SyntaxError('Invalid character found: "' + line[index] + '"')
        tokens.append(token)
    return tokens

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

# Check if token has valid parenthesis
def is_valid_parenthesis(tokens):
    left_count = sum(1 for token in tokens if token['type'] == 'LEFT_PARENTHESIS')
    right_count = sum(1 for token in tokens if token['type'] == 'RIGHT_PARENTHESIS')
    return left_count == right_count


def find_the_matching_parenthesis(tokens, index):
    stack = 1 # count a parenthesis
    while index < len(tokens):
        if tokens[index]['type'] == 'LEFT_PARENTHESIS':
            stack += 1
        elif tokens[index]['type'] == 'RIGHT_PARENTHESIS':
            stack -= 1
            if stack == 0: # find the closing parenthesis for current start parenthesis
                return index
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


def evaluate_multiply_and_devide(tokens):
    index = 1
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


def evaluate(tokens):
    tokens.insert(0, {'type': 'PLUS'})          # 1. Insert a dummy '+' token at the beginning
    evaluate_parenthesis(tokens)                # 2. Evaluate inside parenthesis
    evaluate_abs_int_round(tokens)              # 3. Evaluate abs() and int() and round()
    evaluate_multiply_and_devide(tokens)        # 4. Evaluate '*' and '/' operations first, and update tokens
    answer = evaluate_plus_and_minus(tokens)    # 5. Evaluate "+" and "-" operations
    return answer


def test(line):
    try:
        tokens = tokenize(line)
        actual_answer = evaluate(tokens)
        expected_answer = eval(line)
        if abs(actual_answer - expected_answer) < 1e-8:
            print("PASS! ('%s' = %f)" % (line, expected_answer))
        else:
            print_fail("FAIL! ('%s' should be %f but was %f)" % (line, expected_answer, actual_answer))
    except Exception as e:
        print_error("Error ('%s' raised an exception: %s)" % (line, str(e)))


def print_fail(message):
    RED = "\033[91m"
    RESET = "\033[0m"
    print(f"{RED}{message}{RESET}")

def print_error(message):
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    print(f"{YELLOW}{message}{RESET}")


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    # tests with only + or -
    test("1+2")
    test("1.0+2.1-3")

    # tests with +, -, *, /
    test("3.0+4*2-1/5")
    test("2-3.0*4*2-1/5")
    test("1+4.0*4.0*4.0*3*2")

    # tests division by 0
    test("1+4+7/0")

    # tests division of 0
    test("0/1-3")

    # tests with invalid character
    test("1>8")

    # tests with negative values
    test("2*-3")
    test("-2-3")
    test("2--2")

    # tests +1 as a number
    test("2-+3")

    # tests with large integers
    test("1234567890*987654321")

    # tests number starting with 0
    test("1*01")

    # tests with parenthesis
    test("(3.0+4*(2-1))/5")
    test("(3.0+4*(2-1))/5)")
    test("(-2-2)*2")

    # test with abs,int,round
    test("12+abs(-12)")
    test("12+int(2.6)")
    test("12+round(2.6)")
    test("12+abs(int(round(-1.55)+abs(int(-2.3+4))))")

    # test with " "
    test("12 + abs(int(round(-1.55) + abs(int(-2.3 + 4))))")
    test("       1         + 1           +                         1      ")

    print("==== Test finished! ====\n")

run_test()

# while True:
#     print('> ', end="")
#     line = input()
#     tokens = tokenize(line)
#     try:
#         answer = evaluate(tokens)
#         print("answer = %f\n" % answer)
#     except Exception as e:
#         print("Error: %s\n" % str(e))

