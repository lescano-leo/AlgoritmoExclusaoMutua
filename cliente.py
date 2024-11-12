import socket
import threading
import time
import os

# Configurações do cliente
HOST = '127.0.0.1'
PORT = 65432

status_clientes = {}
lock = threading.Lock()  # Lock para garantir a integridade da tela

def solicitar_token(cliente_id):
    global status_clientes
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            while True:
                sock.sendall(b'REQUEST')
                data = sock.recv(1024).decode()
                if data.startswith('TOKEN'):
                    _, contador, contador_espera = data.split()
                    status_clientes[cliente_id] = f'Tokenizin. Contador: {contador}, Contador de espera: {contador_espera}'
                    atualizar_tela()
                    time.sleep(5)  # Simula o uso do token
                    sock.sendall(b'RELEASE')
                    status_clientes[cliente_id] = 'Token liberado.'
                    atualizar_tela()
                    break
                else:
                    status_clientes[cliente_id] = 'Aguardando token...'
                    atualizar_tela()
                    time.sleep(2)  # Aguarda 2 segundos antes de solicitar novamente
    except Exception as e:
        status_clientes[cliente_id] = f'Erro ao solicitar token: {e}'
        atualizar_tela()

def atualizar_status(cliente_id):
    global status_clientes
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            while True:
                sock.sendall(b'STATUS')
                data = sock.recv(1024).decode()
                if data.startswith('STATUS'):
                    _, contador, contador_espera = data.split()
                    if status_clientes[cliente_id].startswith('Tokenizin'):
                        status_clientes[cliente_id] = f'Tokenizin. Contador: {contador}, Contador de espera: {contador_espera}'
                    else:
                        status_clientes[cliente_id] = f'Status atualizado. Contador: {contador}, Contador de espera: {contador_espera}'
                    atualizar_tela()
                time.sleep(5)  # Atualiza o status a cada 5 segundos
    except Exception as e:
        status_clientes[cliente_id] = f'Erro ao atualizar status: {e}'
        atualizar_tela()

def atualizar_tela():
    # Função para atualizar a tela de forma segura
    with lock:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== Status dos Clientes ===")
        for cliente_id, status in status_clientes.items():
            print(f'Cliente {cliente_id}: {status}')

def iniciar_cliente(cliente_id):
    threading.Thread(target=solicitar_token, args=(cliente_id,)).start()
    threading.Thread(target=atualizar_status, args=(cliente_id,)).start()

if __name__ == "__main__":
    num_clientes = 5  # Número de clientes a serem simulados
    for i in range(num_clientes):
        status_clientes[i] = 'Iniciando...'
        iniciar_cliente(i)
    while True:
        time.sleep(1)  # Mantém o script principal rodando