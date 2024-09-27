import socket
import threading
import os
import sys
import pickle

class Servidor():
    def __init__(self, host="localhost", port=7000):
        self.clientes = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((str(host), int(port)))
        self.sock.listen(10)
        self.sock.setblocking(False)

        aceptar = threading.Thread(target=self.aceptarCon, daemon=True)
        procesar = threading.Thread(target=self.procesarCon, daemon=True)
        aceptar.start()
        procesar.start()

        try:
            while True:
                msg = input('-> ')
                if msg == 'salir':
                    break
        except KeyboardInterrupt:
            print("Servidor detenido por el usuario.")
        finally:
            self.sock.close()
            sys.exit()

    def msg_to_all(self, msg, cliente):
        for c in self.clientes:
            try:
                if c != cliente:
                    c.send(msg)
            except:
                self.clientes.remove(c)

    def aceptarCon(self):
        print("aceptarCon iniciado")
        while True:
            try:
                conn, addr = self.sock.accept()
                conn.setblocking(False)
                self.clientes.append(conn)
                print(f"Cliente {addr} conectado.")
            except BlockingIOError:
                continue

    def procesarCon(self):
        print("ProcesarCon iniciado")
        while True:
            if len(self.clientes) > 0:
                for c in self.clientes:
                    try:
                        data = c.recv(1024)
                        if data:
                            command = pickle.loads(data)
                            print(f"Comando recibido: {command}") 
                            self.process_command(command, c)
                    except Exception as e:
                        print(f"Error procesando conexión: {e}")
                        self.clientes.remove(c)

    def process_command(self, command, cliente):
        if command.startswith("lsFiles"):
            try:
                files = os.listdir('Files')  
                response = '\n'.join(files).encode() 
                cliente.send(pickle.dumps(response))
            except Exception as e:
                print(f"Error listando archivos: {e}")
        elif command.startswith("get "):
            filename = command.split(" ")[1]
            self.send_file(filename, cliente)

    def send_file(self, filename, cliente):
        try:
            filepath = os.path.join('Files', filename)
            with open(filepath, 'rb') as file:
                data = file.read()
                cliente.send(pickle.dumps(data))
        except FileNotFoundError:
            cliente.send(pickle.dumps(f"Archivo {filename} no encontrado.").encode()) 
if __name__ == "__main__":
    server = Servidor()
