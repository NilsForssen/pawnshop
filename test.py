from string import ascii_lowercase 


def int2base(x, base):
    if x < 0:
        sign = -1
    elif x == 0:
        return ascii_lowercase[0]
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(int(x % base))
        x = int(x / base)

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return [ascii_lowercase[digit-1] for  digit in digits]

mynum = 678
for num in range(100):
    print(int2base(num,26))
