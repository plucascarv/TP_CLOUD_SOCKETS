import socket
import argparse
import time
import sys
import os

READY = "READY"
READY_ACK = "READY ACK"
BYE = "bye"
ENCODING = 'utf-8'
OUTPUT_DIR = "client_results"

def start_client(host, port, directory):
  if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print(f"Criado diretório de saída: {OUTPUT_DIR}/")

  client_socket = None  
  # 1. Obter informações do endereço
  try:
    addrinfo = socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM)
  except socket.gaierror as e:
    print(f"Erro ao obter informações do endereço: {e}")
    return
  print(f"Tentando conectar a {host}:{port} e requisitar diretório '{directory}'...")
  
  # 2. Tenta a conexão
  for res in addrinfo:
    family, socktype, proto, _, sa = res

    try:
      # 3. Cria o socket e tenta conectar
      client_socket = socket.socket(family, socktype, proto)
      client_socket.connect(sa)

      connect_host = sa[0] if family == socket.AF_INET else f"[{sa[0]}]"
      print(f"Conectado ao servidor em {connect_host}:{sa[1]} ({'IPv6' if family == socket.AF_INET6 else 'IPv4'})")
      break
    except OSError as msg:
      print(f"Falha ao tentar conectar a {sa}: {msg}")
      if client_socket:
        client_socket.close()
        client_socket = None
        continue
  
  if client_socket is None:
    print("Erro: não foi possível conectar ao servidor!")
    return
  
  total_bytes_received = 0
  start_time = 0
  end_time = 0

  try:
    # Processo de comunicação
    client_socket.sendall(READY.encode(ENCODING))
    ack_message = client_socket.recv(1024).decode(ENCODING).strip()

    if ack_message != READY_ACK:
      print(f"Protocolo falhou. Esperado '{READY_ACK}', Recebido: {ack_message}")
      return
    print(f"Servidor: {READY_ACK}")

    client_socket.sendall(directory.encode(ENCODING))
    start_time = time.perf_counter()

    received_data = b""
    while True:
      chunk = client_socket.recv(4096)
      if not chunk:
        break
                
      received_data += chunk
      total_bytes_received += len(chunk)
    end_time = time.perf_counter()
        
    # Fechamento e Cálculo de Desempenho
    client_socket.sendall(BYE.encode(ENCODING))
    received_content = received_data.decode(ENCODING)
    
    if host == "::1":
      safe_host = "IPv6"
    elif host == "127.0.0.1":
      safe_host = "IPv4"
    else:
      safe_host = host
        
    output_filename_base = f"lista_de_arquivos_{safe_host}_{port}_{directory}"
    safe_filename = output_filename_base.replace('/', '_').replace(':', '_').replace('\\', '_')
    output_filename = os.path.join(OUTPUT_DIR, f"{safe_filename}.txt")

    with open(output_filename, 'w', encoding=ENCODING) as f:
      f.write(received_content)
    print(f"\nLista de arquivos recebida ({total_bytes_received} bytes) e salva em '{output_filename}'.")
        
    # Calcula o Tempo Gasto e Throughput
    time_elapsed = end_time - start_time
        
    if time_elapsed > 0:
      throughput = total_bytes_received / time_elapsed
            
      # Formatação da saída
      print("-" * 50)
      print("  Resultados das Medições de Desempenho")
      print(f"  Tamanho Total Transferido: {total_bytes_received} bytes")
      print(f"  Tempo Gasto na Transferência: {time_elapsed:.6f} segundos")
      print(f"  Throughput (MB/s): {throughput / (1024 * 1024):.2f} MB/s")
      print("-" * 50)

    else:
      print("Tempo gasto foi zero ou negativo. Não é possível calcular o Throughput.")


  except ConnectionRefusedError:
    print(f"Erro: Conexão recusada. Certifique-se de que o servidor está rodando em {host}:{port}.")
  except Exception as e:
    print(f"Erro durante a comunicação: {e}")
  finally:
    # Fecha a conexão
    client_socket.close()
    print("Conexão fechada.")


if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    description="Iniciar um cliente TCP/IP para listagem de diretórios e medição de throughput.",
    usage='%(prog)s <host> <port> <directory>'
  )
  parser.add_argument("host", type=str, help="O endereço do servidor (e.g., 'localhost' ou um IP).")
  parser.add_argument("port", type=int, help="A porta do servidor (inteiro entre 1 e 65535).")
  parser.add_argument("directory", type=str, help="O nome do diretório a ser requisitado no servidor.")
  args = parser.parse_args()
    
  start_client(args.host, args.port, args.directory)