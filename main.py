import requests
import scrypt 
import socket
import json

POOL_HOST = "ltc.zsolo.bid"  
POOL_PORT = 4057
user = "ltc1quja3smxyr4m02f7v8tjmcwz37567k7z0rj66ac"
API_URL = "https://ltc-chain.api.btc.com/v3/block/latest"
SALT = b"LitecoinMiningSalt"
nonce = 0
Mining = True

print("Start Solo Mining Litecoin")
print("--------------------------")

def mine_block():
  print("Finding a new share")
  global nonce
  response = requests.get(API_URL)
  block_data = response.json()["data"] 
  print(block_data)  
  previous_hash = block_data["prev_block_hash"]
  height = block_data["height"] + 1  
  while Mining:
    input_data = (previous_hash + str(height) + str(nonce)).encode()
    block_hash = scrypt.hash(input_data, salt=SALT)
    if block_hash.startswith(b"0000"):     
      print(f"Block mined: {block_hash}")
      return block_hash
    nonce += 1

def submit_block(block_hash):

  client = socket.socket()
  client.connect((POOL_HOST, POOL_PORT))
  message = {"method":"submit",
             "params":{"username":user,"job_id":"","nonce":"","result":block_hash}}
  message = json.dumps(message).encode()
  client.send(message)
  response = client.recv(1024).decode()
  print(f"Pool response: {response}")
  client.close()
  print("Share was accepted")

if __name__ == "__main__":
    mined_block = mine_block()
    print(mined_block)
    submit_block(mined_block)
