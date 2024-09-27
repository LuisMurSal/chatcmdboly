import socket
import threading
import sys
import pickle

class Cliente():
    def __init__(self, host="localhost", port=7000):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((str(host), int(port)))
            print("Conectado al servidor.")
            msg_recv = threading.Thread(target=self.msg_recv, daemon=True)
            msg_recv.start()
            while True:
                msg = input('-> ')
                if msg != 'salir':
                    self.send_msg(msg)
                else:
                    self.sock.close()
                    sys.exit()
        except Exception as e:
            print(f"Error al conectar el socket: {e}")

    def msg_recv(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if data:
                    data = pickle.loads(data)
                    print(data.decode())  # Asegúrate de decodificar el mensaje
            except Exception as e:
                print(f"Error recibiendo mensaje: {e}")
            finally:
                pass

    def send_msg(self,msg):
        try:
            self.sock.send(pickle.dumps(msg))
        except Exception as e:
            print(f'Error enviando mensaje: {e}')

if __name__ == "__main__":
    cliente = Cliente()
