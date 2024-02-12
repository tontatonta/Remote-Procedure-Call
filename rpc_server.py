
import socket
import os
import json
import math

class Function: #それぞれの関数を定義S
    def floor(params):
        x = float(params)
        return math.floor(x)

    def nroot(params):
        n,x = params.split()
        n = int(n)
        x = int(x)
        return math.floor(x**(1/n))

    def reverse(params):
        s = str(params)
        return s[::-1]

    def validAnagram(params):
        a,b = params.split()
        a = str(a)
        b = str(b)
        if len(a) != len(b):
            return False
        return sorted(a) == sorted(b)

    def sort(params):
        params = str(params)
        return sorted(params)    



def main():
    functionHashmap = {
        "floor": Function.floor,
        "nroot": Function.nroot,
        "reverse": Function.reverse,
        "validAnagram": Function.validAnagram,
        "sort": Function.sort
    }

    sock = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
    server_address = "./rpc_file"

    try:
        os.unlink(server_address)
    except FileNotFoundError:
        pass

    print("クライアントと接続")
    sock.bind(server_address)

    sock.listen(1)

    
    while True:
        try:
            
            while True:
                connection,client_address = sock.accept()
                print("- - - - - - - - - - - -")
                data = connection.recv(1024)

                receivedData = json.loads(data)    

                method = receivedData["method"]
                params = receivedData["params"]
                id = receivedData["id"]

                if method in functionHashmap:                   
                    result = functionHashmap[method](params)
                    answer = {
                        "結果": result,
                        "ID":id
                    }
                    
                else:
                    answer = {
                        "結果": "その方法は定義されていません",
                        "ID":id
                    }

                if data:
                    connection.send(json.dumps(answer).encode())
                else:
                    print("データがありません",client_address)
                    break         
                            

        finally:
            print("Closing current connection")
            connection.close()


if __name__ == "__main__":
    main()