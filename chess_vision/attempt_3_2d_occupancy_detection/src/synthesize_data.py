import chess
import chess.svg
import cairosvg
from PIL import Image
import io


def generate_chess_images(num_images):
    for i in range(num_images):
        board = chess.Board()
        # Ensure we have enough legal moves
        num_moves = min(10, len(list(board.legal_moves)))

        for _ in range(i % num_moves + 1):  # Make moves
            move = list(board.legal_moves)[0]  # Choose the first legal move
            board.push(move)

        # Generate the modified FEN filename
        # Get only the piece placement part of the FEN
        fen = board.fen().split(" ")[0]
        # Replace slashes with dashes for the filename
        filename = fen.replace("/", "-") + ".jpeg"

        # Convert the SVG to a JPEG image
        svg = chess.svg.board(board=board)
        png = cairosvg.svg2png(bytestring=svg.encode("utf-8"))
        image = Image.open(io.BytesIO(png))

        # Save the image with the modified FEN as the filename
        image.save(filename)


# Example: Generate and save 5 chessboard images with FEN-named files
generate_chess_images(5)
