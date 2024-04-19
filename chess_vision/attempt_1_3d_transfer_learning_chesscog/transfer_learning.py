import os
import cv2
import numpy as np
from pathlib import Path
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from torch.utils.data import Dataset, DataLoader
import torch.optim as optim
import chesscog
from chesscog.core import device, DEVICE


class ChessDataset(Dataset):
    def __init__(self, image_dir, transform=None):
        image_dir = Path(image_dir).expanduser()
        self.image_paths = [os.path.join(image_dir, img)
                            for img in os.listdir(image_dir)]
        self.transform = transform
        self.fen_string = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, index):
        image = cv2.imread(self.image_paths[index])
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if self.transform:
            image = self.transform(image)

        fen_vector = self.fen_to_vector(self.fen_string)
        return image, fen_vector

    def fen_to_vector(self, fen):
        board_vector = np.zeros((64, 12))
        piece_to_index = {
            'p': 0, 'n': 1, 'b': 2, 'r': 3, 'q': 4, 'k': 5,
            'P': 6, 'N': 7, 'B': 8, 'R': 9, 'Q': 10, 'K': 11
        }
        positions = fen.split()[0]
        row = 0
        col = 0
        for char in positions:
            if char.isdigit():
                col += int(char)
            elif char == '/':
                row += 1
                col = 0
            else:
                index = piece_to_index[char]
                board_vector[row * 8 + col, index] = 1
                col += 1
        return board_vector.flatten()


if __name__ == "__main__":
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((299, 299)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
    ])

    dataset = ChessDataset(
        image_dir='~/Desktop/personal_github/capstone/data/processed', transform=transform)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

    # Load and modify InceptionV3
    model_path = Path(
        '~/Desktop/personal_github/capstone/models/InceptionV3.pt').expanduser()
    inception_v3 = models.inception_v3(pretrained=False)

    # Assuming you have 64 positions and 12 possible classes for each
    # num_final_outputs = 64 * 12  # 768
    num_final_outputs = 12

    # Adjust the final layer of the main classifier to match the number of classes you have
    num_ftrs = inception_v3.fc.in_features
    # Update the number of output features to match the total label count
    # Assuming each position on the board can be one of 12 classes
    # 64 board positions, 12 possible classes each
    # inception_v3.fc = nn.Linear(num_ftrs, 64 * 12)
    inception_v3.fc = nn.Linear(num_ftrs, num_final_outputs)

    # Adjust the auxiliary classifier
    if hasattr(inception_v3, 'AuxLogits'):
        num_aux_ftrs = inception_v3.AuxLogits.fc.in_features
        inception_v3.AuxLogits.fc = nn.Linear(num_aux_ftrs, 12)

    # Now load the state dict
    if os.path.exists(model_path):
        loaded_object = torch.load(model_path, map_location=DEVICE)

        # Adjust keys if necessary and load the state dict
        if hasattr(loaded_object, 'state_dict'):
            state_dict = loaded_object.state_dict()
            adjusted_state_dict = {key.replace(
                'model.', ''): value for key, value in state_dict.items()}
        else:
            # Assuming the loaded object is a state dict
            adjusted_state_dict = {key.replace(
                'model.', ''): value for key, value in loaded_object.items()}

        inception_v3.load_state_dict(adjusted_state_dict, strict=False)
    else:
        print("Pre-trained model not found. Initializing with default weights.")

    # Define loss function and optimizer
    # criterion = nn.CrossEntropyLoss()
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(inception_v3.fc.parameters(), lr=0.001)

    # Training loop
    num_epochs = 10  # Adjust the number of epochs
    for epoch in range(num_epochs):
        inception_v3.train()
        # When computing the loss, ensure labels are of the correct shape and type
        for images, labels in dataloader:
            optimizer.zero_grad()
            outputs, aux_outputs = inception_v3(images)

            # Ensure labels are floats since BCEWithLogitsLoss expects float targets
            labels = labels.float()

            # Compute the loss for both main and auxiliary outputs
            loss1 = criterion(outputs, labels)
            loss2 = criterion(aux_outputs, labels)

            # Final loss
            loss = loss1 + 0.4 * loss2
            loss.backward()
            optimizer.step()
        print(f'Epoch {epoch+1}, Loss: {loss.item()}')

    # Save the model
    torch.save(inception_v3.state_dict(
    ), '/Users/nankivel/Desktop/personal_github/capstone/chesscog/models/transfer_learning_models/piece_classifier/chess_inception_v3_finetuned.pth')
