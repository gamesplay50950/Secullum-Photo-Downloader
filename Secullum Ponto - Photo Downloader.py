import requests
import os
import time
import base64
import csv
from datetime import datetime


AZUL = '\033[94m'
VERDE = '\033[92m'
VERMELHO = '\033[91m'
AMARELO = '\033[93m'
RESET = '\033[0m'

def input_azul(texto):
    return input(f"{AZUL}{texto}{RESET}")

print(f"{AMARELO}=== SECULLUM PHOTO DOWNLOADER ==={RESET}\n")

authorization = input_azul("Authorization (Bearer ...): ").strip()
user_agent = input_azul("User-Agent: ").strip() or "Mozilla/5.0"
referer = input_azul("Referer: ").strip() or "https://pontoweb.secullum.com.br/"
cookies_input = input_azul("Cookies: ").strip()
cookies_dict = {}
if cookies_input:
    for part in cookies_input.split(';'):
        if '=' in part:
            k, v = part.strip().split('=', 1)
            cookies_dict[k] = v

api_funcionario = input_azul("URL do funcionário (com {id}): ").strip()
if "{id}" not in api_funcionario:
    print(f"{VERMELHO}ERRO: use {{id}}{RESET}")
    exit(1)

api_biometria = input_azul("URL da biometria (com {id}): ").strip()
if "{id}" not in api_biometria:
    print(f"{VERMELHO}ERRO: use {{id}}{RESET}")
    exit(1)

while True:
    modo = input_azul("\n[1] CSV | [2] Varredura: ").strip()
    if modo in ["1", "2"]: break

if modo == "1":
    csv_path = input_azul("CSV: ").strip()
    col = input_azul("Coluna ID: ").strip() or "ID"
    with open(csv_path, 'r', encoding='utf-8') as f:
        ids = [row[col].strip() for row in csv.DictReader(f) if row[col]. Matrícula.strip()]
else:
    ini = int(input_azul("ID inicial: "))
    fim = int(input_azul("ID final: "))
    ids = [str(i) for i in range(ini, fim + 1)]


os.makedirs('fotos_colaboradores', exist_ok=True)
log_file = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

session = requests.Session()
session.headers.update({
    'Authorization': authorization,
    'User-Agent': user_agent,
    'Referer': referer,
    'Accept': 'application/json, text/plain, */*',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://pontoweb.secullum.com.br'
})
session.cookies.update(cookies_dict)

log = []

print(f"\n{AMARELO}Iniciando...{RESET}\n")


for id_func in ids:
    numero_folha = None
    id_foto = None
    status = "Erro"
    baixado = "Não"

    try:
        url_dados = api_funcionario.replace("{id}", id_func)
        r = session.get(url_dados, timeout=15)
        if r.status_code != 200:
            status = f"HTTP {r.status_code}"
            print(f"{VERMELHO}✗ {id_func} → {status}{RESET}")
            log.append([id_func, "", "", "Não", status])
            continue

        dados = r.json()
        numero_folha = dados.get("NumeroFolha") or dados.get("numeroFolha")
        if not numero_folha:
            print(f"{AMARELO}✗ {id_func} → sem matrícula{RESET}")
            status = "Sem matrícula"
            log.append([id_func, "", "", "Não", status])
            continue
        print(f"{AZUL}→ {id_func} → {numero_folha}{RESET}")

        url_bio = api_biometria.replace("{id}", id_func)
        r_bio = session.get(url_bio, timeout=15)
        if r_bio.status_code != 200:
            status = f"Bio {r_bio.status_code}"
            print(f"{VERMELHO}  Erro biometria{RESET}")
            log.append([id_func, numero_folha, "", "Não", status])
            continue

        for b in r_bio.json():
            if "face" in str(b.get("DedoDescricao", "")).lower():
                id_foto = b["Id"]
                print(f"{VERDE}  Face ID: {id_foto}{RESET}")
                break

        if not id_foto:
            print(f"{AMARELO}  Sem face{RESET}")
            status = "Sem face"
            log.append([id_func, numero_folha, "", "Não", status])
            continue

        url_foto = f"https://pontoweb.secullum.com.br/BioWeb/FotoBiometria/{id_foto}"
        r_foto = session.get(url_foto, timeout=15)
        if r_foto.status_code == 200 and r_foto.json().get("FotoBiometria"):
            img = base64.b64decode(r_foto.json()["FotoBiometria"])
            with open(f"fotos_colaboradores/{numero_folha}.jpg", "wb") as f:
                f.write(img)
            print(f"{VERDE}  {numero_folha}.jpg{RESET}")
            status = "Sucesso"
            baixado = "Sim"
        else:
            status = "Foto vazia"

    except Exception as e:
        status = f"Erro: {str(e)[:30]}"

    log.append([id_func, numero_folha or "", id_foto or "", baixado, status])
    time.sleep(0.7)

log_file = f"Log_download_{datetime.now().strftime('%d%m%Y_%H%M%S')}.txt"
with open(log_file, 'w', encoding='utf-8') as f:
    f.write("ID;NumeroFolha;ID_Foto;Baixado;Status\n")
    for entry in log:
        linha = f"{entry[0]};{entry[1]};{entry[2]};{entry[3]};{entry[4]}\n"
        f.write(linha)

print(f"→ Log salvo em: {VERDE}{log_file}{RESET}")

print(f"\n{AMARELO}=== FINALIZADO ==={RESET}")
print(f"→ Fotos: {VERDE}fotos_colaboradores/{RESET}")
print(f"→ Log: {VERDE}{log_file}{RESET}")
print(f"→ Baixadas: {VERDE}{sum(1 for x in log if x[3]=='Sim')}{RESET}")
input(f"\n{AZUL}ENTER...{RESET}")
