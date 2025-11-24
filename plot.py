import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("resultados_throughput.csv")

df['Throughput_MB_s'] = df['Throughput_Bytes_s'] / (1024 * 1024)
df['Tempo_Medio_s'] = df['Tempo_Medio_s'].astype(float)
df['Desvio_Padrao_s'] = df['Desvio_Padrao_s'].astype(float)
df['Erro_MB_s'] = (df['Throughput_Bytes_s'] * (df['Desvio_Padrao_s'] / df['Tempo_Medio_s'].replace(0, np.nan))) / (1024 * 1024)

df_plot = df.dropna(subset=['Erro_MB_s', 'Throughput_MB_s']).copy()

plt.figure(figsize=(10, 6))
protocols = df_plot['Protocolo'].unique()
markers = {'IPv4': 'o', 'IPv6': 's'}
colors = {'IPv4': 'C0', 'IPv6': 'C1'}

for protocol in protocols:
  subset = df_plot[df_plot['Protocolo'] == protocol]
    
  plt.plot(
    subset['Tamanho_Bytes'],
    subset['Throughput_MB_s'],
    label=protocol,
    linestyle='-',
    color=colors[protocol]
  )
    
  plt.scatter(
    subset['Tamanho_Bytes'],
    subset['Throughput_MB_s'],
    marker=markers[protocol],
    s=50,
    color=colors[protocol]
  )
    
  plt.errorbar(
    subset['Tamanho_Bytes'],
    subset['Throughput_MB_s'],
    yerr=subset['Erro_MB_s'],
    fmt='none',
    capsize=4,
    color=colors[protocol],
    alpha=0.6
  )

plt.xscale('log', base=2)
plt.xlabel('Tamanho da Mensagem [Bytes]')
plt.ylabel('Throughput Médio [MB/s]')
plt.title('Figura 1 - Throughput vs. Tamanho da Mensagem (IPv4 vs. IPv6)')
plt.legend(title='Protocolo')
plt.grid(True, which="both", ls="--", linewidth=0.5)
plt.savefig('throughput_tamanho.png')