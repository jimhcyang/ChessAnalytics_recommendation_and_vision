

def fen_to_occupancy(fen):
    # Initialize the occupancy string
    occupancy = ""

    # Split the FEN string at spaces and take the first part (ignoring other game state information)
    fen_position = fen.split()[0]

    # Iterate over each character in the FEN position
    for char in fen_position:
        if char.isdigit():
            # If the character is a digit, add that many '0's to the occupancy string
            occupancy += '0' * int(char)
        elif char == '/':
            # If the character is a slash, ignore it (it's just a row separator)
            continue
        else:
            # Any other character represents a piece, so add '1'
            occupancy += '1'

    return occupancy


def occupancy_to_fen(occupancy):
    # Initialize the FEN string
    fen = ""
    empty_count = 0  # Counter for consecutive empty squares

    # Iterate over each character in the occupancy string
    for i, char in enumerate(occupancy):
        if char == '0':
            # Increment counter for empty squares
            empty_count += 1
        else:
            # If there's a counted sequence of empty squares, add it before the piece
            if empty_count > 0:
                fen += str(empty_count)
                empty_count = 0
            # Add a pawn for each '1', using 'P' (we assume white pawns for simplicity)
            fen += 'P'

        # At the end of a row (8 characters processed) or at the end of the string
        if (i + 1) % 8 == 0 and i != 0:
            if empty_count > 0:
                # Add remaining empty square count at the end of a row
                fen += str(empty_count)
                empty_count = 0
            if i != len(occupancy) - 1:
                # Add a slash to separate rows, except at the end of the string
                fen += '/'

    # Handle any remaining empty squares at the end (if the loop ends without resetting)
    if empty_count > 0:
        fen += str(empty_count)

    return fen
