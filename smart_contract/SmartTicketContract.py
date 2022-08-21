import json
import os
from pathlib import Path

import solcx
from environ import environ
from web3 import Web3

from server.settings import BASE_DIR


class SmartTicketContract:
    max_gas_price = 3000000

    def __init__(self, promoter, customer, price):
        __env = environ.Env()
        environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

        # Install the solidity compiler
        solcx.install_solc(version='0.8.16')

        self.__api_key = __env('INFURA_API_KEY')
        self.__w3 = Web3(Web3.HTTPProvider(__env('INFURA_GURLI_ENDPOINT')))

        self.__price = self.__w3.toWei(int(price), 'ether')
        self.__contract_instance = None

        if promoter is not None:
            self.__promoter_id = promoter.uid
            self.__promoter_address = promoter.wallet_hash
            self.__promoter_key = promoter.wallet_private_key

        if customer is not None:
            self.__customer_id = customer.uid
            self.__customer_address = customer.wallet_hash
            self.__customer_key = customer.wallet_private_key

    @staticmethod
    def __compile_source_file() -> dict:
        """
        Opens the file containing the smart contract and compiles it
        :return: dict containing the abi and bin of the contract
        """
        with open(os.path.join(Path(__file__).resolve().parent, 'SmartContract.sol'), 'r') as f:
            source = f.read()

        return solcx.compile_source(
            source,
            output_values=["abi", "bin"],
            base_path='smart_contract'
        )

    def __get_transaction_hash(self, tx):
        """
        Get a transaction hash in a readable format.

        :param tx: Transaction hash
        :return: Transaction hash in string format
        """
        txn = self.__w3.eth.getTransaction(tx)
        tx_json = json.loads(self.__w3.toJSON(txn))
        return tx_json['hash']

    def __send_transaction(self, tx, user_key):
        """
        Sign the transaction with the user key, sends it
        and waits until the transaction is written in a block

        :param tx: Transaction to send
        :param user_key: User signature key
        :return: Transaction hash
        """
        signed_tx = self.__w3.eth.account.sign_transaction(tx, private_key=user_key)
        tx_hash = self.__w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        logs = self.__w3.eth.wait_for_transaction_receipt(tx_hash).logs
        return tx_hash, logs

    def deploy_new_contract(self):
        """
        Creates a new contract and deploys it to the network
        """
        sources = self.__compile_source_file()
        contract_id, contract_interface = next(iter(sources.items()))

        contract = self.__w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface["bin"])

        construct_tx = contract.constructor().build_transaction({
            'nonce': self.__w3.eth.get_transaction_count(self.__promoter_address),
            'gas': SmartTicketContract.max_gas_price,
        })
        signed_tx = self.__w3.eth.account.sign_transaction(construct_tx, private_key=self.__promoter_key)
        tx_hash = self.__w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = self.__w3.eth.wait_for_transaction_receipt(tx_hash)

        return tx_receipt['contractAddress'], contract_interface['abi']

    def set_contract(self, contract_address, contract_abi):
        self.__contract_instance = self.__w3.eth.contract(
            address=contract_address,
            abi=contract_abi
        )

    def confirm_purchase(self):
        """
        Confirms the user wants to buy a ticket.
        This function call the contract method through a new transaction.
        The transaction is signed with the user key before sending it.

        :return: Transaction hash
        """
        price = self.__w3.toWei(self.__price, 'ether')
        tx = self.__contract_instance.functions.safeMint(self.__customer_address).buildTransaction({
            'nonce': self.__w3.eth.get_transaction_count(self.__customer_address),
            'gas': SmartTicketContract.max_gas_price,
            'value': price,
        })
        tx_hash, logs = self.__send_transaction(tx, self.__customer_key)
        return self.__get_transaction_hash(tx_hash), self.__w3.toInt(logs[0].topics[3])

    def refund_seller(self):
        """
        Refunds the promoter
        This function call the contract method through a new transaction.
        The transaction is signed with the promoter key before sending it.

        :return: Transaction hash
        """
        tx = self.__contract_instance.functions.withdraw().buildTransaction({
            'nonce': self.__w3.eth.get_transaction_count(self.__promoter_address),
            'gas': SmartTicketContract.max_gas_price
        })
        tx_hash, _ = self.__send_transaction(tx, self.__promoter_key)
        return self.__get_transaction_hash(tx_hash)

    def get_owner_of(self, token):
        return self.__contract_instance.functions.ownerOf(int(token)).call()
