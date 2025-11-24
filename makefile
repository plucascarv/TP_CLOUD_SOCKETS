# Variáveis de configuração
host = localhost
port = 12345

test_bank_dir = test_bank
output_dir = client_results
results_file = resultados_throughput.csv
plot_file = throughput_tamanho.png

# Execução do projeto
all: plot
	@echo "Projeto realizado com sucesso. Resultados em: $(results_file) e $(plot_file)"

setup:
	@echo "Configurando ambiente de teste"
	@python create_tests.py

server:
	@echo "Iniciando o servidor em $(host):$(port)"
	@python server.py $(host) $(port)

test: setup
	@echo "Executando os testes e coletando os dados"
	@python run_tests.py

plot: test
	@echo "Gerando gráfico de desempenho"
	@python plot.py

# Limpeza de arquivos
data_clean:
	@echo "Limpando arquivos de resultados"
	-rm -f $(results_file)
	-rm -f $(plot_file)
	-rm -rf $(output_dir)
	-find . -name "*.txt" -delete

clean: data_clean
	@echo "Realizando limpeza completa do ambiente de teste"
	-rm -rf $(test_bank_dir)
	-rm -rf __pycache__
	-find . -name "*.pyc" -delete