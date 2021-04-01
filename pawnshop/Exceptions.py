# Exceptions.py

class Illegal(Exception):
    """Move is ilegal"""
    pass


class IllegalMove(Illegal):
    def __init__(self, startPos, targetPos,
                 msg="Piece at {0} cannot move to {1}!"):
        super().__init__(msg.format(startPos, targetPos))


class CheckMate(Illegal):
    def __init__(self, msg="Your king is in checkmate!"):
        super().__init__(msg)


class EmptyError(IndexError):
    def __init__(self, position, msg="Position {0} is empty!"):
        super().__init__(msg.format(position))


class DisabledError(IndexError):
    def __init__(self, position, msg="Position {0} is out of bounce!"):
        super().__init__(msg.format(position))


class PromotionError(Exception):
    def __init__(self, msg="Moved piece needs to be promoted!"):
        super().__init__(msg)


class TurnError(Exception):
    def __init__(self, msg="Wrong player!"):
        super().__init__(msg)


if __name__ == "__main__":

    # Do some testing
    pass
