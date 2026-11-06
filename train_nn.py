import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, accuracy_score

print("1. Chargement des données...")
file_path = "Bruteforce-Tuesday-no-metadata.parquet"
df = pd.read_parquet(file_path)

print("2. Nettoyage et préparation des données...")
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(inplace=True)

target_column = "Label"
if target_column not in df.columns:
    target_column = [col for col in df.columns if 'label' in col.lower()][0]

X = df.drop(columns=[target_column]).values
y_raw = df[target_column].values

# PyTorch a besoin de labels numériques (entiers) au lieu de texte
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y_raw)

print("3. Division et normalisation...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Création d'un Dataset PyTorch personnalisé
class IntrusionDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.long)
    def __len__(self):
        return len(self.X)
    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

train_dataset = IntrusionDataset(X_train_scaled, y_train)
test_dataset = IntrusionDataset(X_test_scaled, y_test)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

print("4. Définition du Réseau de Neurones (Multi-Layer Perceptron)...")
input_dim = X_train_scaled.shape[1]
num_classes = len(np.unique(y))

class IntrusionNN(nn.Module):
    def __init__(self, input_dim, num_classes):
        super(IntrusionNN, self).__init__()
        self.layer1 = nn.Linear(input_dim, 64)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.3)
        self.layer2 = nn.Linear(64, 32)
        self.output = nn.Linear(32, num_classes)
        
    def forward(self, x):
        x = self.relu(self.layer1(x))
        x = self.dropout(x)
        x = self.relu(self.layer2(x))
        x = self.output(x)
        return x

model = IntrusionNN(input_dim, num_classes)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

print("5. Entraînement du Réseau de Neurones (5 époques)...")
epochs = 5
for epoch in range(epochs):
    model.train()
    running_loss = 0.0
    for inputs, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    print(f"Époque [{epoch+1}/{epochs}], Perte (Loss): {running_loss/len(train_loader):.4f}")

print("\n6. Évaluation du modèle PyTorch...")
model.eval()
all_preds = []
all_targets = []
with torch.no_grad():
    for inputs, labels in test_loader:
        outputs = model(inputs)
        _, predicted = torch.max(outputs, 1)
        all_preds.extend(predicted.numpy())
        all_targets.extend(labels.numpy())

print(f"Précision globale (Accuracy) : {accuracy_score(all_targets, all_preds):.4f}")
print("\nRapport de classification détaillé :")
print(classification_report(all_targets, all_preds, target_names=label_encoder.classes_))