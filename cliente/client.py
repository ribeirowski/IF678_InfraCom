import socket

HOST = 'localhost'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
PORT2 = 5001

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (HOST, PORT)
orig = (HOST, PORT2)
bufferSize = 1024

udp.bind(orig)

def receiveFile():
    msg, cliente = udp.recvfrom(bufferSize)
    fileDecoded = msg.decode()
    fileName, fileExt = fileDecoded.split('.')
    fileName = fileName + "_received." + fileExt
    
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
        with open(fileName, 'wb') as newFile:
            newFile.write(qtdBytes)
            
        print("File", i, "received successfully!")

while True:
    filePath = input('Digite o caminho do arquivo com a extensão:')
    fileName = filePath.split('\\')[-1].encode()
    
    udp.sendto (fileName, dest)
    
    with open(filePath, 'rb') as file:
        fileBytes = file.read()
    
    for i in range(0, len(fileBytes), bufferSize):
        udp.sendto(fileBytes[i:i + bufferSize], dest)
        print(i, "bytes sent.")
    
    msgErro = "thiago grangeiro".encode()
    udp.sendto(msgErro, dest)
    
    print(f"File '{fileName.decode()}' sent successfully to the server!")
    
    receiveFile()

udp.close()