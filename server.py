import base64
import socket
"""'Socket' module defines how server and client machines can communicate at hardware level using 
 socket endpoints on top of the operating system."""
import sys
from pathlib import Path
from threading import Thread

SERVER_IP = "0.0.0.0"
SERVER_PORT = 8080
BUFFER_SIZE = 65536
CONNECTION_LIMIT = 1024

#extends the Thread class - defines all the facilities required to create an object that can execute within its own lightweight process
class WorkerThread(Thread):
    def __init__(self, ip, port, conn):
        Thread.__init__(self)
        self.client_ip = ip
        self.client_port = port
        self.conn = conn
        #"New thread has started for client address: {ip}:{port}"

    #override the run function of thread class 
    def run(self):
        msg = self.conn.recv(BUFFER_SIZE)
        tokens = msg.split(b"\n", maxsplit=2)
        cmd = tokens[0].decode().strip().lower()

        #if-else conditions to check which command is chosen
        if cmd == "upload":
            flname = tokens[1].decode().strip()
            fl_data = tokens[2]
            Path("uploads/").mkdir(parents=True, exist_ok=True)
            Path("uploads/{}".format(flname)).write_bytes(fl_data)
            print(f"{self.client_ip}:{self.client_port} -  '{flname}' is Uploaded successfully")

        elif cmd == "download":
            flname = tokens[1].decode().strip()
            file = Path("uploads/{}".format(flname))
            if file.is_file():
                self.conn.send(file.read_bytes())
                print(f"{self.client_ip}:{self.client_port} -  '{flname}' is Downloaded successfully")

        elif cmd == "delete":
            flname = tokens[1].decode().strip()
            file = Path("uploads/{}".format(flname))
            if file.is_file():
                file.unlink()
                print(f"{self.client_ip}:{self.client_port} -  '{flname}' has been Deleted")

        elif cmd == "rename":
            flname = tokens[1].decode().strip()
            new_flname = tokens[2].decode().strip()
            file = Path("uploads/{}".format(flname))
            new_file = Path("uploads/{}".format(new_flname))
            if file.is_file():
                file.rename(new_file)
                print(f"{self.client_ip}:{self.client_port} -  '{flname}' is now renamed to '{new_flname}'")


def main():
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpsock.bind((SERVER_IP, SERVER_PORT))
    tcpsock.listen(CONNECTION_LIMIT)
    print(f"Server is currently running at {SERVER_IP}:{SERVER_PORT}")
    while True:
        (conn, (client_ip, client_port)) = tcpsock.accept()
        # print(f"Connection request from {client_ip}:{client_port}")
        worker = WorkerThread(client_ip, client_port, conn)
        worker.start()


if __name__ == "__main__":
    main()
