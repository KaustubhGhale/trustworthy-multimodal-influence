# src/blockchain/deploy_proof.py
"""
Deploy simple ProvenanceReputation contract to local Ganache and add a sample IPFS entry.
Usage:
  Start Ganache local RPC (default http://127.0.0.1:7545)
  python deploy_proof.py --rpc http://127.0.0.1:7545 --file data/dataset/metadata.csv
"""
import argparse, json, os
from solcx import compile_source, install_solc
from web3 import Web3
import ipfshttpclient

def compile_contract(path):
    source = open(path, 'r', encoding='utf-8').read()
    install_solc('0.8.18')
    compiled = compile_source(source, output_values=['abi','bin'])
    _, contract_interface = compiled.popitem()
    return contract_interface['abi'], contract_interface['bin']

def deploy_and_add(rpc, sol_path, file_to_add):
    w3 = Web3(Web3.HTTPProvider(rpc))
    acct = w3.eth.accounts[0]
    abi, bytecode = compile_contract(sol_path)
    Prov = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = Prov.constructor().transact({'from': acct})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    addr = tx_receipt.contractAddress
    print("Deployed contract at", addr)
    # add file to ipfs
    client = ipfshttpclient.connect()
    res = client.add(file_to_add)
    cid = res['Hash']
    print("IPFS CID:", cid)
    contract = w3.eth.contract(address=addr, abi=abi)
    tx = contract.functions.addEntry(cid, 1000000).transact({'from':acct})
    w3.eth.wait_for_transaction_receipt(tx)
    print("Added entry on-chain.")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--rpc", default="http://127.0.0.1:7545")
    p.add_argument("--sol", default="src/blockchain/ProvenanceReputation.sol")
    p.add_argument("--file", default="data/dataset/metadata.csv")
    args = p.parse_args()
    deploy_and_add(args.rpc, args.sol, args.file)
