import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import os
import matplotlib.pyplot as plt
from PIL import Image
from torchvision import transforms  # <-- Add this import statement
import torchvision

# Set device (use 'cuda' for GPU or 'cpu' for CPU)
device = torch.device('cpu')  # Change to 'cuda' if you want to use GPU

# Dataset class to load images from the directory
class CustomDataset(Dataset):
    def __init__(self, img_dir, transform=None):
        self.img_dir = img_dir
        self.img_paths = []
        
        # Walk through the directory and collect paths to image files only
        for root, dirs, files in os.walk(img_dir):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):  # Image file extensions
                    self.img_paths.append(os.path.join(root, file))
        
        self.transform = transform

    def __len__(self):
        return len(self.img_paths)

    def __getitem__(self, idx):
        img_path = self.img_paths[idx]
        img = Image.open(img_path).convert('RGB')
        if self.transform:
            img = self.transform(img)
        return img, 0  # Dummy label (not used in GANs)

# Define the transformations for the images
transform = transforms.Compose([
    transforms.ToTensor(),        # Convert to tensor
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))  # Normalize to [-1, 1]
])

# Load the dataset
dataset = CustomDataset(img_dir="/Users/gui/Desktop/Datasets/processed_imgs", transform=transform)
dataloader = DataLoader(dataset, batch_size=64, shuffle=True)

# Generator network
class Generator(nn.Module):
    def __init__(self, noise_dim):
        super(Generator, self).__init__()
        self.gen = nn.Sequential(
            nn.ConvTranspose2d(noise_dim, 512, kernel_size=4, stride=1, padding=0),
            nn.BatchNorm2d(512),
            nn.ReLU(True),
            nn.ConvTranspose2d(512, 256, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(True),
            nn.ConvTranspose2d(256, 128, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(True),
            nn.ConvTranspose2d(128, 64, kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(True),
            nn.ConvTranspose2d(64, 3, kernel_size=4, stride=2, padding=1),
            nn.Tanh()  # Tanh to scale output to [-1, 1]
        )

    def forward(self, x):
        return self.gen(x)

# Discriminator network
class Discriminator(nn.Module):
    def __init__(self, img_channels):
        super(Discriminator, self).__init__()
        self.disc = nn.Sequential(
            nn.Conv2d(img_channels, 64, kernel_size=3, stride=2, padding=1),  # kernel size changed to 3
            nn.LeakyReLU(0.2),
            nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(128),
            nn.LeakyReLU(0.2),
            nn.Conv2d(128, 256, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(256),
            nn.LeakyReLU(0.2),
            nn.Conv2d(256, 512, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(512),
            nn.LeakyReLU(0.2),
            # The final layer should produce a single output per image
            nn.Conv2d(512, 1, kernel_size=4, stride=1, padding=0)  # Using a kernel size of 4 to reduce output to (1, 1)
        )

    def forward(self, x):
        x = self.disc(x)
        x = x.view(x.size(0), -1)  # Flatten the tensor to (batch_size, 1)
        return x


# Initialize the models
noise_dim = 100  # Dimensionality of the random noise input to the generator
generator = Generator(noise_dim=noise_dim).to(device)
discriminator = Discriminator(img_channels=3).to(device)

# Loss function
criterion = nn.BCEWithLogitsLoss()  # Using BCEWithLogitsLoss to combine Sigmoid and BCELoss

# Optimizers
lr = 0.0002
beta1 = 0.5
d_optimizer = optim.Adam(discriminator.parameters(), lr=lr, betas=(beta1, 0.999))
g_optimizer = optim.Adam(generator.parameters(), lr=lr, betas=(beta1, 0.999))

# Training loop
epochs = 100
for epoch in range(epochs):
    for i, (real_images, _) in enumerate(dataloader):
        # Move real images to the correct device
        real_images = real_images.to(device)

        # Real labels are 1 for real images
        real_labels = torch.ones(real_images.size(0), 1).to(device)
        # Fake labels are 0 for fake images
        fake_labels = torch.zeros(real_images.size(0), 1).to(device)

        # --- Train Discriminator ---
        discriminator.zero_grad()

        # Forward pass through the discriminator with real images
        outputs = discriminator(real_images)
        d_loss_real = criterion(outputs, real_labels)
        d_loss_real.backward()

        # Generate fake images using the generator
        noise = torch.randn(real_images.size(0), noise_dim, 1, 1).to(device)
        fake_images = generator(noise)

        # Forward pass through the discriminator with fake images
        outputs = discriminator(fake_images.detach())  # Detach to avoid gradients on fake images
        d_loss_fake = criterion(outputs, fake_labels)
        d_loss_fake.backward()

        # Update the discriminator's weights
        d_optimizer.step()

        # --- Train Generator ---
        generator.zero_grad()

        # Forward pass through the discriminator with fake images
        outputs = discriminator(fake_images)
        g_loss = criterion(outputs, real_labels)  # The generator wants the discriminator to think fake images are real
        g_loss.backward()

        # Update the generator's weights
        g_optimizer.step()

        # Print the losses for monitoring
        if i % 100 == 0:  # Print every 100 batches
            print(f"Epoch [{epoch}/{epochs}], Step [{i}/{len(dataloader)}], "
                  f"D Loss Real: {d_loss_real.item()}, D Loss Fake: {d_loss_fake.item()}, G Loss: {g_loss.item()}")

    # Optionally save and visualize some generated images after each epoch
    if epoch % 10 == 0:  # Save generated images every 10 epochs
        with torch.no_grad():
            fake_images = generator(torch.randn(64, noise_dim, 1, 1).to(device))
            fake_images = (fake_images + 1) / 2  # Denormalize to [0, 1]
            grid = torchvision.utils.make_grid(fake_images, nrow=8)
            plt.figure(figsize=(8, 8))
            plt.imshow(grid.permute(1, 2, 0).cpu())
            plt.axis('off')
            plt.show()



