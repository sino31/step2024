# for evaluate_parenthesis func
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

# for test func
def print_fail(message):
    RED = "\033[91m"
    RESET = "\033[0m"
    print(f"{RED}{message}{RESET}")

def print_error(message):
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    print(f"{YELLOW}{message}{RESET}")