class IllegalMove(Exception):
    """Move is ilegal"""
    pass


class Check(IllegalMove):
    pass


class CheckMate(IllegalMove):
    pass


class EmptyError(IndexError):
    pass


class DisabledError(IndexError):
    pass


class UnsuccessfulTest(Exception):
	pass