import time
import requests

API_URL = "https://lynxmetrics.com/apis/bacbo-live/latest" # Exemplo de endpoint
historico_recente = []

def checar_novos_resultados():
    try:
        response = requests.get(API_URL, timeout=5)
        if response.status_code == 200:
            dados = response.json()
            # Supondo que o JSON traga o ID da rodada e o vencedor ("player", "banker" ou "tie")
            rodada_id = dados.get("round_id")
            vencedor = dados.get("winner") 
            
            # Evita duplicatas checando se é uma rodada nova
            if not historico_recente or historico_recente[-1]["id"] != rodada_id:
                historico_recente.append({"id": rodada_id, "winner": vencedor})
                
                # Mantém apenas os últimos 50 resultados na memória
                if len(historico_recente) > 50:
                    historico_recente.pop(0)
                    
                analisar_padroes_e_alertar(historico_recente)
        else:
            print("Erro ao consultar a API:", response.status_code)
    except Exception as e:
        print("Erro de conexão:", e)

def analisar_padroes_e_alertar(historico):
    if len(historico) < 4:
        return
    
    # Exemplo de regra simples: 4 repetições seguidas do mesmo lado
    ultimos_quatro = [r["winner"] for r in historico[-4:]]
    if all(w == ultimos_quatro[0] for w in ultimos_quatro):
        enviar_alerta_telegram(f"🚨 Alerta de Padrão! 4 seguidas no: {ultimos_quatro[0].upper()}")

def enviar_alerta_telegram(mensagem):
    # Insira seu token de Bot do Telegram e o Chat ID aqui
    print(f"[ALERTA DISPARADO]: {mensagem}")

# Loop principal de monitoramento (executa a cada 5 segundos)
if __name__ == "__main__":
    print("Iniciando monitor do Bac Bo...")
    while True:
        checar_novos_resultados()
        time.sleep(5)
