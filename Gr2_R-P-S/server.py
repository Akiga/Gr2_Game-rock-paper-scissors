import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

rooms = {}   # room_name -> [conn1, conn2]
choices = {} # room_name -> {conn: choice}
lock = threading.Lock()
