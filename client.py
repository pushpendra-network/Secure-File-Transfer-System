import socket
from cryptography.fernet import Fernet

s = socket.socket()
s.connect(("localhost", 9999))

# ---------------- LOGIN ----------------
username = input("Enter username: ")
password = input("Enter password: ")

# send username
s.sendall(len(username).to_bytes(4, 'big'))
s.sendall(username.encode())

# send password
s.sendall(len(password).to_bytes(4, 'big'))
s.sendall(password.encode())

# receive response
response = s.recv(1024)

if response == b"FAIL":
    print("Login failed!")
    s.close()
    exit()
else:
    print("Login successful!")

# ---------------- ENCRYPT FILE ----------------
key = Fernet.generate_key()
cipher = Fernet(key)

with open("file.txt", "rb") as f:
    data = f.read()

encrypted_data = cipher.encrypt(data)

# ---------------- SEND KEY ----------------
s.sendall(len(key).to_bytes(4, 'big'))
s.sendall(key)

# ---------------- SEND FILE ----------------
s.sendall(len(encrypted_data).to_bytes(8, 'big'))
s.sendall(encrypted_data)

print("File sent!")

s.close()