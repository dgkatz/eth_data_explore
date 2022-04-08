from web3 import Web3

from aws_eth_http_provider import AWSHTTPProvider

AWS_GETH_SERVER_HTTP = "https://nd-msrinxgg6re2blj26qdoxncvie.ethereum.managedblockchain.us-east-1.amazonaws.com"
AWS_GETH_SERVER_WS = "ws://nd-msrinxgg6re2blj26qdoxncvie.wss.ethereum.managedblockchain.us-east-1.amazonaws.com"


def main():
    w3 = Web3(AWSHTTPProvider("https://nd-msrinxgg6re2blj26qdoxncvie.ethereum.managedblockchain.us-east-1.amazonaws.com"))
    latest_block = w3.eth.get_block("latest")
    print(latest_block)


if __name__ == '__main__':
    main()
