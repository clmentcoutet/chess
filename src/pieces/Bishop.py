from src.pieces.Piece import Piece
from src.utils import constants

class Bishop(Piece):
    @staticmethod
    def _get_bishop_moves(bishop_position: bin, occupied: bin) -> bin:
        """
        Get all the possible moves for a bishop.
        :param bishop_position: bitboard of the bishop's position
        :param occupied: bitboard of all occupied squares
        :return: bitboard of all possible moves for the bishop
        """
        # Define the diagonal directions
        moves = 0
        position = bishop_position

        # Move diagonally up-left (top-left)
        up_left = position
        while up_left:
            up_left = (up_left << 7) & ~occupied  # Move up-left
            moves |= up_left

        # Move diagonally up-right (top-right)
        up_right = position
        while up_right:
            up_right = (up_right << 9) & ~occupied  # Move up-right
            moves |= up_right

        # Move diagonally down-left (bottom-left)
        down_left = position
        while down_left:
            down_left = (down_left >> 9) & ~occupied  # Move down-left
            moves |= down_left

        # Move diagonally down-right (bottom-right)
        down_right = position
        while down_right:
            down_right = (down_right >> 7) & ~occupied  # Move down-right
            moves |= down_right

        return moves

    @classmethod
    def get_possible_moves(cls, bishops: bin, occupied: bin) -> bin:
        """
        Get all possible moves for bishops.
        :param bishops: bitboard of bishop positions
        :param occupied: bitboard of all occupied squares
        :return: bitboard of all possible moves for bishops
        """
        all_moves = 0
        # Iterate over each bishop position in the bitboard
        while bishops:
            bishop_position = bishops & -bishops  # Isolate the lowest bit representing a bishop
            bishops &= bishops - 1  # Clear the lowest bit

            # Calculate moves for the isolated bishop position
            bishop_moves = cls._get_bishop_moves(bishop_position, occupied)

            # Combine all moves
            all_moves |= bishop_moves

        return all_moves
