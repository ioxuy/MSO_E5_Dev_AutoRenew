# -*- coding: UTF-8 -*-
import os
import time
import hashlib
import base64
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Register the azure app first and make sure the app has the following permissions:
# Files.Read.All、Files.ReadWrite.All
# Sites.Read.All、Sites.ReadWrite.All
# User.Read.All、User.ReadWrite.All
# Directory.Read.All、Directory.ReadWrite.All
# Mail.Read、Mail.ReadWrite、MailboxSettings.Read
# MailboxSettings.ReadWrite
# After registration, you must click on behalf of xxx to grant administrator consent, otherwise outlook api cannot be called

dir_path = os.path.abspath(os.path.dirname(__file__))
refresh_token_path = os.path.join(dir_path, "refresh_token")

apis = [
    'https://graph.microsoft.com/v1.0/drive/root',
    'https://graph.microsoft.com/v1.0/me/drive/root',
    'https://graph.microsoft.com/v1.0/me/drive',
    'https://graph.microsoft.com/v1.0/me/drive/root/children',    
    'https://graph.microsoft.com/v1.0/users',
    'https://graph.microsoft.com/v1.0/me/messages',
    'https://graph.microsoft.com/v1.0/me/mailFolders',
    'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',
    'https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages/delta',
    'https://graph.microsoft.com/v1.0/me/outlook/masterCategories',
#    'https://api.powerbi.com/v1.0/myorg/apps',    
]

class AESCipher():

    def __init__(self, key):
        self.key = key.encode('utf-8')
        self.bs = 16

    def encrypt(self, plaintext):
        cipher = AES.new(self.key, AES.MODE_ECB)
        plaintext = pad(plaintext.encode('utf-8'), self.bs)
        ciphertext = cipher.encrypt(plaintext)
        return base64.b64encode(ciphertext).decode()

    def decrypt(self, ciphertext):
        cipher = AES.new(self.key, AES.MODE_ECB)
        ciphertext = base64.b64decode(ciphertext)
        plaintext = cipher.decrypt(ciphertext)
        return unpad(plaintext, self.bs).decode('utf-8')


def get_access_token(refresh_token, client_id, client_secret):
    url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': 'http://localhost:53682/'
    }
    res = requests.post(url, data=data, headers=headers)
    access_token = ''
    if res.status_code == 200:
        access_token = res.json().get('access_token','')
        key = hashlib.md5(client_id.encode('utf-8')).hexdigest()
        aes = AESCipher(key)
        ciphertext = aes.encrypt(refresh_token)
        open(refresh_token_path,'w').write(ciphertext)
    return access_token

def main():
    client_id = os.environ.get('CLIENT_ID','')
    client_secret = os.environ.get('CLIENT_SECRET','')
    refresh_token = os.environ.get('REFRESH_TOKEN','')

    key = hashlib.md5(client_id.encode('utf-8')).hexdigest()
    if os.path.exists(refresh_token_path):
        try:
            ciphertext = open(refresh_token_path).read() 
            aes = AESCipher(key)            
            refresh_token = aes.decrypt(ciphertext)
        except:
            return "AES decryption failed."

    if not client_id or not client_secret or not refresh_token:
        return "client_id, client_secret or refresh_token is empty, cannot proceed."

    try:
        access_token = get_access_token(refresh_token, client_id, client_secret)
    except:
        return "get_access_token Call failed."

    if not access_token:
        return "access_token is empty, cannot proceed."

    session = requests.Session()
    session.headers.update({
        'Authorization': access_token,
        'Content-Type': 'application/json'
    })
    count = 0
    for api in apis:
        try:
            response = session.get(api)
            if response.status_code == 200:
                count += 1
                print(f'{api} Call successful')
            else:
                print(f'{api} Call failed')
        except requests.exceptions.RequestException as e:
            print(e)
            pass
    localtime = time.asctime(time.localtime(time.time()))
    return f'Successfully called the API {count} times. The end of this run is: {localtime}'

if __name__ == "__main__":
    msgs = list()
    for i in range(1,4):
        msg = main()
        msgs.append(f'{i}: {msg}')
    msg = "\n".join(msgs)
    print(msg)


    bot_token = os.environ.get('TG_BOT_TOKEN','')
    chat_id = os.environ.get('TG_CHAT_ID','')
    if bot_token and chat_id:
        msg  = '---------- [E5 AutoRenew] ----------\n' + msg
        requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', json={"chat_id": chat_id, "text": msg})
