# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json

hostName = "localhost"
serverPort = 8080
Userlist={}
Sellers={}
MaxSupply=100000
CurrentSupply=0
CoinsPerMine = 1
MineCD = 150
CoinCountJson = "ENTER FILENAME FOR Coins.json"
SellerIDsJson = "ENTER FILENAME FOR Seller.json"


#
#
#
#Print Statements and comments are still in german feel free to reach out if I should update them to an english version
#
#
#







def save_to_json(filename):
    with open(filename, 'w') as file:
        json.dump(Userlist, file)
    print(f"Benutzerdaten wurden in {filename} gespeichert.")


# Läd Hasmap aus Json
def load_from_json(filename1, filename2):
    global Userlist
    try:
        with open(filename1, 'r') as file:
            Userlist = json.load(file)
        print(f"Benutzerdaten wurden aus {filename1} geladen.")
    except FileNotFoundError:
        print(f"Datei {filename1} nicht gefunden. Starte mit einem leeren Dictionary.")
    except json.JSONDecodeError:
        print(f"Fehler beim Dekodieren von {filename1}. Starte mit einem leeren Dictionary.")

    global Sellers
    try:
        with open(filename2, 'r') as file:
            Sellers = json.load(file)
        print(f"Benutzerdaten wurden aus {filename2} geladen.")
    except FileNotFoundError:
        print(f"Datei {filename2} nicht gefunden. Starte mit einem leeren Dictionary.")
    except json.JSONDecodeError:
        print(f"Fehler beim Dekodieren von {filename2}. Starte mit einem leeren Dictionary.")



class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        global CurrentSupply
        #print(Userlist) 
        
        

        filtered_userlist = {user: {'score': info['score']} for user, info in Userlist.items()}
        
        response = json.dumps(filtered_userlist, ensure_ascii=False)

        
        User = self.headers.get("User")
        Kunde = self.headers.get("Kunde")
        Amount = self.headers.get("Amount")
        print(User)
        if User in Userlist:
            if int(Userlist[User]['timestamp'])+MineCD <= time.time():
                if CurrentSupply<MaxSupply:
                    Userlist[User]['score']=Userlist[User]['score']+CoinsPerMine
                    Userlist[User]['timestamp'] = time.time()
                    CurrentSupply=+CoinsPerMine
                    print(Userlist)
                    self.send_response(200)
                    save_to_json(CoinCountJson)
                else:
                    self.send_response(204)
                    print("Max Supply an Coins wurde erreicht")
            else:
                self.send_response(200)
                print("Betrugsversuch: mind. Zeit nicht vorbei")
        elif User in Sellers:
            if Userlist[Kunde]['score']>int(Amount)-100:
                SellersUser = Sellers[User]['User']
                Userlist[Kunde]['score']=Userlist[Kunde]['score']-int(Amount)
                Userlist[SellersUser]['score']=Userlist[SellersUser]['score']+int(Amount)
                self.send_response(200)
                save_to_json(CoinCountJson)
            else:
                self.send_response(204)
                print("Kunde im Minus BROKE BOI detected")
        else:
            self.send_response(203)
            print("Name kein registrierter Nutzer")


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