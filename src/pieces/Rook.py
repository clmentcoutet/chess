from src.pieces.Piece import Piece
from src.utils import constants

class Rook(Piece):
    @staticmethod
    def _get_rook_moves(rook_position: bin, occupied: bin) -> bin:
        """
        Get all the possible moves for a rook.
        :param rook_position: bitboard of the rook's position
        :param occupied: bitboard of all occupied squares
        :return: bitboard of all possible moves for the rook
        """
        # Define the horizontal and vertical directions
        moves = 0
        position = rook_position

        # Move up (vertical)
        up = position
        while up:
            up = (up << 8) & ~occupied  # Move up
            moves |= up

        # Move down (vertical)
        down = position
        while down:
            down = (down >> 8) & ~occupied  # Move down
            moves |= down

        # Move left (horizontal)
        left = position
        while left:
            left = (left >> 1) & constants.NOT_A_FILE & ~occupied  # Move left
            moves |= left

        # Move right (horizontal)
        right = position
        while right:
            right = (right << 1) & constants.NOT_H_FILE & ~occupied  # Move right
            moves |= right

        return moves

    @classmethod
    def get_possible_moves(cls, rooks: bin, occupied: bin) -> bin:
        """
        Get all possible moves for rooks.
        :param rooks: bitboard of rook positions
        :param occupied: bitboard of all occupied squares
        :return: bitboard of all possible moves for rooks
        """
        all_moves = 0
        # Iterate over each rook position in the bitboard
        while rooks:
            rook_position = rooks & -rooks  # Isolate the lowest bit representing a rook
            rooks &= rooks - 1  # Clear the lowest bit

            # Calculate moves for the isolated rook position
            rook_moves = cls._get_rook_moves(rook_position, occupied)

            # Combine all moves
            all_moves |= rook_moves

        return all_moves
