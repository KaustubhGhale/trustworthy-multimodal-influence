# Trustworthy Multi-Modal Influence & Community Detection

A unified project combining **Computer Vision**, **Social Network Analysis**, and **Blockchain** to detect communities, analyze influence patterns, and ensure trustworthy reputation scoring using decentralized ledgers.

## 📘 Overview
This research integrates:
- Vision-based co-appearance & scene analysis
- Graph-based community detection and link prediction
- Blockchain-backed on-chain reputation recording

## ⚙️ Tech Stack
- **Python 3.10**
- **YOLOv8n**, `face_recognition`, `networkx`, `torch`
- **Blockchain:** Solidity + Web3.py + IPFS

## 🧩 Pipeline
1. Dataset preparation (Visual Genome / custom)
2. CV preprocessing (faces, objects, OCR)
3. Graph construction and SNA
4. Link prediction (LogReg + GNN)
5. On-chain reputation recording

## 🚀 Setup
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## 🧪 Run
```bash
python src/data/dataset_prepare_visualgenome.py --mode local --img_dir data/images --out data/dataset
python src/data/preprocess_cv_lite.py --meta data/dataset/metadata.csv --out data/dataset
python src/data/build_graph.py --meta data/dataset/metadata.csv --cv data/dataset/cv_metadata_lite.csv --faces data/dataset/face_clusters.csv
```

## 🔗 Blockchain Integration
Run Ganache locally, then:
```bash
python src/blockchain/deploy_proof.py --rpc http://127.0.0.1:7545 --file data/dataset/metadata.csv
```
