# Ethereum Contract Analyzer

A Python tool for analyzing Ethereum smart contracts, retrieving contract creators, other contracts deployed by the same creator, and identifying top interactors with the contract using Etherscan API and Web3.

## Features

- **Get Contract Creator**: Retrieves the creator of a specific smart contract.
- **Analyze Other Contracts**: Finds other contracts deployed by the same creator.
- **Top Interactors**: Retrieves the top interactors with a given contract.

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt` or managed via `Poetry`.

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/neochrist/ethereum-dependency-graph
    cd ethereum-dependency-graph
    ```

2. Install Dependencies:

    - Using `pip` and `requirements.txt`:

      ```bash
      pip install -r requirements.txt
      ```

3. Set up Environment Variables:

    Create a `.env` file in the root of the project with your Etherscan API key and Infura project ID:

    ```plaintext
    ETHERSCAN_API_KEY=your_etherscan_api_key
    INFURA_PROJECT_ID=your_infura_project_id
    ```

4. Run the Analyzer:

    Run the script and provide a contract address when prompted:

    ```bash
    python ethereum_contract_analyzer.py
    ```

    You will be asked to input the Ethereum contract address. The script will then:
    - Fetch the contract creator.
    - List other contracts deployed by the same creator.
    - Display the top interactors with the contract.

## Running Tests

To ensure the repository is cloned correctly and everything is set up, run the unit tests using the following command:

```bash
python3 -m unittest discover -s tests
