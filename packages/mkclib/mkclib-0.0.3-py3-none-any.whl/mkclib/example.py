def add_one(number):
    return number + 1
    
def check_prime(no):
    is_prime = True
    for i in range(2, no):
        if no % i == 0:
            is_prime = False
            break
    return is_prime
    
def calc_BMI(h, w):
    BMI = w / (h/100) ** 2
    # print(f'BMI={round(BMI, 2)}')

    BMI_message = ''
    if BMI < 18.5:
        BMI_message = '體重過輕'
    elif BMI < 24:
        BMI_message = '正常'
    else:
        BMI_message = '過重'
        
    return round(BMI, 2), BMI_message
    
def print_9x9_table(row, col):
    for i in range(1, row+1):
        for j in range(1, col+1):
            print(f'{i}x{j}={i*j}', end='\t')
        print()        