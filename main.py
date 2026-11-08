#PROJECT-Smart Chess Game
import io
import random
import tkinter as tk
from contextlib import redirect_stdout


def sign(number):
    if number > 0:
        return 1
    if number < 0:
        return -1
    return 0


class Piece:
    symbol = ""

    def __init__(self, colour, position, is_live=True):
        self.colour = colour
        self.position = position
        self.is_live = is_live

    def is_valid_move(self, start, end, board):
        return False

    def ends_on_own_piece(self, end, board):
        target = board.get_spot(end[0], end[1]).piece
        if target is not None and target.colour == self.colour:
            return True
        return False

    def is_path_clear(self, start, end, board):
        row_step = sign(end[0] - start[0])
        col_step = sign(end[1] - start[1])
        row = start[0] + row_step
        col = start[1] + col_step

        while (row, col) != end:
            if board.get_spot(row, col).piece is not None:
                return False
            row += row_step
            col += col_step
        return True


class Pawn(Piece):
    symbol = "\u265F"

    def is_valid_move(self, start, end, board):
        if self.colour == "White":
            direction = -1
            start_row = 6
        else:
            direction = 1
            start_row = 1

        row_diff = end[0] - start[0]
        col_diff = abs(end[1] - start[1])
        target = board.get_spot(end[0], end[1]).piece

        if col_diff == 0 and target is None:
            if row_diff == direction:
                return True
            if start[0] == start_row and row_diff == 2 * direction:
                middle_piece = board.get_spot(start[0] + direction, start[1]).piece
                return middle_piece is None
            return False

        if col_diff == 1 and row_diff == direction:
            return target is not None and target.colour != self.colour

        return False


class Rook(Piece):
    symbol = "\u265C"

    def is_valid_move(self, start, end, board):
        if self.ends_on_own_piece(end, board):
            return False
        same_row = start[0] == end[0]
        same_col = start[1] == end[1]
        if not (same_row or same_col):
            return False
        return self.is_path_clear(start, end, board)


class Knight(Piece):
    symbol = "\u265E"

    def is_valid_move(self, start, end, board):
        if self.ends_on_own_piece(end, board):
            return False
        row_diff = abs(end[0] - start[0])
        col_diff = abs(end[1] - start[1])
        return (row_diff, col_diff) in [(2, 1), (1, 2)]


class Bishop(Piece):
    symbol = "\u265D"

    def is_valid_move(self, start, end, board):
        if self.ends_on_own_piece(end, board):
            return False
        row_diff = abs(end[0] - start[0])
        col_diff = abs(end[1] - start[1])
        if row_diff != col_diff:
            return False
        return self.is_path_clear(start, end, board)


class Queen(Piece):
    symbol = "\u265B"

    def is_valid_move(self, start, end, board):
        if self.ends_on_own_piece(end, board):
            return False
        row_diff = abs(end[0] - start[0])
        col_diff = abs(end[1] - start[1])
        straight = row_diff == 0 or col_diff == 0
        diagonal = row_diff == col_diff
        if not (straight or diagonal):
            return False
        return self.is_path_clear(start, end, board)


class King(Piece):
    symbol = "\u265A"

    def is_valid_move(self, start, end, board):
        if self.ends_on_own_piece(end, board):
            return False
        row_diff = abs(end[0] - start[0])
        col_diff = abs(end[1] - start[1])
        return max(row_diff, col_diff) == 1


class Spot:
    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece


class Board:
    def __init__(self):
        self.grid = [[Spot(r, c) for c in range(8)] for r in range(8)]
        self.initialize_board()

    def initialize_board(self):
        for col in range(8):
            self.grid[1][col].piece = Pawn("Black", (1, col))
            self.grid[6][col].piece = Pawn("White", (6, col))

        order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col, piece_class in enumerate(order):
            self.grid[0][col].piece = piece_class("Black", (0, col))
            self.grid[7][col].piece = piece_class("White", (7, col))

    def get_spot(self, row, col):
        return self.grid[row][col]


class Game:
    def __init__(self):
        self.board = Board()
        self.current_turn = "White"
        self.game_status = "ACTIVE"
        self.winner = None

    def player_move(self, start_row, start_col, end_row, end_col):
        start_spot = self.board.get_spot(start_row, start_col)
        end_spot = self.board.get_spot(end_row, end_col)
        piece = start_spot.piece

        if piece is None:
            print("There is no piece here!")
            return False

        if piece.colour != self.current_turn:
            print(f"It is {self.current_turn}'s turn!")
            return False

        if not piece.is_valid_move((start_row, start_col), (end_row, end_col), self.board):
            print("This move is not valid for this piece!")
            return False

        captured_piece = end_spot.piece
        if captured_piece is not None:
            captured_piece.is_live = False
            if isinstance(captured_piece, King):
                self.game_status = "FINISHED"
                self.winner = piece.colour

        end_spot.piece = piece
        piece.position = (end_row, end_col)
        start_spot.piece = None

        if self.current_turn == "White":
            self.current_turn = "Black"
        else:
            self.current_turn = "White"
        return True


class ComputerPlayer:
    def __init__(self, colour):
        self.colour = colour

    def choose_move(self, game):
        all_moves = []
        capture_moves = []

        for row in range(8):
            for col in range(8):
                piece = game.board.grid[row][col].piece
                if piece is None or piece.colour != self.colour:
                    continue

                for end_row in range(8):
                    for end_col in range(8):
                        start = (row, col)
                        end = (end_row, end_col)
                        if piece.is_valid_move(start, end, game.board):
                            all_moves.append((start, end))
                            if game.board.grid[end_row][end_col].piece is not None:
                                capture_moves.append((start, end))

        if capture_moves:
            return random.choice(capture_moves)
        if all_moves:
            return random.choice(all_moves)
        return None


