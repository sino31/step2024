#! /usr/bin/python3
from tokenizer import tokenize
from evaluator import evaluate
from utils import print_fail, print_error

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
    test("2*+4")
    test("2*++4")
    test("+++++++2+3")
    test("2*+-3")

    # tests with large integers
    test("1234567890*987654321")

    # tests number starting with 0
    test("1*01")

    # tests with parenthesis
    test("(3.0+4*(2-1))/5")
    test("(3.0+4*(2-1))/5)")
    test("(-2-2)*2")
    test("2*(*2)")

    # test with abs,int,round
    test("12+abs(-12)")
    test("12+int(2.6)")
    test("12+round(2.6)")
    test("12+abs(int(round(-1.55)+abs(int(-2.3+4))))")

    # test with " "
    test("12 + abs(int(round(-1.55) + abs(int(-2.3 + 4))))")
    test("       1         + 1           +                         1      ")

    print("==== Test finished! ====\n")


if __name__ == "__main__":
    run_test()

    line = ""
    while line != "q":
        print('> ', end="")
        line = input()
        if line == "q":  # Exit the loop if 'q' is entered
            break
        tokens = tokenize(line)
        try:
            answer = evaluate(tokens)
            print("answer = %f\n" % answer)
        except Exception as e:
            print("Error: %s\n" % str(e))