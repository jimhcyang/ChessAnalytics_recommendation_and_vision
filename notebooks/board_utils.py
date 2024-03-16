from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from tqdm import tqdm
from sklearn.preprocessing import normalize
from scipy.sparse import csr_matrix, vstack
from scipy.spatial.distance import cdist
import numpy as np
import pandas as pd
import io
import chess
import chess.pgn
import chess.svg
import os
import re

def games_from_drive():
    max_games = 500000 
    asset_dir = 'asset'
    file_name = '2023_tc_500000_games.pgn'

    gauth = GoogleAuth()
    gauth.DEFAULT_SETTINGS['client_config_file'] = 'client_secret_1057507276332-5mk9ac9q22rsmtm1idlqvpraq08ar8p5.apps.googleusercontent.com.json'
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile("mycreds.txt")
    drive = GoogleDrive(gauth)

    def load_pgns_from_text(pgns_text, num_games=None, start_index=0, encoding="utf-8"):
        games = []
        file_io = io.StringIO(pgns_text)
        for _ in tqdm(range(start_index), desc='Skipping games', unit='game', leave=False):
            game = chess.pgn.read_game(file_io)
            if game is None:
                break
        for _ in tqdm(range(num_games), desc='Loading games', unit='game', leave=True) if num_games else iter(int, 1):
            game = chess.pgn.read_game(file_io)
            if game is None:
                break
            games.append(game)
        return games

    def find_folder_id(folder_name):
        file_list = drive.ListFile({'q': f"title='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
        for file in file_list:
            if file['title'] == folder_name:
                return file['id']
        return None

    def read_pgn_file_from_drive(file_title, parent_id):
        query = f"'{parent_id}' in parents and trashed=false and title='{file_title}'"
        file_list = drive.ListFile({'q': query}).GetList()
        if not file_list:
            print(f"No file found with title: {file_title}")
            return None
        file = file_list[0]
        urls = file.GetContentString(encoding='UTF-8')
        return urls

    chess_games_loaded = False
    print("loading pgn...")
    asset_folder_id = find_folder_id(asset_dir)

    if asset_folder_id is None:
        print("Asset folder not found.")
    else:
        pgns_text = read_pgn_file_from_drive(file_name, asset_folder_id)
        games = load_pgns_from_text(pgns_text, num_games=max_games)
        if games is not None:
            print("pgn file loaded successfully.")
    return games

def load_pgns(file_path, num_games=None, start_index=0, encoding="utf-8"):
    games = []
    with open(file_path, "r", encoding=encoding) as file:
        for _ in tqdm(range(start_index), desc='Skipping games', unit='game', leave=False):
            game = chess.pgn.read_game(file)
            if game is None:
                break
        for _ in tqdm(range(num_games), desc='Loading games', unit='game', leave=True) if num_games else iter(int, 1):
            game = chess.pgn.read_game(file)
            if game is None:
                break
            games.append(game)
    return games

def game_to_csr_matrix(game, csr=True):
    board = game.board()
    fen_array_list = []
    turn = chess.WHITE
    for move in game.mainline_moves():
        board.push(move)
        turn = not turn
        fen_array = board_to_array(board)
        orient_array = orient_board(fen_array, turn)
        fen_array_list.append(orient_array)
    if csr:
        game_csr_matrix = csr_matrix(np.array(fen_array_list))
        return game_csr_matrix
    else:
        return np.array(fen_array_list)

def povscore_to_int(eval, turn):
    eval = str(eval)
    if eval[0] != '#':
        evaluation = float(eval)
    else:
        if eval[1] != '-':
            evaluation = 10
        else:
            evaluation = -10
    return evaluation*(-1)**(not turn)

def get_eval_from_result(result):
    if result == '1-0':
        return 10
    elif result == '0-1':
        return -10
    else:
        return 0
    
def game_and_eval_to_csr_matrix(game):
    result = game.headers['Result']
    board = game.board()
    fen_array_list = []
    evals_list = []
    turn = chess.WHITE

    for node in game.mainline():
        move = node.move
        board.push(move)
        turn = not turn
        fen_array = board_to_array(board)
        orient_array = orient_board(fen_array, turn)
        fen_array_list.append(orient_array)

        comment = node.comment
        eval_match = re.search(r"\[%eval (.*?)\]", comment)
        eval_tag = eval_match.group(1) if eval_match else get_eval_from_result(result)
        evals_list.append(povscore_to_int(eval_tag,turn))

    game_csr_matrix = csr_matrix(np.array(fen_array_list))
    evals_list = np.clip(evals_list, -10, 10)

    return game_csr_matrix, evals_list

def board_to_array(board):
    standard_counts = [8,2,2,2,1]
    board_array = []
    materials = []
    for color in chess.COLORS:
        for piece in chess.PIECE_TYPES:
            vector, count = bitboard_of_piece(board, piece, color)
            board_array.extend(vector)
            try:
                materials.append(count/standard_counts[piece-1])
            except:
                pass

    castles = get_castle_info(board)
    peasants = get_en_passant_array(board)
    board_array.extend(castles)
    board_array.extend(peasants)
    board_array.extend(materials)

    turn = board.turn
    halfmove_clock = board.halfmove_clock * 0.01
    board_array.append(turn)  # 1 for white's turn, 0 for black's turn
    board_array.append(halfmove_clock)
    
    return np.array(board_array)

def bitboard_of_piece(board, piece_type, color):
    bit_array = np.zeros(64, dtype=int)
    squares = list(board.pieces(piece_type, color))
    piece_count = len(squares)
    bit_array[squares] = 1
    return bit_array, piece_count

def get_en_passant_array(board):
    en_passant_array = np.zeros(64, dtype=int)
    if board.ep_square is not None:
        en_passant_array[board.ep_square] = 1
    relevant_squares = np.concatenate((en_passant_array[16:24], en_passant_array[40:48]))
    return relevant_squares

def get_castle_info(board):
    white_kingside = board.has_castling_rights(chess.WHITE) and board.has_kingside_castling_rights(chess.WHITE)
    white_queenside = board.has_castling_rights(chess.WHITE) and board.has_queenside_castling_rights(chess.WHITE)
    black_kingside = board.has_castling_rights(chess.BLACK) and board.has_kingside_castling_rights(chess.BLACK)
    black_queenside = board.has_castling_rights(chess.BLACK) and board.has_queenside_castling_rights(chess.BLACK)
    return [white_kingside, white_queenside, black_kingside, black_queenside]

def orient_board(board_vec, turn):
    if turn == chess.WHITE:
        perspective_vec = board_vec[:768]
        self_castles = board_vec[768:770]
        opponenet_castles = board_vec[770:772]
        possible_peasant = board_vec[772:780]
        self_piececount = board_vec[788:793]
        opponent_piececount = board_vec[793:798]
        fifty_and_turn = board_vec[-2:][::-1]
    else:
        flipped_vec = np.array([mat[::-1] for mat in board_vec[:768].reshape(12,8,8)]).reshape(-1)
        perspective_vec = np.concatenate([flipped_vec[384:],flipped_vec[:384]])
        self_castles = board_vec[770:772]
        opponenet_castles = board_vec[768:770]
        possible_peasant = board_vec[780:788]
        self_piececount = board_vec[793:798]
        opponent_piececount = board_vec[788:793]
        fifty_and_turn = board_vec[-2:][::-1]
            
    player_vec = np.concatenate([perspective_vec, self_castles, opponenet_castles, possible_peasant, self_piececount, opponent_piececount, fifty_and_turn])
    return player_vec

def reverse_orient_board(player_vec):
    turn = int(player_vec[-1])
    
    if turn == chess.WHITE:
        perspective_vec = player_vec[:768]
        white_castles = player_vec[768:770]
        black_castles = player_vec[770:772]
        possible_peasant = np.concatenate([player_vec[772:780],[0]*8])
        white_piececount = player_vec[780:785]
        black_piececount = player_vec[785:790]
        fifty_and_turn = player_vec[-2:][::-1]
        
    else:
        unflipped_vec = np.array([mat[::-1] for mat in player_vec[:768].reshape(12,8,8)]).reshape(-1)
        perspective_vec = np.concatenate([unflipped_vec[384:],unflipped_vec[:384]])
        black_castles = player_vec[768:770]
        white_castles = player_vec[770:772]
        possible_peasant = np.concatenate([[0]*8, player_vec[772:780]])
        black_piececount = player_vec[780:785]
        white_piececount = player_vec[785:790]
        fifty_and_turn = player_vec[-2:][::-1]

    board_vec = np.concatenate([perspective_vec, white_castles, black_castles, possible_peasant, white_piececount, black_piececount, fifty_and_turn])
    return board_vec

def vector_to_fen(vector):
    piece_symbols = "PNBRQKpnbrqk"
    board = [""] * 64

    for square in range(64):
        for piece_index in range(12):
            if vector[piece_index * 64 + square] == 1:
                board[square] = piece_symbols[piece_index]
                break

    fen_parts = []
    for rank in range(8, 0, -1):
        empty_count = 0
        rank_str = ""
        for file in range(8):
            piece = board[(rank-1)*8 + file]
            if piece == "":
                empty_count += 1
            else:
                if empty_count > 0:
                    rank_str += str(empty_count)
                    empty_count = 0
                rank_str += piece
        if empty_count > 0:
            rank_str += str(empty_count)
        fen_parts.append(rank_str)

    piece_placement = "/".join(fen_parts)
    
    active_color = "w" if vector[-2] == 1 else "b"
    
    castling_rights = ''.join(['K' if vector[768] == 1 else '',
                               'Q' if vector[769] == 1 else '',
                               'k' if vector[770] == 1 else '',
                               'q' if vector[771] == 1 else '',])
    if castling_rights == "":
        castling_rights = "-"

    en_passant_vector = vector[772:788]
    en_passant_target = "-"
    for i, val in enumerate(en_passant_vector):
        if val == 1:
            en_passant_target = chess.SQUARE_NAMES[16 + i] if i < 8 else chess.SQUARE_NAMES[40 + (i - 8)]
            break
    
    halfmove_clock = int(vector[-1])
    
    fullmove_number = "1"
    
    fen = f"{piece_placement} {active_color} {castling_rights} {en_passant_target} {halfmove_clock} {fullmove_number}"
    
    return fen

def index_to_piece_square(input_num, san=False):
    if input_num > 767:
        toret = index_to_plus_feature(input_num)
        return toret
    piece_colors = ["White", "Black"]
    type_list = ["Pawn", "Knight", "Bishop", "Rook", "Queen", "King"]
    type_l = ["P", "N", "B", "R", "Q", "K"]
    square_files = "abcdefgh"
    square_ranks = "12345678"

    piece_int = input_num // 64
    piece_col = int(piece_int > 5)
    PieceColor = piece_colors[piece_col]
    type_int = piece_int % 6
    PieceName = type_list[type_int]
    square_int = input_num % 64
    square_file = square_files[square_int % 8]
    square_rank = square_ranks[square_int // 8]

    if san:
        piece_symbols = [p.lower() if piece_col else p for p in type_l]
        piece = piece_symbols[type_int]
        return f'{piece}{square_file}{square_rank}'

    return f'{PieceColor} {PieceName} on {square_file}{square_rank}'

def index_to_plus_feature(input_num):
    if input_num < 768:
        print('This function is intended for input numbers greater than 767.')
        return None
    
    elif 768 <= input_num <= 771:
        castling_rights = ["White_Kingside", "White_Queenside", "Black_Kingside", "Black_Queenside"]
        return f'Castle_{castling_rights[input_num - 768]}'
    
    elif 772 <= input_num < 788:
        square_files = "abcdefgh"
        square_ranks = "36"  # En passant can only target these ranks
        en_passant_file = square_files[(input_num - 772) % 8]
        en_passant_rank = square_ranks[(input_num - 772) // 8]
        return f'en_passant {en_passant_file}{en_passant_rank}'
    
    elif input_num == 798:
        return 'turn_w'
    
    elif input_num == 799:
        return 'Halfmove_Clock'
    
    else:
        color = (input_num - 788) // 5
        type = (input_num - 788) % 5
        piece_colors = ["White", "Black"]
        type_list = ["Pawn", "Knight", "Bishop", "Rook", "Queen", "King"]
        return f'Material_{piece_colors[color]}_{type_list[type]}'

def apply_norm_and_idf(matrix):
    idf = get_idf_from_doc_term_mat(matrix)
    fen_idf_matrix = matrix.multiply(idf)
    fen_idf_matrix_norm = normalize(fen_idf_matrix, norm='l2', axis=1)
    return fen_idf_matrix_norm

def get_idf_from_doc_term_mat(matrix):
    document_frequencies = matrix.getnnz(axis=0)
    N = matrix.shape[0]
    normalizer = np.log(1 + N) + 1
    idf = (np.log((1 + N) / (1 + document_frequencies)) + 1)/normalizer
    return idf

def apply_query_transformations(query, matrix):
    idf = get_idf_from_doc_term_mat(matrix)
    scaled_query = query.reshape(1, -1) * idf
    normalized_query = normalize(scaled_query, norm='l2', axis=1)
    return normalized_query