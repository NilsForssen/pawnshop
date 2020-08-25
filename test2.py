from string import ascii_lowercase

def func(dec, base):
    print("dec: ", dec)
    indexList = []

    if dec / base > 1:
        indexList.append(int(dec / base) - 1)
        indexList.extend(func(dec % base, base))

    elif (dec / base) == 1:
        indexList.append(int(dec / base) - 1)
        indexList.extend(func(int(dec / base) - 1, base))

    else:
        indexList.append((dec % base))

    return indexList


def conv2Alpha(dec, base):
    if base > 26:
        raise ValueError("Base cannot be larger 25, the number of characters in the English alphabet")

    # def func(dec, base):
    #     indexList = []

    #     this = dec / base

    #     if this >= base:
    #         base *= base
    #         indexList.extend(func(dec), base)

    #     elif this > 1:
    #         indexList.append(int(this) - 1)
    #         indexList.extend(func(dec % base))

    #     elif this == 1:
    #         indexList.append(int(this) - 1)
    #         indexList.extend(func(int(this) - 1))

    #     else:
    #         indexList.append((dec % base))

    #     return indexList

    indexList = func(dec, base)

    return "".join([ascii_lowercase[i] for i in indexList])


def countAlpha():
    stringList = [0]
    num = 0
    
    while True:

        yield (num, "".join([ascii_lowercase[num] for num in stringList]))
        i = 1
        num += 1 

        while True:

            if i > len(stringList):
                stringList.insert(0,0)
                break
            else:
                charToChange2 = stringList[-i] + 1

            if charToChange2 >= len(ascii_lowercase):
                stringList[-i::] = [0]*(i)
                i += 1 
                continue
            else:

                stringList[-i] = charToChange2
                break




def test(dec, base):
    base += 1
    letters = 'a' + ascii_lowercase
    dec += 1
    indexList = []

    while dec:
        indexList.append(dec % base)
        dec = int(dec / base)

    indexList.reverse()

    return [('a' + ascii_lowercase)[i] for i in indexList if i % 10 != 0]


print(test(27,26))


# if __name__ == "__main__":
#     generator = countAlpha()
#     for i in range(10000):
#         print(conv2Alpha(i, 26))
#         print(next(generator))
#     # for i in countAlpha():
#     #     print(i)



