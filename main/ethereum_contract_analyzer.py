import os
from web3 import Web3
import requests
from dotenv import load_dotenv

load_dotenv()

ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')
INFURA_PROJECT_ID = os.getenv('INFURA_PROJECT_ID')

w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}'))

def get_contract_creator(contract_address):
    url = f'https://api.etherscan.io/api?module=contract&action=getcontractcreation&contractaddresses={contract_address}&apikey={ETHERSCAN_API_KEY}'
    response = requests.get(url)
    data = response.json()
    if data['status'] == '1':
        return data['result'][0]['contractCreator']
    return None

def get_contracts_by_creator(creator_address):
    url = f'https://api.etherscan.io/api?module=account&action=txlist&address={creator_address}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}'
    response = requests.get(url)
    data = response.json()
    contracts = []
    if data['status'] == '1':
        for tx in data['result']:
            if tx['to'] == '' and tx['contractAddress'] != '':
                contracts.append(tx['contractAddress'])
    return contracts

def get_top_interactors(contract_address, limit=5):
    url = f'https://api.etherscan.io/api?module=account&action=txlist&address={contract_address}&startblock=0&endblock=99999999&sort=desc&apikey={ETHERSCAN_API_KEY}'
    response = requests.get(url)
    data = response.json()
    interactors = {}
    if data['status'] == '1':
        for tx in data['result']:
            if tx['from'] != contract_address:
                interactors[tx['from']] = interactors.get(tx['from'], 0) + 1
    return sorted(interactors.items(), key=lambda x: x[1], reverse=True)[:limit]

def analyze_contract(contract_address):
    print(f"Analyzing contract: {contract_address}")
    
    # Get contract creator
    creator = get_contract_creator(contract_address)
    print(f"Contract Creator: {creator}")
    
    # Get other contracts deployed by the creator
    other_contracts = get_contracts_by_creator(creator)
    print("Other contracts deployed by the creator:")
    for contract in other_contracts:
        if contract.lower() != contract_address.lower():
            print(f"- {contract}")
    
    # Get top interactors
    top_interactors = get_top_interactors(contract_address)
    print("Top interactors:")
    for address, count in top_interactors:
        print(f"- {address}: {count} interactions")

if __name__ == "__main__":
    contract_address = input("Enter the Ethereum contract address: ")
    analyze_contract(contract_address)