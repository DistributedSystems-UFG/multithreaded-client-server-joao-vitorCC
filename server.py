from socket  import *
from constCS import * #-
import threading
import math
import time

def lidar_com_cliente(conexao, endereco):
	print(f"Conectado com: {addr[0]}")
	while True:                # forever
		data = conn.recv(1024)   # receive data from client
		if not data: break       # stop if client stopped
		comando = data.decode().strip()
		time.sleep(2)
		if comando.startswith("RAIZ"):
			resposta = calcular_raiz(comando)
		elif comando.startswith("INVERTE"):
			resposta = inverter_texto(comando)
		elif comando.startswith("SOMA"):
			resposta = somar_valores(comando)	
		else:
			resposta = "Comando não reconhecido. Use RAIZ ou INVERTE."
		#print(bytes.decode(data))
	conn.send(f"{resposta}\n".encode())
#conn.send(str.encode(bytes.decode(data)+"*")) # return sent data plus an "*"
	conn.close()               # close the connect
    
def iniciar_servidor():
    servidor = socket(AF_INET, SOCK_STREAM)
    servidor.bind(('0.0.0.0', port)) # Ouve em todas as interfaces na porta 5050
    servidor.listen()
    print("[ESCUTANDO] Servidor aguardando conexões...")

    while True:
        # Aceita nova conexão (bloqueia aqui até alguém conectar)
        conn, addr = servidor.accept()
        # Cria uma thread dedicada para o novo cliente
        thread = threading.Thread(target=lidar_com_cliente, args=(conn, addr))
        thread.start()
        print(f"[CONEXÕES ATIVAS] {threading.active_count() - 1}")    

def somar_valores(dados):
    partes = dados.split()
    
    # Verifica se enviou a quantidade certa de argumentos
    if len(partes) != 3:
        return "Erro: Use SOMA <num1> <num2>"
    
    try:
        # Tenta converter as strings para números (float aceita decimais)
        n1 = float(partes[1])
        n2 = float(partes[2])
        res = n1 + n2
        return f"Resultado da soma: {res}"
    except ValueError:
        # Se o usuário digitou letras em vez de números, cai aqui
        return "Erro: Os valores fornecidos devem ser números válidos."

def calcular_raiz(comando):
    """Calcula raiz quadrada: 'RAIZ 25' -> 5.0"""
    partes = comando.split()
    
    if len(partes) != 2:
        return "Erro: Use RAIZ <numero>"
    
    try:
        valor = float(partes[1])
        if valor < 0:
            return "Erro: Não existe raiz quadrada real de número negativo."
        return f"A raiz de {valor} é {math.sqrt(valor)}"
    except ValueError:
        return "Erro: O valor para a raiz deve ser um número."
        
def inverter_texto(dados):
    # Exemplo: cliente envia "INVERTE ola mundo"
    # Pega tudo após a palavra 'INVERTE '
    texto = dados[8:] 
    return f"Texto invertido: {texto[::-1]}"

iniciar_servidor()
