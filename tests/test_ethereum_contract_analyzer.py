import unittest
from unittest.mock import patch, MagicMock
from main.ethereum_contract_analyzer import ( 
    get_contract_creator,
    get_contracts_by_creator,
    get_top_interactors,
    analyze_contract
)


class TestEthereumContractAnalyzer(unittest.TestCase):

    @patch('main.ethereum_contract_analyzer.requests.get')
    def test_get_contract_creator(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'status': '1',
            'result': [{'contractCreator': '0x123456789abcdef'}]
        }
        mock_get.return_value = mock_response

        creator = get_contract_creator('0xcontractaddress')
        self.assertEqual(creator, '0x123456789abcdef')

    @patch('main.ethereum_contract_analyzer.requests.get')
    def test_get_contracts_by_creator(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'status': '1',
            'result': [
                {'to': '', 'contractAddress': '0xcontract1'},
                {'to': '0xsomeaddress', 'contractAddress': ''},
                {'to': '', 'contractAddress': '0xcontract2'}
            ]
        }
        mock_get.return_value = mock_response

        contracts = get_contracts_by_creator('0xcreatoraddress')
        self.assertEqual(contracts, ['0xcontract1', '0xcontract2'])

    @patch('main.ethereum_contract_analyzer.requests.get')
    def test_get_top_interactors(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'status': '1',
            'result': [
                {'from': '0xuser1', 'to': '0xcontractaddress'},
                {'from': '0xuser2', 'to': '0xcontractaddress'},
                {'from': '0xuser1', 'to': '0xcontractaddress'},
                {'from': '0xuser3', 'to': '0xcontractaddress'},
                {'from': '0xuser2', 'to': '0xcontractaddress'},
                {'from': '0xcontractaddress', 'to': '0xsomeaddress'},  # This should be ignored
            ]
        }
        mock_get.return_value = mock_response

        top_interactors = get_top_interactors('0xcontractaddress', limit=2)
        expected = [('0xuser1', 2), ('0xuser2', 2)]
        self.assertEqual(top_interactors, expected)

    @patch('main.ethereum_contract_analyzer.get_contract_creator')
    @patch('main.ethereum_contract_analyzer.get_contracts_by_creator')
    @patch('main.ethereum_contract_analyzer.get_top_interactors')
    def test_analyze_contract(self, mock_top_interactors, mock_contracts_by_creator, mock_contract_creator):
        mock_contract_creator.return_value = '0xcreator'
        mock_contracts_by_creator.return_value = ['0xcontract1', '0xcontract2']
        mock_top_interactors.return_value = [('0xuser1', 5), ('0xuser2', 3)]

        with patch('builtins.print') as mock_print:
            analyze_contract('0xcontractaddress')

            mock_print.assert_any_call("Analyzing contract: 0xcontractaddress")
            mock_print.assert_any_call("Contract Creator: 0xcreator")
            mock_print.assert_any_call("Other contracts deployed by the creator:")
            mock_print.assert_any_call("- 0xcontract1")
            mock_print.assert_any_call("- 0xcontract2")
            mock_print.assert_any_call("Top interactors:")
            mock_print.assert_any_call("- 0xuser1: 5 interactions")
            mock_print.assert_any_call("- 0xuser2: 3 interactions")