#!/usr/bin/env python3

#import the required libraries 
import base64
import select
import socket
import sys
from pathlib import Path

# Include the server IP address and port number
SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080


def abort(msg):
    print("ERROR DURING CONNECTION: " + msg, file=sys.stderr)
    sys.exit(1)


def parse_arguments():
    args = {}

    # get command
    try:
        args["command"] = sys.argv[1].strip().upper()
    except IndexError:
        abort("Please provide any command. No command provided")

    # get filename
    try:
        args["filename"] = sys.argv[2].strip()
    except IndexError:
        abort("no filename provided")
        #command to Upload a file
    if args["command"] == "UPLOAD":
        pass
        #Command to download the uploaded file
    elif args["command"] == "DOWNLOAD":
        pass
        #Command to Delete the existing file
    elif args["command"] == "DELETE":
        pass
        #Command to Rename already existing file
    elif args["command"] == "RENAME":



        # get new filename
        try:
            args["new_filename"] = sys.argv[3].strip().upper()
        except IndexError:
            abort("Please provide a file name. New filename is not provided")
    else:
        abort("Invalid command")

    return args

#function to upload a new file
def do_UPLOAD(sock, filename):
    file = Path(filename)
    if not file.is_file():
        abort("Invalid file")
    encoded = base64.b64encode(file.read_bytes()).decode()
    msg = "{}\n{}\n{}".format("UPLOAD", file.name, encoded)
    sock.sendto(msg.encode(), (SERVER_IP, SERVER_PORT))

#function to download a new file
def do_DOWNLOAD(sock, filename):
    msg = "{}\n{}".format("DOWNLOAD", filename)
    sock.sendto(msg.encode(), (SERVER_IP, SERVER_PORT))
    ready = select.select([sock], [], [], 1)[0]
    if ready:
        data = sock.recv(65536)
        Path("DOWNLOADs/").mkdir(parents=True, exist_ok=True)
        Path("DOWNLOADs/{}".format(filename)).write_bytes(data)
    else:
        abort("DOWNLOAD timeout")

#function to delete a file
def do_DELETE(sock, filename):
    msg = "{}\n{}".format("DELETE", filename)
    sock.sendto(msg.encode(), (SERVER_IP, SERVER_PORT))

#function to rename a file
def do_RENAME(sock, filename, new_filename):
    msg = "{}\n{}\n{}".format("RENAME", filename, new_filename)
    sock.sendto(msg.encode(), (SERVER_IP, SERVER_PORT))


def main():
    args = parse_arguments()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))
    if args["command"] == "UPLOAD":
        do_UPLOAD(sock, args["filename"])
    elif args["command"] == "DOWNLOAD":
        do_DOWNLOAD(sock, args["filename"])
    elif args["command"] == "DELETE":
        do_DELETE(sock, args["filename"])
    elif args["command"] == "RENAME":
        do_RENAME(sock, args["filename"], args["new_filename"])
    sock.close()


if __name__ == "__main__":
    main()
