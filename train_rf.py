import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

print("1. Chargement des données...")
# Remplacez par le nom du fichier que vous souhaitez tester (ex: Brute Force ou DoS)
file_path = "Bruteforce-Tuesday-no-metadata.parquet"
df = pd.read_parquet(file_path)

print(f"Dimensions initiales du dataset : {df.shape}")

print("\n2. Prétraitement et nettoyage des données...")
# Nettoyage des valeurs infinies ou manquantes qui font planté l'entraînement
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(inplace=True)

# Séparation des features (X) et de la cible (y)
# Note : Vérifiez si le nom de la colonne cible est bien 'Label' dans votre fichier
target_column = "Label" 
if target_column not in df.columns:
    # Parfois les espaces ou la casse posent problème, cherchons une colonne similaire
    target_column = [col for col in df.columns if 'label' in col.lower()][0]

X = df.drop(columns=[target_column])
y = df[target_column]

# Si le dataset est trop lourd pour votre RAM, vous pouvez échantillonner (ex: garder 20% des données)
# X = X.sample(frac=0.2, random_state=42)
# y = y.loc[X.index]

print(f"Classes détectées : {y.unique()}")

print("\n3. Division en ensembles d'entraînement et de test...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("\n4. Normalisation des caractéristiques (Scaling)...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\n5. Entraînement du modèle Random Forest...")
# n_estimators=100 (nombre d'arbres)
rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf_model.fit(X_train_scaled, y_train)

print("\n6. Évaluation du modèle...")
y_pred = rf_model.predict(X_test_scaled)

print(f"Précision globale (Accuracy) : {accuracy_score(y_test, y_pred):.4f}")
print("\nRapport de classification détaillé :")
print(classification_report(y_test, y_pred))

print("Matrice de confusion :")
print(confusion_matrix(y_test, y_pred))
import joblib

# Sauvegarde du modèle entraîné
joblib.dump(rf_model, 'train_rf.pkl')
print("Modèle sauvegardé avec succès dans train_rf.pkl")