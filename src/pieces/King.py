from src.pieces.Piece import Piece
from src.utils import constants

class King(Piece):
    @staticmethod
    def _get_king_moves(king_position: bin, occupied: bin) -> bin:
        """
        Get all the possible moves for a king.
        :param king_position: bitboard of the king's position
        :param occupied: bitboard of all occupied squares
        :return: bitboard of all possible moves for the king
        """
        # Define the 8 possible moves for a king (left, right, up, down, and 4 diagonals)
        moves = 0
        position = king_position

        # Move up
        moves |= (position << 8) & ~occupied
        # Move down
        moves |= (position >> 8) & ~occupied
        # Move left
        moves |= (position >> 1) & constants.NOT_A_FILE & ~occupied
        # Move right
        moves |= (position << 1) & constants.NOT_H_FILE & ~occupied
        # Move up-left diagonal
        moves |= (position << 7) & constants.NOT_H_FILE & ~occupied
        # Move up-right diagonal
        moves |= (position << 9) & constants.NOT_A_FILE & ~occupied
        # Move down-left diagonal
        moves |= (position >> 9) & constants.NOT_H_FILE & ~occupied
        # Move down-right diagonal
        moves |= (position >> 7) & constants.NOT_A_FILE & ~occupied

        return moves

    @classmethod
    def get_possible_moves(cls, kings: bin, occupied: bin) -> bin:
        """
        Get all possible moves for kings.
        :param kings: bitboard of king positions
        :param occupied: bitboard of all occupied squares
        :return: bitboard of all possible moves for kings
        """
        all_moves = 0
        # Iterate over each king position in the bitboard
        while kings:
            king_position = kings & -kings  # Isolate the lowest bit representing a king
            kings &= kings - 1  # Clear the lowest bit

            # Calculate moves for the isolated king position
            king_moves = cls._get_king_moves(king_position, occupied)

            # Combine all moves
            all_moves |= king_moves

        return all_moves
