import socket

HOST = 'localhost'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
PORT2 = 5001

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (HOST, PORT2)
orig = (HOST, PORT)
bufferSize = 1024

udp.bind(orig)

def sendFile(fileName):
    fileEncoded = fileName.encode()
    udp.sendto (fileEncoded, dest)
    
    with open(fileName, 'rb') as file:
        fileBytes = file.read()
    
    for i in range(0, len(fileBytes), bufferSize):
        udp.sendto(fileBytes[i:i + bufferSize], dest)
        print(i, "bytes sent.")
    
    msgErro = "thiago grangeiro".encode()
    udp.sendto(msgErro, dest)
    
    print(f"File '{fileName}' sent successfully to the server!")

while True:
    msg, cliente = udp.recvfrom(bufferSize)
    filePathReceive = msg.decode()
    fileNameReceive = filePathReceive.split('/')[-1]
    fileNameReceive, fileExt = fileNameReceive.split('.')
    fileNameReceive = fileNameReceive + "." + fileExt
    
    qtdBytes = b''
    i = 0
    
    while True:
        msg, cliente = udp.recvfrom(bufferSize)
        if not msg:
            break
        if msg == "thiago grangeiro".encode():
            break
        qtdBytes += msg

        i += bufferSize
        with open(fileNameReceive, 'wb') as newFile:
            newFile.write(qtdBytes)
            
        print("File", i, "received successfully!")
    
    sendFile(fileNameReceive)
    
udp.close()