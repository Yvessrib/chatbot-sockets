from socket import *

PortaServidor = 12000 # Porta do servidor

# Criação do socket UDP e configuração do servidor
SocketServidor = socket(AF_INET, SOCK_DGRAM)
SocketServidor.bind(('', PortaServidor))  # Vincula o socket porta especificada
SocketServidor.settimeout(1000)  # Define um timeout de 1000 segundos para o socket

clientes = {} # Dicionário para armazenar o estado de cada cliente

# Definição dos estados do diálogo
MENU = "MENU"
CONTA_CORRENTE = "CONTA_CORRENTE"
CONTA_SALARIO = "CONTA_SALARIO"
ENCERRAR = "ENCERRAR"

# Mensagem inicial enviada ao cliente quando ele se conecta
mensagem_inicial = "Bem-vindo ao Banco do Brasil. Selecione uma opção: 1 para conta corrente, 2 para conta salário ou 3 para encerrar."

print("Server Ready")

# Loop principal do servidor
while True:
    try:
        # Recebe a mensagem do cliente
        mensagem, EnderecoCliente = SocketServidor.recvfrom(1024)
        mensagem_recebida = mensagem.decode('utf-8')
        print(f"Recebido do cliente: {EnderecoCliente}", mensagem_recebida)

        # Verifica se o cliente já está no dicionário de clientes
        if EnderecoCliente not in clientes:
            # Se não estiver, adiciona o cliente ao dicionário com o estado inicial MENU
            clientes[EnderecoCliente] = {"estado": MENU, "historico": []}
            print("Cliente adicionado")
            # Envia a mensagem inicial ao cliente
            SocketServidor.sendto(mensagem_inicial.encode('utf-8'), EnderecoCliente)
            continue  # Pula para a próxima iteração do loop

        # Armazena a mensagem recebida no histórico do cliente
        clientes[EnderecoCliente]["historico"].append(mensagem_recebida)

        # Obtém o estado atual do cliente
        estado_atual = clientes[EnderecoCliente]["estado"]
        resposta = ""

        # Lógica de estados
        if estado_atual == MENU:
            if mensagem_recebida == "1":
                resposta = "Você selecionou conta corrente. Seu saldo é R$ 2.500,00. Digite 3 para retornar ao menu."
                clientes[EnderecoCliente]["estado"] = CONTA_CORRENTE  # Transição para o estado CONTA_CORRENTE

            elif mensagem_recebida == "2":
                resposta = "Você selecionou conta salário. Seu saldo é R$ 1.200,00. Digite 3 para retornar ao menu."
                clientes[EnderecoCliente]["estado"] = CONTA_SALARIO  # Transição para o estado CONTA_SALARIO

            elif mensagem_recebida == "3":
                clientes[EnderecoCliente]["estado"] = ENCERRAR  # Transição para o estado ENCERRAR
                resposta = "\n\tEncerrando o atendimento. Obrigado por utilizar o Banco do Brasil!"

            else:
                resposta = "Opção inválida. Por favor, digite 1 para conta corrente, 2 para conta salário, ou 3 para encerrar."

        elif estado_atual == CONTA_CORRENTE:
            if mensagem_recebida == "3":
                clientes[EnderecoCliente]["estado"] = MENU  # Volta para o estado MENU
                resposta = mensagem_inicial  # Envia a mensagem inicial novamente
            else:
                resposta = "Opção inválida. Digite 3 para voltar ao menu."

        elif estado_atual == CONTA_SALARIO:
            if mensagem_recebida == "3":
                clientes[EnderecoCliente]["estado"] = MENU  # Volta para o estado MENU
                resposta = mensagem_inicial  # Envia a mensagem inicial novamente
            else:
                resposta = "Opção inválida. Digite 3 para voltar ao menu."

        elif estado_atual == ENCERRAR:
            resposta = "\n\tEncerrando o atendimento. Obrigado por utilizar o Banco do Brasil!"
            SocketServidor.close()  # Fecha o socket do servidor ao encerrar o atendimento

        # Envia a resposta ao cliente
        SocketServidor.sendto(resposta.encode('utf-8'), EnderecoCliente)

        # Exibe o histórico de mensagens com o cliente no terminal
        print(f"Histórico com {EnderecoCliente}: {clientes[EnderecoCliente]['historico']}")

    except timeout:
        # Tratamento de timeout, indicando que nenhuma mensagem foi recebida dentro do tempo limite
        print("Timeout. Nenhuma mensagem recebida do cliente.")
