import chess

# rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPB/RNBQQBBR w kq - 0 1


def filename_to_fen(filename):
    board_part = filename.split('.')[0].replace('-', '/')
    full_fen = f"{board_part} w KQkq - 0 1"
    try:
        board = chess.Board(full_fen)
        return board.fen()
    except ValueError as e:
        print(f"Error creating board from FEN: {e}")
        return None


def fen_to_filename(fen):
    board_part = fen.split(' ')[0]
    filename_part = board_part.replace('/', '-')
    filename = f"{filename_part}.jpeg"
    return filename


def fen_to_all_white_pawns(fen):
    board = chess.Board(fen)
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            board.set_piece_at(square, chess.Piece(chess.PAWN, chess.WHITE))
    return board.fen()
