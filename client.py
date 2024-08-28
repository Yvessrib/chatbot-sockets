from socket import *

# Endereço do Servidor
servername = 'localhost'  # Teste local
serverPort = 12000  # Definição da porta
clientSocket = None  # Socket do cliente


def send_message(message: str):
    
    global clientSocket
    
    clientSocket.sendto(message.encode('utf-8'), (servername, serverPort)) # Codifica a mensagem que será enviada ao servidor
    
    modified_sentence, server_address = clientSocket.recvfrom(1024)  # Recebe a resposta do servidor
    
    resposta = modified_sentence.decode('utf-8')  # Decodifica a resposta recebida
    
    print("\n" + resposta)  # Exibe a resposta no console
    
    return resposta  # Retorna a resposta para uso no loop principal


def main():
    
    global clientSocket
    
    # Criação do socket UDP (AF_INET indica IPv4, SOCK_DGRAM indica UDP)
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(1000)  # Define um timeout de 1000 segundos para operações de rede
   
    input('Pressione qualquer tecla para iniciar a conversa...') # Mensagem inicial para o usuário

    resposta = send_message("") # Envia uma mensagem inicial ao servidor para iniciar a conversa e receber a mensagem de boas-vindas

    while True:  # Loop principal para interação contínua com o servidor
      
        if "Encerrando o atendiento. Obrigado!" in resposta:  # Verifica se a resposta do servidor indica o encerramento do chat
            break  # Sai do loop se o chat foi encerrado

        sentence = input('\nDigite sua opção: ')  # Solicita ao usuário que insira uma opção e a envia ao servidor
        resposta = send_message(sentence)  # Envia a opção e recebe a nova resposta do servidor

    clientSocket.close()  # Fecha o socket ao encerrar a comunicação


if __name__ == "__main__":
    main()  # Chama a função principal para iniciar o cliente
