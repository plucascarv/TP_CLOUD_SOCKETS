import subprocess
import time
import math
import csv
import re
import os

TEST_POWERS = list(range(0, 17)) 
REPETITIONS = 10 
SERVER_PORT = 12345
TEST_HOSTS = {
  "IPv4": "127.0.0.1",
  "IPv6": "::1"
}
OUTPUT_FILE = "resultados_throughput.csv"
CLIENT_SCRIPT = "client.py"

def calculate_stats(times, total_bytes):
  # Calcula média, desvio padrão e throughput.
  n = len(times)
  
  avg_time = sum(times) / n
  
  if n > 1:
    variance = sum([(t - avg_time) ** 2 for t in times]) / (n - 1)
    std_dev = math.sqrt(variance)
  else:
    std_dev = 0.0
    
  if avg_time > 0:
    avg_throughput_bytes_s = total_bytes / avg_time
  else:
    avg_throughput_bytes_s = 0.0

  return avg_time, std_dev, avg_throughput_bytes_s

def run_single_test(host, port, directory):
  # Executa o cliente e usa regex para extrair o tempo gasto.
  try:
    command = [
      'python', CLIENT_SCRIPT,
      host, str(port), directory
    ]
    
    result = subprocess.run(
      command,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      text=True,
      timeout=30,
    )
    
    full_output = result.stdout + result.stderr
    
    for line in full_output.split('\n'):
      if "Tempo Gasto na Transferência:" in line:
        match = re.search(r'(\d+\.\d+)', line)
        if match:
          return float(match.group(1))
            
    return None
    
  except subprocess.TimeoutExpired:
    print(f"  [ALERTA] Teste para {directory} excedeu o tempo limite.")
    return None
  except Exception as e:
    print(f"  [ERRO GERAL] Falha no subprocesso: {e}")
    return None

def collect_data():
  # Coordena a execução de todos os testes e salva o CSV.
  with open(OUTPUT_FILE, 'w', newline='') as csvfile:
    fieldnames = [
      'i', 
      'Protocolo', 
      'Tamanho_Bytes', 
      'N_Mensagens', 
      'Tempo_Medio_s', 
      'Desvio_Padrao_s', 
      'Throughput_Bytes_s', 
      'Throughput_KB_s',
      'Tempos_Brutos_s'
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    print(f"Iniciando a coleta de dados com {REPETITIONS} repetições por caso...")
    
    for i in TEST_POWERS:
      directory = f"test_reservoir/test_{i}"
      total_bytes = 2 ** i
      
      for protocol, host in TEST_HOSTS.items():
        
        print(f"\n-> Testando {protocol} | {directory} ({total_bytes} bytes)")
        
        times = []
        for r in range(REPETITIONS):
          time.sleep(0.1)
          elapsed_time = run_single_test(host, SERVER_PORT, directory)
          
          if elapsed_time is not None:
            times.append(elapsed_time)
            print(f"  Repetição {r+1}: {elapsed_time:.9f} s")
          else:
            print(f"  Repetição {r+1}: FALHOU")

        if not times:
          print(f"  [AVISO] Dados insuficientes para {protocol} - {directory}.")
          continue

        avg_time, std_dev, avg_throughput = calculate_stats(times, total_bytes)
        raw_times_str = ";".join(f"{t:.9f}" for t in times)
        
        writer.writerow({
          'i': i,
          'Protocolo': protocol,
          'Tamanho_Bytes': total_bytes,
          'N_Mensagens': 1,
          'Tempo_Medio_s': f"{avg_time:.9f}",
          'Desvio_Padrao_s': f"{std_dev:.9f}",
          'Throughput_Bytes_s': f"{avg_throughput:.2f}",
          'Throughput_KB_s': f"{avg_throughput / 1024:.2f}",
          'Tempos_Brutos_s': raw_times_str
        })
        print(f"  RESULTADO FINAL: {avg_throughput / 1024:.2f} KB/s (Std Dev: {std_dev:.6f} s)")

  print(f"\n Coleta de dados concluída. Resultados salvos em {OUTPUT_FILE}")

if __name__ == "__main__":
  if not os.path.exists("test_bank"):
      print("ERRO: A pasta 'test_bank' não foi encontrada. Execute o create_tests.py primeiro.")
  else:
      collect_data()