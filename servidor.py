import socket
import threading
import queue
import keyboard
import os

# Configurações do servidor
HOST = '127.0.0.1'
PORT = 65432

# Fila de processos
fila = queue.Queue()
token = True  # Inicialmente, o token está disponível
contador = 0  # Contador compartilhado
contador_espera = 0  # Contador de espera
conexoes = []  # Lista para armazenar todas as conexões ativas
servidor_ativo = True

def gerenciar_token(conn, addr):
    global token, contador, contador_espera
    conexoes.append(conn)
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            if data == 'REQUEST':
                fila.put((conn, addr))
                contador_espera += 1
                print(f'[SOLICITAÇÃO] Cliente {addr} solicitou o token. Contador de espera: {contador_espera}')
                if token:
                    enviar_token()
            elif data == 'RELEASE':
                contador += 1  # Incrementa o contador quando o token é liberado
                token = True
                print(f'[LIBERAÇÃO] Token liberado pelo cliente {addr}. Contador: {contador}')
                if not fila.empty():
                    enviar_token()
            elif data == 'STATUS':
                conn.sendall(f'STATUS {contador} {contador_espera}'.encode())
    except Exception as e:
        print(f'[ERRO] Erro ao gerenciar token para o cliente {addr}: {e}')
    finally:
        try:
            conn.close()
            conexoes.remove(conn)
        except Exception as e:
            print(f'[ERRO] Erro ao fechar a conexão para o cliente {addr}: {e}')

def enviar_token():
    global token, contador_espera
    if not fila.empty():
        next_conn, next_addr = fila.get()
        token = False
        contador_espera -= 1
        next_conn.sendall(f'TOKEN {contador} {contador_espera}'.encode())
        print(f'[ENVIO] Token enviado para o cliente {next_addr}. Contador: {contador}, Contador de espera: {contador_espera}')

def iniciar_servidor():
    global servidor_ativo
    servidor_ativo = True
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f'Servidor iniciado em {HOST}:{PORT}')
        threading.Thread(target=monitorar_teclas).start()
        while servidor_ativo:
            try:
                conn, addr = s.accept()
                threading.Thread(target=gerenciar_token, args=(conn, addr)).start()
            except Exception as e:
                if servidor_ativo:
                    print(f'[ERRO] Erro ao aceitar conexão: {e}')

def monitorar_teclas():
    keyboard.add_hotkey('esc', fechar_conexoes)
    keyboard.add_hotkey('f5', reiniciar_servidor)
    keyboard.wait()

def fechar_conexoes():
    global servidor_ativo
    servidor_ativo = False
    print('Fechando todas as conexões...')
    for conn in conexoes:
        try:
            conn.close()
        except Exception as e:
            print(f'[ERRO] Erro ao fechar a conexão: {e}')
    print('Todas as conexões foram fechadas.')

def reiniciar_servidor():
    global servidor_ativo
    if not servidor_ativo:
        print('Reiniciando o servidor...')
        threading.Thread(target=iniciar_servidor).start()

if __name__ == "__main__":
    iniciar_servidor()