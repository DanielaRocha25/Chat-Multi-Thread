import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(('localhost', 8888))
print("Digite '@SAIR' para sair do chat.") # Informa ao usuário qual palavra permite sair do programa
user = input("Informe seu usuário: ") #Cada pessoa que logar no chat terá seu usuário
def envia():
    running = True
    while running:
        msg = input() #Coleta a mensagem do usuário
        texto = f"{user}|{msg}"
        if msg == '@SAIR': #Verifica se o usuario digitou '@SAIR'. Se fim, faz o logout do cliente.
            running = False
            server.close()
        else:
            server.send(texto.encode("utf-8"))#Envia o usuário e a mensagem

# Função para receber as mensagens.
def recebe():
    while True:
        try:
            message = server.recv(2048).decode("utf-8")
            print(f"{message.upper()}")
        except:
            break


t1 = threading.Thread(target=envia)#Criei uma thread para enviar
t2 = threading.Thread(target=recebe)#A segunda thread é para receber a mensagem
t1.start() #Começa a thread de enviar
t2.start() #Começa a thread de receber
t1.join() #bloqueia a thread atual para até a thread alvo terminar
t2.join()

#Apos sair do loop imprime a mensagem abaixo e fecha o cliente.
print("Logout realizado com sucesso.")
server.close()
