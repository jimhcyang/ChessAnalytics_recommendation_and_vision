from collections import deque
import os

def extract_gm_games(pgn_file_path, output_file_path):
    window_size = 25
    lines_window = deque(maxlen=window_size)
    game_buffer = []
    total_games = 0
    gm_games_count = 0
    is_gm_game = False
    decide = False
    pgn = False

    with open(pgn_file_path, 'r', encoding='utf-8') as pgn_file:
        for line in pgn_file:
            
            if pgn:
                if line == "\n":
                    decide = True
                else:
                    lines_window.append(line)
                    game_buffer.append(line)
                    continue 

            lines_window.append(line)
            game_buffer.append(line)

            if decide:
                if is_gm_game:
                    gm_games_count += 1
                    total_games += 1
                    with open(output_file_path, 'a', encoding='utf-8') as output_file:
                        output_file.writelines(game_buffer)
                        output_file.writelines('\n')
                else:
                    total_games += 1
                game_buffer = []
                lines_window = deque(maxlen=window_size)
                is_gm_game = False
                decide = False
                pgn = False
                continue

            if line == "\n":
                pgn = True
                if any('"GM"' in line for line in lines_window if 'Title' in line):
                    is_gm_game = True

    extracted_percentage = (gm_games_count / total_games) * 100 if total_games > 0 else 0
    print(f"Extraction completed. {gm_games_count}/{total_games} games extracted.")
    print(f"Extracted Percentage is {extracted_percentage:.2f}%.")

assets_path = os.path.join(os.path.dirname(os.getcwd()), 'data')
single_path = os.path.join(assets_path, 'caissa_base.pgn')
output_path = os.path.join(assets_path, 'caissa_gm.pgn')

extract_gm_games(single_path, output_path)
print("Extraction completed.")

#Extraction completed. 619384/4874268 games extracted.
#Extracted Percentage is 12.71%.
#Extraction completed.