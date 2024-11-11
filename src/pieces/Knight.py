from src.pieces.Piece import Piece
from src.utils import constants

class Knight(Piece):
    @staticmethod
    def _get_knight_moves(knights: bin, occupied: bin) -> bin:
        """
        Get all potential moves for knights, including only empty squares.
        :param knights: bitboard of knight positions
        :param occupied: bitboard of all occupied squares
        :return: bitboard of possible knight moves
        """
        # Masks to prevent wraparound from file A and file H
        a_file_mask = constants.A_FILE_MASK
        ab_file_mask = constants.AB_FILE_MASK  # For two leftward moves
        h_file_mask = constants.H_FILE_MASK
        gh_file_mask = constants.GH_FILE_MASK  # For two rightward moves

        # Calculate knight moves by shifting the knight's bitboard
        # Eight possible moves for each knight

        # Two up, one left
        moves_up_left = (knights << 15) & ~a_file_mask
        # Two up, one right
        moves_up_right = (knights << 17) & ~h_file_mask
        # One up, two left
        moves_left_up = (knights << 6) & ~ab_file_mask
        # One up, two right
        moves_right_up = (knights << 10) & ~gh_file_mask

        # Two down, one left
        moves_down_left = (knights >> 17) & ~a_file_mask
        # Two down, one right
        moves_down_right = (knights >> 15) & ~h_file_mask
        # One down, two left
        moves_left_down = (knights >> 10) & ~ab_file_mask
        # One down, two right
        moves_right_down = (knights >> 6) & ~gh_file_mask

        # Combine all moves
        all_moves = (moves_up_left | moves_up_right | moves_left_up | moves_right_up |
                     moves_down_left | moves_down_right | moves_left_down | moves_right_down)

        # Mask out occupied squares
        return all_moves & ~occupied

    @classmethod
    def get_possible_moves(cls, knights: bin, occupied: bin) -> bin:
        """
        Get all possible moves for knights.
        :param knights: bitboard of knight positions
        :param occupied: bitboard of all occupied squares
        :return: bitboard of possible moves for knights
        """
        return cls._get_knight_moves(knights, occupied)
