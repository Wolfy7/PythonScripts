"""
Port scanner
"""
# import socket
# import time

# host = input("Hostname:")

# try:
#     ip = socket.gethostbyname(host)
# except socket.gaierror:
#     print(f"Error: Hostname: {host} could not be resolved!")

# start = time.time()
# for i in range(100):
#     try:
#         # AF_INET for socket family of address version 4 /  AF_INET6 for socket family of address version 6
#         # SOCK_STREAM  for Socket type of TCP connections / SOCK_DGRAM for Socket type of UDP connections
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         conn = sock.connect((ip, i))
#         print(f"Port {i} is Open")
#         sock.close()
#     except:
#         print(f"Port {i} is Close")
# end = time.time()
# print("Port scanning finished. Duration:", (end-start))

# For 100 ports - Port scanning finished. Duration: 199.84074807167053

"""
Port scanner with Multithreading
"""
# import socket
# import time
# import threading
# from queue import Queue

# threads = []

# host = input("Hostname:")

# try:
#     ip = socket.gethostbyname(host)
# except socket.gaierror:
#     print(f"Error: Hostname: {host} could not be resolved!")

# def portscan(port):
#     try:
#         # AF_INET for socket family of address version 4 /  AF_INET6 for socket family of address version 6
#         # SOCK_STREAM  for Socket type of TCP connections / SOCK_DGRAM for Socket type of UDP connections
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         conn = sock.connect((ip, port))
#         print(f"Port {port} is Open")
#         sock.close()
#     except:
#         print(f"Port {port} is Close")


# start = time.time()

# for x in range(100):
#     t = threading.Thread(target=portscan, args=(x,))
#     t.daemon = True
#     t.start()
#     threads.append(t)

# for t in threads:
#     t.join()

# end = time.time()
# print("Port scanning finished. Duration:", (end-start))

# For 100 ports - Port scanning finished. Duration: 2.0868663787841797

"""
Port scanner with Multithreading and Queue
"""
import socket
import time
import threading
from queue import Queue

print_lock = threading.Lock()

host = input("Hostname:")

try:
    ip = socket.gethostbyname(host)
except socket.gaierror:
    print(f"Error: Hostname: {host} could not be resolved!")

def portscan(port):
    try:
        # AF_INET for socket family of address version 4 /  AF_INET6 for socket family of address version 6
        # SOCK_STREAM  for Socket type of TCP connections / SOCK_DGRAM for Socket type of UDP connections
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn = sock.connect((ip, port))
        with print_lock:
            print(f"Port {port} is Open")
        sock.close()
    except:
        with print_lock:
            print(f"Port {port} is Close")

def threader():
   while True:
      worker = q.get()
      portscan(worker)
      q.task_done()

q = Queue()

start = time.time()

for x in range(10):
   t = threading.Thread(target = threader)
   t.daemon = True
   t.start()

for worker in range(100):
   q.put(worker)

q.join()
end = time.time()
print("Port scanning finished. Duration:", (end-start))

# For 100 ports with 10 Threads - Port scanning finished. Duration: 20.27564024925232