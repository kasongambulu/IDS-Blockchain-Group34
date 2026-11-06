from __future__ import annotations

import joblib
import numpy as np
import pandas as pd
from eth_account import Account
from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel

app = FastAPI(
    title="IDS & Blockchain Threat Sharing API",
    version="1.0",
)

# 1. Chargement du modèle Random Forest entraîné
try:
  model = joblib.load("train_rf.pkl")
  print("Modèle Random Forest chargé avec succès !")
except Exception as e:
  print(f"Erreur lors du chargement du modèle : {e}")

# 2. Configuration Blockchain (Sepolia & Infura)
INFURA_URL = "https://sepolia.infura.io/v3/4e23938591fe4329aefd1508441f6fc0"
PRIVATE_KEY = (
    "cf1b369bee8f5c6f53c87a6327569ac62f24b01ca2eedfd9381d22fde202a307"
)
CONTRACT_ADDRESS = "0xe194fbb67e88d669434bd9da29837fbdc3b4d5"


class NetworkTraffic(BaseModel):
  features: list[float]


def call_ethereum_rpc(method, params=[]):
  payload = {"jsonrpc": "2.0", "method": method, "params": params, "id": 1}
  response = requests.post(INFURA_URL, json=payload, timeout=10)
  return response.json()


def send_threat_to_blockchain(threat_info: str):
  try:
    account = Account.from_key(PRIVATE_KEY)
    sender_address = account.address

    nonce_res = call_ethereum_rpc(
        "eth_getTransactionCount", [sender_address, "latest"]
    )
    nonce = int(nonce_res.get("result", "0x0"), 16)

    gas_price_res = call_ethereum_rpc("eth_gasPrice", [])
    gas_price = int(gas_price_res.get("result", "0x3B9ACA00"), 16)

    tx = {
        "nonce": nonce,
        "gasPrice": gas_price,
        "gas": 200000,
        "to": CONTRACT_ADDRESS,
        "value": 0,
        "data": "0x",
        "chainId": 11155111,
    }

    signed_tx = Account.sign_transaction(tx, PRIVATE_KEY)
    tx_res = call_ethereum_rpc(
        "eth_sendRawTransaction", ["0x" + signed_tx.raw_transaction.hex()]
    )
    return tx_res.get("result")
  except Exception as e:
    print(f"Erreur blockchain : {e}")
    return None


@app.get("/")
def home():
  return {
      "message": "Bienvenue sur l'API IDS connectée à la blockchain Sepolia !"
  }


@app.post("/predict_and_share")
def predict_and_share(data: NetworkTraffic):
  if model is None:
    raise HTTPException(
        status_code=500, detail="Modèle non chargé sur le serveur."
    )

  expected_features = model.n_features_in_
  user_features = data.features

  # Ajustement dynamique propre et bien indenté
  if len(user_features) < expected_features:
    user_features = user_features + [0.0] * (
        expected_features - len(user_features)
    )
  elif len(user_features) > expected_features:
    user_features = user_features[:expected_features]

  input_data = np.array(user_features).reshape(1, -1)
  prediction = model.predict(input_data)
  prediction_result = str(prediction[0])

  blockchain_tx = None
  if prediction_result.lower() != "benign":
    print(
        f"Menace détectée : {prediction_result}. Enregistrement sur la"
        " blockchain..."
    )
    blockchain_tx = send_threat_to_blockchain(prediction_result)

  return {
      "prediction": prediction_result,
      "blockchain_tx_hash": blockchain_tx,
      "status": "Alerte partagée sur la blockchain"
      if blockchain_tx
      else "Trafic bénin ou non partagé",
  }