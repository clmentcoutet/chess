from src.pieces.Piece import Piece
from src.utils import constants


class Pawn(Piece):
    @staticmethod
    def _get_simple_push_move(color: bin, pawns: bin, occupied: bin) -> bin:
        """
        Get the simple push move for the pawns
        :param color: color of the pawns, 0 for white, 1 for black
        :param pawns: bitboard of the pawns
        :param occupied: bitboard of all the pieces
        :return:
        """
        if color == 0:
            return (pawns << 8) & ~occupied
        elif color == 1:
            return (pawns >> 8) & ~occupied
        else:
            raise ValueError("color value not valid")

    @staticmethod
    def _get_double_push_move(color: bin, pawns: bin, occupied: bin) -> bin:
        """
        Get the double push move for the pawns
        :param color: color of the pawns, 0 for white, 1 for black
        :param pawns: bitboard of the pawns
        :param occupied: bitboard of all the pieces
        :return:
        """
        second_rank = constants.SECOND_RANK
        seventh_rank = constants.SEVENTH_RANK
        if color == 0:
            return ((pawns & second_rank) << 16) & ~occupied
        elif color == 1:
            return ((pawns & seventh_rank) >> 16) & ~occupied
        else:
            raise ValueError("color value not valid")

    @staticmethod
    def _get_capture_move(color: bin, pawns: bin, pieces: bin) -> bin:
        """
        Get the capture move for the pawns
        :param color: color of the pawns, 0 for white, 1 for black
        :param pawns: bitboard of the pawns
        :param pieces: bitboard of the other color pieces
        :return:
        """
        a_file_mask = constants.A_FILE_MASK
        h_file_mask = constants.H_FILE_MASK
        if color == 0:
            left_capture = (pawns << 7) & pieces & h_file_mask
            right_capture = (pawns << 9) & pieces & a_file_mask
            return left_capture | right_capture
        elif color == 1:
            left_capture = (pawns >> 9) & pieces & h_file_mask
            right_capture = (pawns >> 7) & pieces & a_file_mask
            return left_capture | right_capture
        else:
            raise ValueError("color value not valid")

    @staticmethod
    def _get_en_passant_move(color: bin, pawns: bin, en_passant_square: bin) -> bin:
        """
        Get the en passant move for the pawns
        :param color: color of the pawns, 0 for white, 1 for black
        :param pawns: bitboard of the pawns
        :param en_passant_square: bitboard of the en passant square
        :return:
        """
        if color == 0:
            en_passant_left = (pawns << 7) & en_passant_square
            en_passant_right = (pawns << 9) & en_passant_square
            return en_passant_left | en_passant_right
        elif color == 1:
            en_passant_left = (pawns >> 9) & en_passant_square
            en_passant_right = (pawns >> 7) & en_passant_square
            return en_passant_left | en_passant_right
        else:
            raise ValueError("color value not valid")

    @classmethod
    def get_possibles_moves(
        cls, color: bin, pawns: bin, occupied: bin, pieces: bin, en_passant_square: bin
    ) -> bin:
        """
        Get all the possible moves for the pawns
        :param color: color of the pawns, 0 for white, 1 for black
        :param pawns: bitboard of the pawns
        :param occupied: bitboard of all the pieces
        :param pieces: bitboard of the other color pieces
        :param en_passant_square: bitboard of the en passant square
        :return:
        """
        simple_push = cls._get_simple_push_move(color, pawns, occupied)
        double_push = cls._get_double_push_move(color, pawns, occupied)
        capture = cls._get_capture_move(color, pawns, pieces)
        en_passant = cls._get_en_passant_move(color, pawns, en_passant_square)
        return simple_push | double_push | capture | en_passant
