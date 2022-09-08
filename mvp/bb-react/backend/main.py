import os
import json
import pandas
import requests
import simplejson as json

from aggregator import Sr71Radar
from crypto_client import CryptoClient
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS, cross_origin
from sherlock import Sherlock
from wallet_processor import WalletProcessor

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/transactionHistory', methods=['GET'])
@cross_origin()
def get_transaction_history():
    walletAddress = request.args.get('walletAddress', default=AKITA_ADDRESS, type=str)
    wallet_processor = WalletProcessor()
    stats = wallet_processor.process(walletAddress)
    print(f'VATTTRUUUU STATS: {stats}')
    # transactions = wallet_processor.get_transaction_history(walletAddress)
    # print("TRANSACTION COUNT: ", len(transactions))
    # print("TRANSACTIONS SIR: ", transactions)


    # transfers = crypto_client._get_all_transfers(RAGSY_ADDRESS)
    # print("ALL TRANSFERS: ", len(transfers))
    # crypto_client.get_transaction_receipt('0x8118accb3746ebb4f7c349e57f9453de9b55ca64803a72895630bbe24f17ad33')
    # '0x822356b6b1ef3fc3cdc913fee836a6de445e4a7381774ce459944d1691e9df8d')
    return {}
    # return transactions



@app.route('/prubby', methods=['GET'])
@cross_origin()
def get_prubby_time():
    sr71 = Sr71Radar()
    print(f"----Scanning initiated. Prepare Sr-71 for takeoff. Prubs Away!----")
    return sr71.scan([RAGSY_ADDRESS, PRUBBY_ADDRESS])

RAGSY_ADDRESS = ''
PRUBBY_ADDRESS = ''

TEST_ADDRESSES = [
    "0x7ae92148e79d60a0749fd6de374c8e81dfddf792", # 2 NFTs
    PRUBBY_ADDRESS, # recent Matic transaction
    # "0x091933ee1088cdf5daace8baec0997a4e93f0dd6",
    "0x828103b231b39fffce028562412b3c04a4640e64",
    "0xd6216fc19db775df9774a6e33526131da7d19a2c"
    # "0x4399f61795d3e50096e236a6d31ab24470c99fd5",
    # "0xd69b0089d9ca950640f5dc9931a41a5965f00303",
    # "0x4baf012726cb5ec7dda57bc2770798a38100c44d"
    ]

@app.route('/prubbyNft', methods=['GET'])
def get_prubby_nft():
    crypto_client = CryptoClient()
    crypto_client.get_nfts_for_wallet("0x7ae92148e79d60a0749fd6de374c8e81dfddf792")
    return {}

@app.route('/blackbirdInbound', methods=['GET'])
def recon():
    sr71 = Sr71Radar()
    # addys = [w3.toChecksumAddress(k) for k in addys]

    print(f"----Scanning initiated. Prepare Sr-71 for takeoff. Prubs Away!----")
    # return sr71.scan(addys[-1:])
    return sr71.scan(["0xd6216fc19db775df9774a6e33526131da7d19a2c"])


@app.route("/getSherlockStakingPositions", methods=['GET'])
@cross_origin()
def get_sherlock_staking_positions():
    sherlock = Sherlock()
    return sherlock.get_stakers_time_series()

@app.route("/getSherlockStakingPool", methods=['GET'])
@cross_origin()
def get_sherlock_staking_pool():
    sherlock = Sherlock()
    return sherlock.get_staking_pool_time_series()

@app.route("/getSherlockStakerWalletStats", methods=['GET'])
@cross_origin()
def get_sherlock_wallet_stats():
    sherlock = Sherlock()
    return sherlock.get_staker_wallet_stats()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
