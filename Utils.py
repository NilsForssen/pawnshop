from Exceptions import DisabledError
from string import ascii_lowercase

def _catchOutofBounce(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return False
    return wrapper


def _positivePos(func):
    def wrapper(pInstance, pos, bInstance):

        if not pos[0] < 0 and not pos[1] < 0:
            return func(pInstance, pos, bInstance)
        else:
            return False
    return wrapper


def infiRange(start, stop=None, step=1):
    i = start
    while True:
        if stop and stop == i:
            break
        yield i
        i += step


def convPosition(func):
    def wrapper(instance, *args, **kwargs):
        if isinstance(pos, string):
            func(pos)

            
def toNotation(pos, board):
    notation = ""

    notation += board._rows - pos[0]

    notation += conv2Alpha(pos[1])

    return notation


def conv2Alpha(num):
    for n, notation in countAlpha():
        if num == n:
            return notation


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
