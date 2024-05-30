# Handle negative numbers input
def handle_negative_numbers(line, tokens, index):
    (next_token, next_index) = read_number(line, index + 1)
    next_token['number'] *= -1
    tokens.append(next_token)
    return next_index

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



def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            # Skip '+' if it is immediately after another operator (e.g., '+1', '++313')
            if index > 0 and line[index - 1] in '+-*/':
                index += 1
                continue
            else:
                (token, index) = read_plus(line, index)
        elif line[index] == '-':
            # Handle negative numbers
            if index > 0 and line[index - 1] in '+-*/(' and index + 1 < len(line) and line[index + 1].isdigit():
                next_index = handle_negative_numbers(line, tokens, index)
                index = next_index
                continue
            else:
                read_minus(line, index)
            (token, index) = read_minus(line, index)
        elif line[index] == '*' and index > 0 and line[index - 1] not in '+-*/(':
            (token, index) = read_multiply(line, index)
        elif line[index] == '/' and index > 0 and line[index - 1] not in '+-*/(':
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