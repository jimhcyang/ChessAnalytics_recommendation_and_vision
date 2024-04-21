from src.utils import fen_to_all_white_pawns
import logging

logger = logging.getLogger(__name__)


def compare_occupancy(original_fen, predicted_occupancy):
    ground_truth = fen_to_all_white_pawns(original_fen)
    if predicted_occupancy == ground_truth:
        return "Successful occupancy detection"
    else:
        return "Occupancy mismatch"
