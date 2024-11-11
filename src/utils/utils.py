def move_to_index(move: str) -> int:
    """
    Convert a move string to a square index
    :param move: str: move string in algebraic notation
    :return: int: square index
    """
    return (ord(move[0]) - ord("a")) + (int(move[1]) - 1) * 8


def index_to_move(index: int) -> str:
    """
    Convert a square index to a move string
    :param index: int: square index
    :return: str: move string in algebraic notation
    """
    return chr(index % 8 + ord("a")) + str(index // 8 + 1)
