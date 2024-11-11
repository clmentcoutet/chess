from src.pieces.Piece import Piece
from src.utils import constants

class Queen(Piece):
    @staticmethod
    def _get_vertical_moves(queen_position: bin, occupied: bin) -> bin:
        """
        Get all vertical moves for the queen.
        :param queen_position:
        :param occupied:
        :return:
        """
        moves = 0
        position = queen_position

        # Move up
        while (position := position << 8) and not (position & occupied):
            moves |= position
        if position & occupied:  # Add the first occupied square
            moves |= position

        position = queen_position

        # Move down
        while (position := position >> 8) and not (position & occupied):
            moves |= position
        if position & occupied:  # Add the first occupied square
            moves |= position

        return moves

    @staticmethod
    def _get_horizontal_moves(queen_position: bin, occupied: bin) -> bin:
        moves = 0
        position = queen_position

        # Move left
        while (position := (position >> 1) & constants.NOT_A_FILE) and not (position & occupied):
            moves |= position
        if position & occupied:
            moves |= position

        position = queen_position

        # Move right
        while (position := (position << 1) & constants.NOT_H_FILE) and not (position & occupied):
            moves |= position
        if position & occupied:
            moves |= position

        return moves

    @staticmethod
    def _get_diagonal_moves(queen_position: bin, occupied: bin) -> bin:
        moves = 0
        position = queen_position

        # Up-left diagonal
        while (position := (position << 7) & constants.NOT_H_FILE) and not (position & occupied):
            moves |= position
        if position & occupied:
            moves |= position

        position = queen_position

        # Up-right diagonal
        while (position := (position << 9) & constants.NOT_A_FILE) and not (position & occupied):
            moves |= position
        if position & occupied:
            moves |= position

        position = queen_position

        # Down-left diagonal
        while (position := (position >> 9) & constants.NOT_H_FILE) and not (position & occupied):
            moves |= position
        if position & occupied:
            moves |= position

        position = queen_position

        # Down-right diagonal
        while (position := (position >> 7) & constants.NOT_A_FILE) and not (position & occupied):
            moves |= position
        if position & occupied:
            moves |= position

        return moves

    @classmethod
    def get_possible_moves(cls, queens: bin, occupied: bin) -> bin:
        """
        Get all possible moves for queens.
        :param queens: bitboard of queen positions
        :param occupied: bitboard of all occupied squares
        :return: bitboard of possible moves for queens
        """
        all_moves = 0
        # Iterate over each queen position in the bitboard
        while queens:
            queen_position = queens & -queens  # Isolate the lowest bit representing a queen
            queens &= queens - 1  # Clear the lowest bit

            # Calculate moves for the isolated queen position
            vertical_moves = cls._get_vertical_moves(queen_position, occupied)
            horizontal_moves = cls._get_horizontal_moves(queen_position, occupied)
            diagonal_moves = cls._get_diagonal_moves(queen_position, occupied)

            # Combine all moves
            all_moves |= vertical_moves | horizontal_moves | diagonal_moves

        return all_moves
