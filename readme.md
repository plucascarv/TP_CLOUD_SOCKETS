# Sistema Cliente-Servidor de Transferência de Diretórios (TCP/IPv4/IPv6)

Este repositório armazena os códigos para um projeto que implementa um sistema de comunicação cliente-servidor para demonstrar e avaliar o desempenho de transferência de informações de diretórios no contexto da **Computação em Nuvem**. Este projete foi desenvolvido como parte da avaliação da matéria MATA59 - Redes de Computadores na Universidade Federal da Bahia.

-----

## 1\. Objetivo do Projeto

O objetivo principal é construir uma aplicação **robusta** de comunicação de requisição-resposta que seja compatível com **IPv4** e **IPv6**, e, em seguida, submetê-la a uma avaliação de desempenho para medir a taxa de transferência (*throughput*).

### Tecnologias Principais

  * **Linguagem:** Python 3.x
  * **Protocolo:** TCP
  * **Compatibilidade:** Implementação de Sockets **Dual-Stack** (IPv4/IPv6)
  * **Análise:** Pandas, Matplotlib, NumPy

-----

## 2\. Operação e Protocolo

O sistema executa um processo de transferência de metadados de diretório, onde o cliente solicita uma lista de arquivos de um diretório específico ao servidor.

### Fluxo de Comunicação

O processo de comunicação segue o padrão **READY/ACK** para sincronização e medição:

1.  **Conexão:** O Cliente se conecta ao Servidor (via IPv4 ou IPv6).
2.  **Handshake:** O Cliente envia **"READY"** e o Servidor responde com **"READY ACK"**.
3.  **Requisição:** O Cliente envia o caminho do diretório desejado (ex: `test_reservoir/test_1`).
4.  **Transferência:** O Servidor lista os arquivos e envia os nomes, concatenados com um terminador.
5.  **Medição:** O Cliente mede o tempo gasto desde o envio da requisição até o recebimento do último byte.
6.  **Encerramento:** O Cliente envia **"bye"** e fecha a conexão.

-----

## 3\. Avaliação de Desempenho

A principal métrica de avaliação é o **Throughput** ($\bar{B}$), medido em **Bytes/s** no lado do cliente.

$$\text{Throughput} = \frac{\text{Número total de bytes enviados}}{\text{Tempo médio medido no cliente}}$$

Os testes abrangem 16 casos, com o tamanho da mensagem variando em potências de **$2^i$ bytes ($i=1$ a $16$)**, permitindo analisar o impacto do *overhead* em diferentes escalas de carga útil.

-----

## 4\. Pré-requisitos e Uso

Este projeto utiliza um `Makefile` para automatizar todas as etapas de configuração e execução.

### Pré-requisitos

Certifique-se de que você tem o Python 3.x e as bibliotecas de análise instaladas:

```bash
# 1. Instalar as bibliotecas essenciais (para análise e visualização)
python -m pip install pandas matplotlib numpy
```

### Execução Completa (Usando `Makefile`)

Execute o servidor em uma janela e o teste na outra.

| Comando | Descrição |
| :--- | :--- |
| `make setup` | **Cria** os diretórios de teste (`test_bank/test_1` até `test_16`) com o número exato de bytes. |
| `make server` | **Inicia** o `server.py` no `localhost:12345`. (Deve rodar em um terminal separado). |
| `make test` | **Roda a bateria de testes** (10 repetições por caso/protocolo) e salva os resultados em `resultados_throughput.csv`. |
| `make plot` | **Gera o gráfico** de Throughput (`throughput_tamanho.png`) a partir dos dados do CSV. |
| `make all` | Executa `setup`, `test`, e `plot` sequencialmente. |
| `make clean` | Remove todos os arquivos gerados (`.csv`, `.png`, `client_results/`, `test_bank/`). |

-----

## 5\. Estrutura do Repositório

| Arquivo/Pasta | Função |
| :--- | :--- |
| `server.py` | Implementação do servidor TCP Dual-Stack. |
| `client.py` | Implementação do cliente TCP, lógica do protocolo e cálculo do tempo. |
| `run_tests.py` | Automatiza 320 execuções, coleta o tempo bruto e calcula as estatísticas. |
| `create_tests.py` | Gera os diretórios de teste, garantindo o tamanho exato de $2^i$ bytes no *payload* transferido. |
| `plot.py` | Código para gerar o gráfico final de Throughput. |
| `Makefile` | Script de automação para gerenciar o projeto. |

É importante comentar que os arquivos referentes ao diretórios de teste e resultados da execução de client.py não puderam ser adicionados devido ao tamanho dos nomes destes. No entanto, eles são automaticamente gerados durante a execução dos códigos. Com a ressalva de que é necessário criar manualmente o diretório 'test_0' - completamente vazio -, para que a execução siga exatamente os mesmos elementos que a original.