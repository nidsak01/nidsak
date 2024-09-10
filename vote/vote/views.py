from eth_utils import address
import os
import json
from django.shortcuts import render
from django.http import HttpResponse
from eth_account import Account
from web3 import Web3
from solcx import compile_standard, install_solc
# from eth_account.messages import encode_defunct
# from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import solcx
from solcx import compile_standard, install_solc
from .models import Vote
from django.shortcuts import render
from web3 import Web3
from . import models
from .models import Vote
from .contract_config import ABI, CONTRACT_ADDRESS  # Import ABI and contract address

def vote(request):
    if request.method == 'POST':
        option = request.POST.get('option')
        voter = request.POST.get('voter')

        # Initialize Web3
        w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
        account = w3.eth.accounts[0]

        # Initialize the contract
        voting_contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
        
        # Check if the voter has already voted
        if voting_contract.functions.hasVotedStatus(account).call():
            return HttpResponse("You have already voted.")
        
        # Call the contract function
        voting_contract.functions.vote(option).transact({'from': account})
        
        # Save the vote to the database
        Vote.objects.create(option=option, voter=voter)
        
        return render(request, 'success.html')
    else:
        return render(request, 'vote.html')


# def vote(request):
#     if request.method == 'POST':
#         option = request.POST.get('option')
#         voter = request.POST.get('voter')
#         w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
#         account = w3.eth.accounts[0]
#         voting_contract = w3.eth.contract(address=contract_address, abi=abi)
#         voting_contract.functions.vote(option).transact({'from': account})
#         Vote.objects.create(option=option, voter=voter)
#         return render(request, 'success.html')
#     else:
#         return render(request, 'vote.html')

