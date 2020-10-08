class Illegal(Exception):
    """Move is ilegal"""
    pass

class IllegalMove(Exception):
    def __init__(self, startPos, targetPos, msg="Piece at {0} cannot move to {1}!"):
        super().__init__(msg.format(startPos, targetPos))

class Check(Illegal):
    def __init__(self, startPos, targetPos, msg="Cannot move piece at {0} to {1} since your king is in check!"):
        super().__init__(msg.format(startPos, targetPos))

class CheckMate(Illegal):
    def __init__(self, color, msg="{0} Checkmated!"):
        super().__init__(msg.format(color))

class EmptyError(IndexError):
    def __init__(self, position, msg="Position {0} is empty!"):
        super().__init__(msg.format(position))

class DisabledError(IndexError):
    def __init__(self, position, msg="Position {0} is out of bounce!"):
        super().__init__(msg.format(position))

class PromotionError(Exception):
    def __init__(self, targetPos, msg="Piece moved to {0} was needs to be promoted!"):
        super().__init__(msg.format(position))

class UnsuccessfulTest(Exception):
	pass
