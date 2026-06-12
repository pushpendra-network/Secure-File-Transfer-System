import socket
from cryptography.fernet import Fernet

# Login credentials
USERNAME = "admin"
PASSWORD = "1234"

# Function to receive exact bytes
def recv_exact(conn, size):
    data = b""
    while len(data) < size:
        packet = conn.recv(size - len(data))
        if not packet:
            return None
        data += packet
    return data

s = socket.socket()
s.bind(("localhost", 9999))
s.listen(1)

print("Server waiting...")

conn, addr = s.accept()
print("Connected from", addr)

# ---------------- LOGIN ----------------
user_len = int.from_bytes(recv_exact(conn, 4), 'big')
username = recv_exact(conn, user_len).decode()

pass_len = int.from_bytes(recv_exact(conn, 4), 'big')
password = recv_exact(conn, pass_len).decode()

if username != USERNAME or password != PASSWORD:
    conn.send(b"FAIL")
    print("Unauthorized access!")
    conn.close()
    exit()
else:
    conn.send(b"OK")
    print("User authenticated")

# ---------------- RECEIVE KEY ----------------
key_len = int.from_bytes(recv_exact(conn, 4), 'big')
key = recv_exact(conn, key_len)

cipher = Fernet(key)

# ---------------- RECEIVE FILE ----------------
data_len = int.from_bytes(recv_exact(conn, 8), 'big')
encrypted_data = recv_exact(conn, data_len)

# ---------------- DECRYPT ----------------
decrypted = cipher.decrypt(encrypted_data)

with open("received.txt", "wb") as f:
    f.write(decrypted)

print("File received and saved!")

conn.close()