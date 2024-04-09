import torch
import torch.nn.functional as F
from PIL import Image
import pandas as pd
from src.utils import occupancy_to_fen, fen_to_occupancy
from src.occupancy import ChessBoardCNN
from torchvision import transforms

# Assuming the rest of your code is the same and the model is already trained and available


def predict(image_path, model, transform, label=None):
    """
    Predict the chess board configuration in FEN notation from an image.

    Args:
    image_path (str): Path to the image of the chessboard.
    model (torch.nn.Module): The trained neural network model.
    transform (torchvision.transforms.Compose): Transformations to apply to the image.
    label (str, optional): The actual label (FEN notation) for the image, if available.

    Returns:
    str: The predicted FEN notation of the board.
    """
    # Load and transform the image
    image = Image.open(image_path)
    image = transform(image).unsqueeze(0)  # Add batch dimension

    # Get predictions from the model
    model.eval()
    with torch.no_grad():
        outputs = model(image)
        predicted = outputs > 0.5
        occupancy = ''.join(
            ['1' if x else '0' for x in predicted.squeeze().tolist()])

    # Convert the occupancy to FEN notation
    predicted_fen = occupancy_to_fen(occupancy)

    # If a label (actual FEN) is provided, compare it with the prediction
    if label:
        actual_fen = occupancy_to_fen(fen_to_occupancy(label))
        print(f"Actual FEN: {actual_fen}")
        print(f"Predicted FEN: {predicted_fen}")
    else:
        print(f"Predicted FEN: {predicted_fen}")

    return predicted_fen


# Example usage:
# Assuming the model is loaded and a transform is defined
model_path = 'models/new_occupancy_detection.pth'
model = ChessBoardCNN()
model.load_state_dict(torch.load(model_path))

transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
])

# Predict the FEN notation for an image
predicted_fen = predict(
    'data/occupancy/test_real/IMG_0439.JPG', model, transform)

pass
