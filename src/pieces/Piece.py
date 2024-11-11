from abc import ABC


class Piece(ABC):
    """
    base class for piece
    """

    @classmethod
    def move_piece(cls, bitboard: bin, square_index: int) -> bin:
        """
        move piece to square_index
        :param bitboard: bin: bitboard of the piece
        :param square_index: int: index of the square to move to
        :return: bin: new bitboard
        """
        return bitboard | (1 << square_index)
