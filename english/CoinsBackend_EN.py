from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json

hostName = "localhost"
serverPort = 8080
Userlist = {}
Sellers = {}
MaxSupply = 100000
CurrentSupply = 0
CoinsPerMine = 1
MineCD = 150
CoinCountJson = "ENTER FILENAME FOR Coins.json"
SellerIDsJson = "ENTER FILENAME FOR Seller.json"

# 
# 
# 
# Print statements and comments have been translated to English.
# 
# 
# 

def save_to_json(filename):
    with open(filename, 'w') as file:
        json.dump(Userlist, file)
    print(f"User data has been saved to {filename}.")

# Load Hashmap from JSON
def load_from_json(filename1, filename2):
    global Userlist
    try:
        with open(filename1, 'r') as file:
            Userlist = json.load(file)
        print(f"User data has been loaded from {filename1}.")
    except FileNotFoundError:
        print(f"File {filename1} not found. Starting with an empty dictionary.")
    except json.JSONDecodeError:
        print(f"Error decoding {filename1}. Starting with an empty dictionary.")

    global Sellers
    try:
        with open(filename2, 'r') as file:
            Sellers = json.load(file)
        print(f"User data has been loaded from {filename2}.")
    except FileNotFoundError:
        print(f"File {filename2} not found. Starting with an empty dictionary.")
    except json.JSONDecodeError:
        print(f"Error decoding {filename2}. Starting with an empty dictionary.")

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        global CurrentSupply

        filtered_userlist = {user: {'score': info['score']} for user, info in Userlist.items()}
        response = json.dumps(filtered_userlist, ensure_ascii=False)

        User = self.headers.get("User")
        Customer = self.headers.get("Customer")
        Amount = self.headers.get("Amount")
        print(User)

        if User in Userlist:
            if int(Userlist[User]['timestamp']) + MineCD <= time.time():
                if CurrentSupply < MaxSupply:
                    Userlist[User]['score'] = Userlist[User]['score'] + CoinsPerMine
                    Userlist[User]['timestamp'] = time.time()
                    CurrentSupply += CoinsPerMine
                    print(Userlist)
                    self.send_response(200)
                    save_to_json(CoinCountJson)
                else:
                    self.send_response(204)
                    print("Max supply of coins has been reached")
            else:
                self.send_response(200)
                print("Fraud attempt: minimum time not yet passed")
        elif User in Sellers:
            if Userlist[Customer]['score'] > int(Amount) - 100:
                SellersUser = Sellers[User]['User']
                Userlist[Customer]['score'] = Userlist[Customer]['score'] - int(Amount)
                Userlist[SellersUser]['score'] = Userlist[SellersUser]['score'] + int(Amount)
                self.send_response(200)
                save_to_json(CoinCountJson)
            else:
                self.send_response(204)
                print("Customer is broke: BROKE BOI detected")
        else:
            self.send_response(203)
            print("Name is not a registered user")

        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(response, "utf-8"))

if __name__ == "__main__":
    load_from_json(CoinCountJson, SellerIDsJson)
    for key, value in Userlist.items():
        CurrentSupply = CurrentSupply + value['score']
        print(CurrentSupply)
    
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
