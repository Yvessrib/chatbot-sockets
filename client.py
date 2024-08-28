from socket import *

# Endereço do Servidor
servername = 'localhost'  # Definição do endereço do servidor (localhost para testes locais)
serverPort = 12000  # Definição da porta do servidor
clientSocket = None  # Variável global para o socket do cliente


def send_message(message: str):
    global clientSocket
    # Envia a mensagem codificada para o servidor
    clientSocket.sendto(message.encode('utf-8'), (servername, serverPort))
    # Recebe a resposta do servidor
    modified_sentence, server_address = clientSocket.recvfrom(1024)
    resposta = modified_sentence.decode('utf-8')  # Decodifica a resposta recebida
    print("\n" + resposta)  # Exibe a resposta no console
    return resposta  # Retorna a resposta para uso no loop principal


def main():
    global clientSocket
    # Criação do socket UDP (AF_INET indica IPv4, SOCK_DGRAM indica UDP)
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(1000)  # Define um timeout de 1000 segundos para operações de rede

    # Mensagem inicial para o usuário
    input('Pressione qualquer tecla para iniciar a conversa...')

    # Envia uma mensagem inicial ao servidor para iniciar a conversa e receber a mensagem de boas-vindas
    resposta = send_message("")

    # Loop principal para interação contínua com o servidor
    while True:
        # Verifica se a resposta do servidor indica o encerramento do chat
        if "Encerrando o chat. Obrigado!" in resposta:
            break  # Sai do loop se o chat foi encerrado

        # Solicita ao usuário que insira uma opção e a envia ao servidor
        sentence = input('\nDigite sua opção: ')
        resposta = send_message(sentence)  # Envia a opção e recebe a nova resposta do servidor

    clientSocket.close()  # Fecha o socket ao encerrar a comunicação


if __name__ == "__main__":
    main()  # Chama a função principal para iniciar o cliente