SQUARE = 80
BAR = 50
BOARD_SIZE = SQUARE * 8

LIGHT_SQUARE = "#F0D9B5"
DARK_SQUARE = "#B58863"
SELECTED_SQUARE = "#F6F669"
LAST_MOVE_SQUARE = "#CDD26A"

ACTIVE_BAR = "#8BC34A"
INACTIVE_BAR = "#D0D0D0"


class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess - You vs Computer")
        self.game = Game()
        self.computer = ComputerPlayer("Black")
        self.selected = None
        self.last_move = None
        self.message = ""

        self.canvas = tk.Canvas(root, width=BOARD_SIZE, height=BOARD_SIZE + 2 * BAR,
                                highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

        self.message_label = tk.Label(root, font=("Arial", 13), fg="red", pady=6)
        self.message_label.pack()

        self.draw()

    def draw(self):
        self.canvas.delete("all")
        self.draw_player_bars()
        self.draw_squares()
        self.draw_pieces()
        self.message_label.config(text=self.message)

    def draw_player_bars(self):
        bars = [
            ("Black", 0, 180),
            ("White", BAR + BOARD_SIZE, 0),
        ]
        for colour, top, angle in bars:
            is_active = self.game.game_status == "ACTIVE" and self.game.current_turn == colour
            is_winner = self.game.winner == colour

            if is_active or is_winner:
                bar_colour = ACTIVE_BAR
            else:
                bar_colour = INACTIVE_BAR

            if colour == "Black":
                text = "Black player (computer)"
            else:
                text = "White player (you)"
            if is_active:
                text += "  -  your turn"
            if is_winner:
                text += "  -  WINNER!"

            self.canvas.create_rectangle(0, top, BOARD_SIZE, top + BAR,
                                         fill=bar_colour, outline=bar_colour)
            self.canvas.create_text(BOARD_SIZE // 2, top + BAR // 2, text=text,
                                    angle=angle, font=("Arial", 16, "bold"))

    def draw_squares(self):
        for row in range(8):
            for col in range(8):
                x = col * SQUARE
                y = BAR + row * SQUARE

                if (row + col) % 2 == 0:
                    colour = LIGHT_SQUARE
                else:
                    colour = DARK_SQUARE

                if self.last_move and (row, col) in self.last_move:
                    colour = LAST_MOVE_SQUARE
                if self.selected == (row, col):
                    colour = SELECTED_SQUARE

                self.canvas.create_rectangle(x, y, x + SQUARE, y + SQUARE,
                                             fill=colour, outline=colour)

                if col == 0:
                    self.canvas.create_text(x + 8, y + 10, text=str(8 - row),
                                            fill="#555555", font=("Arial", 9))
                if row == 7:
                    self.canvas.create_text(x + SQUARE - 8, y + SQUARE - 10,
                                            text="abcdefgh"[col],
                                            fill="#555555", font=("Arial", 9))

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.game.board.grid[row][col].piece
                if piece is not None:
                    x = col * SQUARE + SQUARE // 2
                    y = BAR + row * SQUARE + SQUARE // 2
                    self.draw_piece(piece, x, y)

    def draw_piece(self, piece, x, y):
        if piece.colour == "White":
            fill = "white"
            angle = 0
        else:
            fill = "black"
            angle = 180

        font = ("Arial", 44)
        offsets = [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, 2), (-2, 2), (2, -2)]
        for dx, dy in offsets:
            self.canvas.create_text(x + dx, y + dy, text=piece.symbol, font=font,
                                    fill="black", angle=angle)
        self.canvas.create_text(x, y, text=piece.symbol, font=font,
                                fill=fill, angle=angle)

    def on_click(self, event):
        if self.game.game_status != "ACTIVE":
            return
        if self.game.current_turn != "White":
            return

        row = (event.y - BAR) // SQUARE
        col = event.x // SQUARE
        if not (0 <= row < 8 and 0 <= col < 8):
            return

        clicked_piece = self.game.board.grid[row][col].piece
        turn = self.game.current_turn
        self.message = ""

        if self.selected is None:
            if clicked_piece is not None and clicked_piece.colour == turn:
                self.selected = (row, col)
            else:
                self.message = "Select one of your own pieces!"

        elif self.selected == (row, col):
            self.selected = None

        elif clicked_piece is not None and clicked_piece.colour == turn:
            self.selected = (row, col)

        else:
            start_row, start_col = self.selected
            output = io.StringIO()
            with redirect_stdout(output):
                moved = self.game.player_move(start_row, start_col, row, col)

            if moved:
                self.last_move = ((start_row, start_col), (row, col))
                if self.game.winner is not None:
                    self.message = f"{self.game.winner} wins! The King was captured."
                else:
                    self.root.after(700, self.computer_move)
            else:
                self.message = output.getvalue().strip()
            self.selected = None

        self.draw()

    def computer_move(self):
        if self.game.game_status != "ACTIVE":
            return

        move = self.computer.choose_move(self.game)
        if move is None:
            self.message = "Computer has no moves left."
            self.draw()
            return

        start, end = move
        self.game.player_move(start[0], start[1], end[0], end[1])
        self.last_move = (start, end)

        if self.game.winner is not None:
            self.message = f"{self.game.winner} wins! The King was captured."
        self.draw()


if __name__ == "__main__":
    root = tk.Tk()
    ChessGUI(root)
    root.mainloop()