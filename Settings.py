
from passlib.hash import pbkdf2_sha256 as hasher
    
password = "performance"
hashed = hasher.hash(password)

DEBUG = True
PORT = 5051
HOST = '127.0.0.1'

PASSWORDS = {
    "admin": '$pbkdf2-sha256$29000$FELoHeO8N.acMwZgzJlTqg$J1dsHWCPf6fSLfPCbWD4/qbNNN41CUbyix4iNR4uCKY'
}

ADMIN_USERS = ["admin"]