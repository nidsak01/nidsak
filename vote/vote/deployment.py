import solcx
from solcx import compile_standard, install_solc
import json
import solcx
from web3 import Web3
install_solc('0.8.0')

with open("./vote/smartcontract.sol", "r") as file:
    contact_list_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"smartcontract.sol": {"content": contact_list_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0",
)

print(compiled_sol)
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["smartcontract.sol"]["Voting"]["evm"]["bytecode"]["object"]
# get abi
abi = json.loads(compiled_sol["contracts"]["smartcontract.sol"]["Voting"]["metadata"])["output"]["abi"]


#to read compiled_code.json
with open('compiled_code.json', 'r') as f:
    compiled_contract = json.load(f)
# get bytecode
bytecode = compiled_sol["contracts"]["smartcontract.sol"]["Voting"]["evm"]["bytecode"]["object"]
# get abi
abi = json.loads(compiled_sol["contracts"]["smartcontract.sol"]["Voting"]["metadata"])["output"]["abi"]
print("ABI -----------------------------",abi)
#interacting with smart contract 
ganache_url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
web3.is_connected()
web3.eth.block_number
chain_id = 1337
address="0x"
private_key ="0x"
# Create the contract in Python
smartcontract = web3.eth.contract(abi=abi, bytecode=bytecode)
# Get the number of latest transaction
nonce = web3.eth.get_transaction_count(address)
print("NONCE_--------------------",nonce)

# build transaction
transaction = smartcontract.constructor().build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": web3.eth.gas_price,
        "from": address,
        "nonce": nonce,
    }
)
# Sign the transaction
sign_transaction = web3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract!")
# Send the transaction
transaction_hash = web3.eth.send_raw_transaction(sign_transaction.rawTransaction)
# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
transaction_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)
print(f"Done! Contract deployed to {transaction_receipt.contractAddress}")



# with open("./vote/smartcontract.sol", "r") as file:
#     contact_list_file = file.read()

# ...
# compiled_sol = compile_standard(
#     {
#         "language": "Solidity",
#         "sources": {"smartcontract.sol": {"content": contact_list_file}},
#         "settings": {
#             "outputSelection": {
#                 "*": {
#                     "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"] # output needed to interact with and deploy contract 
#                 }
#             }
#         },
#     },
#     solc_version="0.8.0",
# )
# print(compiled_sol)
# with open("compiled_code.json", "w") as file:
#     json.dump(compiled_sol, file)

# with open('smartcontract.sol', 'r') as f:
#     source = f.read()

# compiled_sol = py_solc_x.compile_solidity(
#     {'<stdin>': source},
#     output_values=['abi', 'bin']
# )
# contract_id, contract_interface = compiled_sol['<stdin>:MyContract']['abi'], compiled_sol['<stdin>:MyContract']['bin']
# with open(".smartcontract.sol", "r") as file:
#     simple_storage_file = file.read()

 #to save the output in a JSON file