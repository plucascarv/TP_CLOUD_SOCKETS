import os
import shutil
import math
import time

START_POWER = 1
END_POWER = 16
MAX_NAME_LENGTH = 250
MIN_NAME_LENGTH = 1
TEST_BANK_DIR = "test_bank"

def create_test_directories():
  print(f"Iniciando a criação de diretórios de teste ({2**START_POWER} bytes a {2**END_POWER} bytes)...")

  if os.path.exists(TEST_BANK_DIR):
    shutil.rmtree(TEST_BANK_DIR)
  os.makedirs(TEST_BANK_DIR)
  
  successful_tests = 0

  for i in range(START_POWER, END_POWER + 1):
    dir_name_base = f"test_{i}"
    dir_name = os.path.join(TEST_BANK_DIR, dir_name_base)
    target_size = 2 ** i
    
    try:
      ITEM_SIZE_MAX_USEFUL = MAX_NAME_LENGTH + 1
      num_files = math.ceil(target_size / ITEM_SIZE_MAX_USEFUL)

      total_overhead = num_files
      total_payload = target_size - total_overhead 
      base_length = total_payload // num_files
      remainder = total_payload % num_files
      
      lengths = []
      for _ in range(remainder):
        lengths.append(base_length + 1)
      for _ in range(num_files - remainder):
        lengths.append(base_length)
      
      if min(lengths) < MIN_NAME_LENGTH:
        raise ValueError("Payload insuficiente para este número de arquivos.")

      os.makedirs(dir_name)
      
      for k, length in enumerate(lengths):
        index_str = str(k)
        padding_len = length - len(index_str)
        file_name = index_str + ('a' * padding_len)
        
        if len(file_name) > MAX_NAME_LENGTH:
          raise ValueError(f"Comprimento do nome de arquivo {length} excede o limite {MAX_NAME_LENGTH}.")
        file_path = os.path.join(dir_name, file_name)
        
        with open(file_path, 'w') as f:
          pass
        time.sleep(0.001) 

      print(f"Criado diretório '{dir_name}' (i={i}).")
      print(f"  -> N° de Arquivos: {num_files}")
      print(f"  -> Tamanho Total Enviado: {target_size} bytes (Target: {target_size} bytes).")
      successful_tests += 1
      
    except Exception as e:
      print(f"Erro CRÍTICO ao criar arquivos para i={i}: {e}")
      break     
  print(f"\nCriação dos diretórios de teste concluída. {successful_tests} casos criados com sucesso.")

if __name__ == "__main__":
  create_test_directories()