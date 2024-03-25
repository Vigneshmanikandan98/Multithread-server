# Multithread Simple File Transfer System

This project is a simple file transfer system implemented in Python using sockets. It consists of a server and a client script that allow users to upload, download, delete, and rename files on the server.

## Features

- **Upload**: Upload files to the server.
- **Download**: Download files from the server.
- **Delete**: Delete files from the server.
- **Rename**: Rename files on the server.

## Prerequisites

Before running the scripts, ensure you have Python 3 installed on your machine.

## Setup

# Navigate to the project directory:
# Server
Open a terminal and run the server script:
python server.py
The server will start running on 0.0.0.0:8080.

# Client
Open another terminal and run the client script with the desired command:
python client.py <command> <filename> [new_filename]
Replace <command> with one of the following:

UPLOAD: Upload a file to the server.
DOWNLOAD: Download a file from the server.
DELETE: Delete a file from the server.
RENAME: Rename a file on the server.
Replace <filename> with the name of the file to be manipulated.

For the RENAME command, also provide [new_filename] as the new name for the file.

Example:

python client.py UPLOAD myfile.txt
