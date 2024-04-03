import os
import cv2
import numpy as np
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from torch.utils.data import Dataset, DataLoader
import torch.optim as optim


class ChessDataset(Dataset):
    def __init__(self, image_dir, transform=None):
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

    dataset = ChessDataset(image_dir='path/to/images', transform=transform)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

    # Load and modify InceptionV3
    # Path to your pre-trained model
    model_path = '/Users/nankivel/Desktop/personal_github/capstone/chesscog/models/transfer_learning_models/piece_classifier/InceptionV3.pt'

    inception_v3 = models.inception_v3(pretrained=True)
    num_ftrs = inception_v3.fc.in_features
    # Adjust for the output size
    inception_v3.fc = nn.Linear(num_ftrs, 64 * 12)

    # Load the pre-trained weights, if available
    if os.path.exists(model_path):
        inception_v3.load_state_dict(torch.load(model_path))
    else:
        print("Pre-trained model not found. Initializing with default weights.")

    # Define loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(inception_v3.fc.parameters(), lr=0.001)

    # Training loop
    num_epochs = 10  # Adjust the number of epochs
    for epoch in range(num_epochs):
        inception_v3.train()
        for images, labels in dataloader:
            optimizer.zero_grad()
            outputs, aux_outputs = inception_v3(images)
            labels = labels.type(torch.LongTensor)
            loss1 = criterion(outputs, labels)
            loss2 = criterion(aux_outputs, labels)
            loss = loss1 + 0.4 * loss2
            loss.backward()
            optimizer.step()
        print(f'Epoch {epoch+1}, Loss: {loss.item()}')

    # Save the model
    torch.save(inception_v3.state_dict(
    ), '/Users/nankivel/Desktop/personal_github/capstone/chesscog/models/transfer_learning_models/piece_classifier/chess_inception_v3_finetuned.pth')
