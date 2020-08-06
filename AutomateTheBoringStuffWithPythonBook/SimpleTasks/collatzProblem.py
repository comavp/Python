def collatz(number):
    if number % 2:
        number = 3 * number + 1
    else:
        number = number // 2
    print(number)
    return number

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

print('Enter one digit:')
number = int(input())
while number != 1:
    number = collatz(number)
    
