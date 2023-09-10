#Para executar rode o server.py primeiro. Então abra dois terminais e digite python client.py. 
# Isso vai possibilitar o uso do chat por mais de um usuário simultaneamente.
import socket
import datetime
from _thread import *
users_list = []

def serverthread(conn,addr):
    running = True
    list_msg = []
    while running:
        try:
            message = conn.recv(2048).decode("utf-8") #Recebe a mensagem
            if message:
                my_array = message.split("|") # cria um array separando a mensagem e o nome de usuario com |
                now = datetime.datetime.now()
                msg_retorno = ''
                if my_array[1].upper() == "@ORDENAR": #Array que na posição 1 consta a mensagem. Se o usuário digitar @ORDENAR vai mostrar as últimas 15 mensagens, ordenadas pelo horário de envio
                    for i in range(15): #Delimita em 15 para mostrar só 15 mensagens
                        iArray = len(list_msg)-(i+1)
                        msg_retorno += str(i+1) + ' - ' + list_msg[iArray][0].strftime("%Y/%m/%d, %H:%M:%S") + ' - ' + list_msg[iArray][1] + ' :: ' + list_msg[iArray][2] + '\n'
                        if iArray == 0:
                            break
                    sendMessageMe(conn, msg_retorno)
                    #Vai retornar o dia/hora da mensagem, o usuário que escreveu e qual foi a mensagem.
                elif my_array[1].upper() == "@UPLOAD": #Opção de Upload de arquivo para o cliente
                    msg_retorno = "Upload realizado com sucesso."
                    sendMessageMe(conn, msg_retorno)
                elif my_array[1].upper() == "@DOWNLOAD": #Opção de download de arquivo para o cliente.
                    msg_retorno = 'Download completado com sucesso!'
                    sendMessageMe(conn, msg_retorno)
                else:
                    list_msg.append([now, my_array[0], my_array[1]]) #É adicionado na lista o tempo do momento da mensagem, o usuário e a mensagem.
                    msg_retorno = my_array[0] + "::" + my_array[1] #Mostra a mensagem no formato User :: Mensagem
                    sendMessageUsers(conn, msg_retorno)
        except:
            continue

def sendMessageUsers(connection,msg_retorno): # Essa função é para retornar a mensagem para todos os usuarios logados no chat
    for user in users_list:
        if user != connection:
            try:
                user.send(msg_retorno.encode("utf-8"))
            except:
                user.close()
                if user in users_list:
                    users_list.remove(connection)


def sendMessageMe(connection,msg_retorno): # Essa função é para retornar a mensagem apenas para o usuario atual
    for user in users_list:
        if user == connection:
            try:
                user.send(msg_retorno.encode("utf-8"))
            except:
                user.close()
                if user in users_list:
                    users_list.remove(connection)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8888))
server.listen()

while True:
    conn, addr = server.accept()
    users_list.append(conn) #Adiciona na lista de usuários a conn
    print(addr[0] + " connected")
    start_new_thread(serverthread,(conn,addr)) #Começo uma thread


conn.close()
server.close()

#O programa tem uma arquitetura de cliente-servidor.
