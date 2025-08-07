import requests
import time
import re
from keep_alive import keep_alive

email = "rixxant@libero.it"
base_url = "https://antautosurf.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0",
    "Accept": "*/*",
    "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3",
    "X-Requested-With": "XMLHttpRequest",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Referer": f"{base_url}/index.php?bitcoinwallet={email}&ref=",
}

def run_bot():
    session = requests.Session()
    session.headers.update(headers)

    print("🔐 Inizializzo sessione...")
    session.get(f"{base_url}/")

    print("🔍 Ottengo CSRF token...")
    res = session.get(f"{base_url}/index.php?bitcoinwallet={email}&ref=")
    csrf_token = re.search(r"csrf_token=([a-z0-9]+)", res.text)
    if not csrf_token:
        print("❌ CSRF token non trovato.")
        return
    csrf_token = csrf_token.group(1)
    print(f"✅ CSRF token trovato: {csrf_token}")

    while True:
        print("\n🌐 Inizio nuovo ciclo...")
        surf_init_url = f"{base_url}/surf.php?wallet={email}&key=&time=12&ad_id=&isitbad=0&csrf_token={csrf_token}"
        resp = session.get(surf_init_url)

        match = re.search(r"--_--(\d+)--_--([A-Z0-9]+)--_--(\d+)", resp.text)
        if not match:
            print("❌ Parametri non trovati.")
            print(resp.text)
            time.sleep(10)
            continue

        time_value = int(match.group(1))
        key = match.group(2)
        ad_id = match.group(3)

        print(f"🎯 key={key}, time={time_value}s, ad_id={ad_id}")
        print(f"⏳ Attendo {time_value} secondi...")
        time.sleep(time_value)

        final_url = f"{base_url}/surf.php?wallet={email}&key={key}&time={time_value}&ad_id={ad_id}&isitbad=0&csrf_token={csrf_token}"
        final_resp = session.get(final_url)

        print(f"✅ Eseguito: {final_url}")
        print("📄 Risposta:", final_resp.text.strip())

keep_alive()
run_bot()
