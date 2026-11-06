# 🛡️ GROUPE 34 — Détection d'Intrusions par IA & Partage Décentralisé d'Indicateurs de Menace (Blockchain)

Ce projet combine l'**Apprentissage Automatique (Machine Learning)** pour la détection comportementale des menaces réseau en temps réel et la **Blockchain Ethereum Sepolia** pour l'archivage immutable et le partage décentralisé d'indicateurs de compromission (IoC).

---

## 👥 Membres du Groupe 34
   **KASONGA MBULU PAUL**
   **KAMIZELO KIESE RONY**

---

## 📌 1. Vue d'Ensemble du Système

- **Moteur de Détection IA** : Classification des flux réseau via un modèle Random Forest entraîné sur des jeux de données d'attaques réseau (CIC-IDS2017 / UNSW-NB15).
- **API REST Backend** : API haute performance développée avec FastAPI et Uvicorn, intégrant le prétraitement et l'alignement dynamique des caractéristiques (padding/truncation).
- **Registre Décentralisé** : Smart Contract Solidity (`ThreatSharing.sol`) déployé sur le réseau de test Ethereum Sepolia, enregistrant automatiquement les alertes de menaces sous forme de transactions signées cryptographiquement.

---

## 🏗️ 2. Stack Technique & Adresse du Contrat

- **Langages & Frameworks** : Python 3.10, FastAPI, Uvicorn, Scikit-Learn, Pandas, NumPy, Joblib, Solidity.
- **Web3 & Infrastructure** : Web3 / Eth-Account, JSON-RPC via Infura, Ethereum Sepolia Testnet.
- **Adresse du Contrat Intelligent** : [`0xe194fbb67e88d669434bd9da29837fbdc3b4d5`](https://sepolia.etherscan.io/address/0xe194fbb67e88d669434bd9da29837fbdc3b4d5)
- **Lien Explorateur Sepolia Etherscan** : [https://sepolia.etherscan.io/address/0xe194fbb67e88d669434bd9da29837fbdc3b4d5](https://sepolia.etherscan.io/address/0xe194fbb67e88d669434bd9da29837fbdc3b4d5)

---

## 🚀 3. Installation et Lancement en Local

### 3.1 Prérequis
- Python 3.10 ou version ultérieure
- Git

### 3.2 Clonage du Dépôt & Environnement Virtuel
```bash
git clone [https://github.com/votre-compte/IDS-Blockchain-Group34.git](https://github.com/votre-compte/IDS-Blockchain-Group34.git)
cd IDS-Blockchain-Group34

# Création et activation de l'environnement virtuel
python -m venv venv
# Sur Windows:
venv\Scripts\activate
# Sur Linux/Mac:
source venv/bin/activate