import requests
import random
import socket
import base64


def leave(guild):
  with open('tokens.txt', 'r') as f:
      token = f.read().splitlines()
  with open('proxy.txt', 'r') as f:
      lines = f.readlines()
      randomproxy = random.choice(lines)
      proxy = {
        "http://": randomproxy
      }
  for i in token:
    headers={'authorization': i}
    requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{guild}",headers=headers,proxies=proxy)

def send(num):
  with open('tokens.txt', 'r') as f:
      token = f.read().splitlines()
  with open('channel.txt', 'r') as f:
      channel = f.read().splitlines()
  with open('content.txt', 'r') as f:
      content = f.read()
  with open('proxy.txt', 'r') as f:
      lines = f.readlines()
      randomproxy = random.choice(lines)
      proxy = {
        "http://": randomproxy
      }
  number = int(num)
  for nu in range(number):
            a = random.choice(channel)
            url = 'https://discord.com/api/v9/channels/'+a+'/messages'
            en = ["a","b","c","d","i","e","f","g","h","i","j","k","n","m","l","o","p","q","r","s","","t","u","v","w","s","y","g"]
            enran = f"{random.choice(en)}{random.choice(en)}{random.choice(en)}"
            data = {"content": f"{content}"}
            i = random.choice(token)
            header = {"authorization": i}
            r = requests.post(url, data=data, headers=header,proxies=proxy)
            if r.status_code == 200:
              print(f":行けた")

def checker():
  with open('tokens.txt', 'r') as f:
      token = f.read().splitlines()
  for token in token:
    header = {
      "authorization": token
    }
  with open('proxy.txt', 'r') as f:
      lines = f.readlines()
      randomproxy = random.choice(lines)
      proxy = {
        "http://": randomproxy
      }
  userdata = requests.get("https://discord.com/api/v9/users/@me",headers=header,proxies=proxy).json()
  print(f"<name>{userdata['username']}#{userdata['discriminator']} <id>{userdata['id']} <mail>{userdata['email']} <token>{token} <from>{userdata['locale']}")

    
def guilds():
  with open('tokens.txt', 'r') as f:
      token = f.read().splitlines()
  with open('proxy.txt', 'r') as f:
      lines = f.readlines()
      randomproxy = random.choice(lines)
      proxy = {
        "http://": randomproxy
      }
  for token in token:
    header={'authorization': token,"content-type": "application/json"}
    r=requests.get("https://discord.com/api/v9/users/@me/guilds", headers=header,proxies=proxy).json()
    s=['\n'.join([f"name {a['name']} | id {a['id']} |owner {a['owner']}" for a in r])]
    print(s)

def ip():
  ip = socket.gethostbyname(socket.gethostname())
  print(f"{ip}が貴方のipです")

def tokensteal(userid):
  encodedBytes = base64.b64encode(userid.encode("utf-8"))
  encodedStr = str(encodedBytes, "utf-8")
  print("first token:"+encodedStr)
