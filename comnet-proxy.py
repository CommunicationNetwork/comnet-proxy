import socket
from receivers.esp8266_receiver import ESP8266Receiver

backend_connected = False

class ProxyServer:
    def __init__(self, host, port, receiver):
        self.socket = socket.socket()
        self.socket.bind((host, port))
        self.receiver = receiver

    def start(self):
        global backend_connected
        self.socket.listen()
        while True:
            backend, _ = self.socket.accept()
            backend_connected = True
            self.receiver.backend = backend
            self.receiver.start()
            while backend_connected:
                continue
            self.receiver.stop()

def send_callback(data, backend):
    global backend_connected
    try:
        backend.sendall(data)
    except:
        backend_connected = False
        
def main():
    receiver = ESP8266Receiver("wlp4s0mon", "receiver", send_callback)
    proxy = ProxyServer("localhost", 5000, receiver)
    proxy.start()

if __name__ == "__main__":
    main()