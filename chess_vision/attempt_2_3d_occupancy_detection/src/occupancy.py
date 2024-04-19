import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms, datasets
from torch.utils.data import Dataset, DataLoader
import pandas as pd
from PIL import Image


class ChessBoardDataset(Dataset):
    def __init__(self, img_dir, annotation_file, transform=None):
        self.img_labels = pd.read_csv(annotation_file)
        self.img_dir = img_dir
        self.transform = transform

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        img_path = f"{self.img_dir}/{self.img_labels.iloc[idx, 0]}"
        image = Image.open(img_path)
        label = torch.tensor([int(x)
                             for x in list(self.img_labels.iloc[idx, 1])])
        if self.transform:
            image = self.transform(image)
        return image, label

# TODO: seperate into a training module


transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
])

train_dataset = ChessBoardDataset(img_dir='data/occupancy/train',
                                  annotation_file='data/occupancy/train/labels.csv',
                                  transform=transform)

test_dataset = ChessBoardDataset(img_dir='data/occupancy/test',
                                 annotation_file='data/occupancy/test/labels.csv',
                                 transform=transform)

train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=4, shuffle=False)


class ChessBoardCNN(nn.Module):
    def __init__(self):
        super(ChessBoardCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 64, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(64, 128, 3, padding=1)
        self.fc1 = nn.Linear(128 * 64 * 64, 1024)
        self.fc2 = nn.Linear(1024, 64)  # 64 outputs

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(-1, 128 * 64 * 64)
        x = torch.relu(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))
        return x


model = ChessBoardCNN()
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training
num_epochs = 1
for epoch in range(num_epochs):
    for images, labels in train_loader:
        outputs = model(images)
        loss = criterion(outputs, labels.float())
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print(f'Epoch {epoch+1}, Loss: {loss.item()}')

# Evaluation
model.eval()
with torch.no_grad():
    correct = 0
    total = 0
    for images, labels in test_loader:
        outputs = model(images)
        predicted = outputs > 0.5
        total += labels.size(0) * 64  # Total number of squares
        correct += (predicted == labels).sum().item()
    print(f'Accuracy: {100 * correct / total}%')

torch.save(model.state_dict(
), 'models/new_occupancy_detection.pth')
