def is_int(number):
    try:
        int(number)
        return True
    except ValueError:
        return False

msg = input('enter a number: ')

if is_int(msg):
    print('this is a number')
else:
    print('not a valid number')