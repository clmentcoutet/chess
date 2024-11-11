import tkinter as tk
from PIL import Image, ImageTk
import os
import cairosvg
import io

from src import config
from src.game.Game import Game
from src.utils import constants


class ChessGUI:
    def __init__(self, master, game: Game):
        self.master = master
        self.game = game
        self.square_size = 100
        self.board_size = self.square_size * 8

        # Create main canvas
        self.canvas = tk.Canvas(
            master,
            width=self.board_size,
            height=self.board_size
        )
        self.canvas.pack()

        # Initialize piece images
        self.piece_images = {}
        self.load_piece_images()

        # Draw initial board
        self.draw_board()
        self.draw_pieces()

    def load_piece_images(self):
        """Load chess piece SVG images from src/assets/pieces folder"""
        piece_chars = {
            constants.WHITE_PAWN: 'pawn-w.svg',
            constants.WHITE_KNIGHT: 'knight-w.svg',
            constants.WHITE_BISHOP: 'bishop-w.svg',
            constants.WHITE_ROOK: 'rook-w.svg',
            constants.WHITE_QUEEN: 'queen-w.svg',
            constants.WHITE_KING: 'king-w.svg',
            constants.BLACK_PAWN: 'pawn-b.svg',
            constants.BLACK_KNIGHT: 'knight-b.svg',
            constants.BLACK_BISHOP: 'bishop-b.svg',
            constants.BLACK_ROOK: 'rook-b.svg',
            constants.BLACK_QUEEN: 'queen-b.svg',
            constants.BLACK_KING: 'king-b.svg',
        }

        # Get the absolute path to the project root
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        assets_path = str(os.path.join(current_dir, config.PIECE_ASSET_PATH))

        for piece, filename in piece_chars.items():
            # Load and resize image
            image_path = os.path.join(assets_path, filename)
            try:
                # Convert SVG to PNG in memory with the desired size
                png_data = cairosvg.svg2png(
                    url=image_path,
                    output_width=self.square_size - 10,
                    output_height=self.square_size - 10
                )

                # Convert PNG data to PIL Image
                img = Image.open(io.BytesIO(png_data))

                # Convert to PhotoImage for Tkinter
                self.piece_images[piece] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error loading {filename}: {e}")
                # Fallback to text if image loading fails
                self.piece_images[piece] = None

    def draw_board(self):
        """Draw the chess board squares"""
        for row in range(8):
            for col in range(8):
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size

                # Alternate square colors
                color = "#F0D9B5" if (row + col) % 2 == 0 else "#B58863"

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline=""
                )

    def draw_pieces(self):
        """Draw pieces based on bitboard positions"""
        # Clear existing pieces
        self.canvas.delete("piece")

        def get_set_bits(bitboard: bin):
            positions = []
            for i in range(64):
                if bitboard & (1 << i):
                    positions.append(i)
            return positions

        # Map bitboards to piece characters
        piece_mappings = [
            (self.game.white_pawns, constants.WHITE_PAWN),
            (self.game.white_knights, constants.WHITE_KNIGHT),
            (self.game.white_bishops, constants.WHITE_BISHOP),
            (self.game.white_rooks, constants.WHITE_ROOK),
            (self.game.white_queens, constants.WHITE_QUEEN),
            (self.game.white_king, constants.WHITE_KING),
            (self.game.black_pawns, constants.BLACK_PAWN),
            (self.game.black_knights, constants.BLACK_KNIGHT),
            (self.game.black_bishops, constants.BLACK_BISHOP),
            (self.game.black_rooks, constants.BLACK_ROOK),
            (self.game.black_queens, constants.BLACK_QUEEN),
            (self.game.black_king, constants.BLACK_KING),
        ]

        for bitboard, piece_char in piece_mappings:
            positions = get_set_bits(bitboard)
            for pos in positions:
                row = 7 - (pos // 8)  # Flip row for correct orientation
                col = pos % 8
                x = col * self.square_size + self.square_size // 2
                y = row * self.square_size + self.square_size // 2

                if self.piece_images[piece_char]:
                    # Calculate position to center the image
                    img = self.piece_images[piece_char]
                    img_x = x - img.width() // 2
                    img_y = y - img.height() // 2
                    self.canvas.create_image(
                        img_x, img_y,
                        image=img,
                        anchor='nw',
                        tags="piece"
                    )
                else:
                    # Fallback to Unicode characters if image loading fails
                    self.canvas.create_text(
                        x, y,
                        text=piece_char,
                        font=("Arial", 36),
                        fill="black" if piece_char.isupper() else "dark gray",
                        tags="piece"
                    )

    def update_display(self):
        """Update the board display"""
        self.draw_pieces()


def create_chess_gui(game: Game):
    root = tk.Tk()
    root.title("Chess Board")
    gui = ChessGUI(root, game)
    return root, gui

if __name__ == "__main__":
    game = Game(fen=config.BASE_FEN)
    root, gui = create_chess_gui(game)

    root.mainloop()