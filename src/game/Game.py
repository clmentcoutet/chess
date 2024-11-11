from src.utils import constants
from src.utils.utils import move_to_index


class Game:
    def __init__(self, *, fen: str = None):
        self.white_pawns: bin = 0
        self.white_knights: bin = 0
        self.white_bishops: bin = 0
        self.white_rooks: bin = 0
        self.white_queens: bin = 0
        self.white_king: bin = 0
        self.white_pieces: bin = 0

        self.black_pawns: bin = 0
        self.black_knights: bin = 0
        self.black_bishops: bin = 0
        self.black_rooks: bin = 0
        self.black_queens: bin = 0
        self.black_king: bin = 0
        self.black_pieces: bin = 0

        self.turn: bin = 0  # 0 for white, 1 for black
        self.castling_rights: bin = 0  # 4 bits for each castling right (KQkq)
        self.en_passant_square: bin = 0  # 8 bits for each square (a3, b6, etc.)
        self.halfmove_clock: int = (
            0  # Number of halfmoves since the last capture or pawn advance
        )
        self.fullmove_number: int = 1  # Starts at 1, incremented after black's move

        if fen:
            self._fen_to_bitboard(fen)

    def set_castle_rights(self, castle: str) -> None:
        if castle == "-":
            return  # No castling rights
        castle_map = {
            constants.WHITE_KING: 1 << 3,
            constants.WHITE_QUEEN: 1 << 2,
            constants.BLACK_KING: 1 << 1,
            constants.BLACK_QUEEN: 1 << 0,
        }
        for char in castle:
            self.castling_rights |= castle_map.get(char, 0)

    def set_turn(self, turn: str) -> None:
        if turn == constants.WHITE:
            self.turn = 0
        elif turn == constants.BLACK:
            self.turn = 1
        else:
            raise ValueError("turn value not valid for FEN position")

    def set_en_passant(self, move: str) -> None:
        if move == "-":
            return
        # Convert move to square index
        self.en_passant_square = 1 << move_to_index(move)

    def incr_halfmove(self) -> None:
        self.halfmove_clock += 1

    def incr_fullmove(self) -> None:
        self.fullmove_number += 1

    def _fen_to_bitboard(self, fen: str):
        # Split the FEN string into board layout and other data
        split_fen = fen.split()
        board_layout = split_fen[0]
        turn = split_fen[1]
        castle_rights = split_fen[2]
        en_passant = split_fen[3]

        self.set_turn(turn)
        self.set_castle_rights(castle_rights)
        self.set_en_passant(en_passant)

        square_index = 63  # Start from the top-left corner (a8)

        # Map FEN symbols to corresponding piece bitboards
        piece_to_bitboard = {
            constants.WHITE_PAWN: "white_pawns",
            constants.WHITE_KNIGHT: "white_knights",
            constants.WHITE_BISHOP: "white_bishops",
            constants.WHITE_ROOK: "white_rooks",
            constants.WHITE_QUEEN: "white_queens",
            constants.WHITE_KING: "white_king",
            constants.BLACK_PAWN: "black_pawns",
            constants.BLACK_KNIGHT: "black_knights",
            constants.BLACK_BISHOP: "black_bishops",
            constants.BLACK_ROOK: "black_rooks",
            constants.BLACK_QUEEN: "black_queens",
            constants.BLACK_KING: "black_king",
        }

        # Loop through each character in the board layout section of FEN
        for char in board_layout:
            if char.isdigit():  # Skip empty squares
                square_index -= int(
                    char
                )  # Move to the next filled square or end of rank
            elif char == "/":  # Move to the next rank
                continue
            else:  # Place a piece on the board
                # Set the bit for the piece on the corresponding bitboard
                bitboard_name = piece_to_bitboard.get(char)
                if bitboard_name:
                    setattr(
                        self,
                        bitboard_name,
                        getattr(self, bitboard_name) | (1 << square_index),
                    )
                square_index -= 1  # Move to the next square

    def display_bitboards(self):
        # Helper to visualize each bitboard
        for attr, value in self.__dict__.items():
            if isinstance(value, int):
                print(f"{attr}: {value:064b}")


if __name__ == "__main__":
    game = Game(fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    game.display_bitboards()
