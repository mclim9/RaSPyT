""" Rohde & Schwarz Automation for demonstration use."""
import socket

def sQuery(SCPI):                           # Socket Query
    sWrite(SCPI)
    sOut = s.recv(100000).decode().strip()
    print(f'Query: {sOut}')
    return sOut

def sWrite(SCPI):                           # Socket Write
    print(f'Write: {SCPI}')
    s.sendall(f'{SCPI}\n'.encode())

s = socket.socket()
s.connect(('192.168.58.115', 5025))
s.settimeout(5)

print(sQuery('*IDN?'))
print(sQuery('*OPT?'))
