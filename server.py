import socket
import argparse
import os
import sys

READY = "READY"
READY_ACK = "READY ACK"
BYE = "bye"
ENCODING = 'utf-8'

def start_server(host, port):
  # Cria o socket TCP/IP
  server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
  server_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
  bind_host = host if host != '0.0.0.0' and host != 'localhost' else '::'

  try:
    # Associa o socket ao endereço e porta
    server_socket.bind((bind_host, port, 0, 0))
    print(f"Servidor iniciado em {host}:{port}")

    # Habilita o servidor a ouvir conexões
    server_socket.listen(1)
    print("Aguardando conexões...")

    # Loop principal para aceitar múltiplas conexões
    while True:
      client_socket, client_address = server_socket.accept()
      print(f"\nConexão estabelecida com {client_address}")

      try:          
        # 1. Recebe 'READY' do cliente
        message = client_socket.recv(1024).decode(ENCODING).strip()
        if message != READY:
          print(f"Protocolo falhou. Esperado '{READY}', Recebido: {message}")
          continue
        print(f"Cliente: {message}")

        # 2. Envia 'READY ACK'
        client_socket.sendall(READY_ACK.encode(ENCODING))
        print(f"Servidor: {READY_ACK}")
                
        # 3. Recebe o nome do diretório
        dir_name_bytes = client_socket.recv(1024)
        if not dir_name_bytes:
          print("Conexão encerrada prematuramente pelo cliente.")
          continue
                    
        dir_name = dir_name_bytes.decode(ENCODING).strip()
        print(f"Cliente requisitou o diretório: '{dir_name}'")
                
        # Processamento e Envio da Lista de Arquivos
        if os.path.isdir(dir_name):
          file_list = os.listdir(dir_name)
          response_data = "\n".join(file_list)

          if response_data:
            response_data += "\n"
          
          response_bytes = response_data.encode(ENCODING)
                    
          # Envia a lista de arquivos
          client_socket.sendall(response_bytes)
          print(f"Enviado {len(response_bytes)} bytes (lista de arquivos de '{dir_name}').")
          client_socket.shutdown(socket.SHUT_WR)
                    
        else:
          error_message = f"ERRO: O diretório '{dir_name}' não foi encontrado."
          client_socket.sendall(error_message.encode(ENCODING))
          client_socket.shutdown(socket.SHUT_WR) # Fechar envio mesmo no erro
          print(error_message)


        try:
          # Tenta receber o 'bye'
          bye_message = client_socket.recv(1024) 
          if bye_message.decode(ENCODING).strip() == BYE:
            print(f"Cliente: {BYE}. Conexão encerrada pelo cliente.")
          elif not bye_message:
            print("Cliente encerrou a conexão (socket fechado).")
          else:
            print(f"Recebido dado residual do cliente: {bye_message.decode(ENCODING).strip()}")
        except ConnectionResetError:
          print("Cliente encerrou a conexão (reset).")
        except Exception as e:
          print(f"Erro ao receber encerramento do cliente: {e}")
      finally:
        client_socket.close()

  except KeyboardInterrupt:
    print("\nServidor encerrado por interrupção do usuário.")
  except Exception as e:
    print(f"Erro fatal do servidor: {e}")
  finally:
    server_socket.close()


if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    description="Iniciar um servidor TCP/IP para listagem de diretórios e medição de throughput.",
    usage='%(prog)s <host> <port>'
  )
  parser.add_argument("host", type=str, help="O endereço do servidor (e.g., 'localhost' ou '0.0.0.0').")
  parser.add_argument("port", type=int, help="A porta do servidor (inteiro entre 1 e 65535).")
  args = parser.parse_args()
    
  start_server(args.host, args.port)