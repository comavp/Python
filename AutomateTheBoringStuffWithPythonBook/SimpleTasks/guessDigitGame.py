import random
import math
import sys

def read_int_value():
    while True:
        try:
            result = int(input())
            break
        except KeyboardInterrupt:
            print('Program was interrupt from keyboard')
            sys.exit()
        except ValueError:
            print('Warning: invalid input, please try again')        
    return result

def get_guess_limit(a, b):
    return int(math.log2(b - a)) + 2

def start_program():
    a = random.randint(0, 99)
    b = random.randint(100, 1000)
    digit = random.randint(a, b)
    attempt_number = get_guess_limit(a, b)
    
    print('I have a random digit between ' + str(a) + ' and ' + str(b))
    while attempt_number:
        print('You have ' + str(attempt_number) + ' attempts')
        guess = read_int_value()
        if guess == digit:
            print('Accepted!')
            break
        elif guess > digit:
            print('Wrong answer: your digit is too big')
        else:
            print('Wrong answer: your digit isn\'t big enought')
        attempt_number -= 1

    if guess != digit:
        print('Game over! You don\'t have any attempts')
        print('(My digit was ' + str(digit) + ')')

start_program()
