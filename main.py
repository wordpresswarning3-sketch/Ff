import requests
import json
import time
from datetime import datetime, timedelta


url1 = "https://m2.0xarm.com/api/add_player"

payload1 = {
  "player_id": "10985661938"
}

headers1 = {
  'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
  'Accept-Encoding': "gzip, deflate, br, zstd",
  'Content-Type': "application/json",
  'sec-ch-ua-platform': "\"Linux\"",
  'sec-ch-ua': "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
  'sec-ch-ua-mobile': "?0",
  'x-m2byte-ts': "1781402669",
  'x-m2byte-token': "4997dd4c11cb4f329cdfd39a1c4135558ac78939b6511a89bd19a44015f5bdf4",
  'x-m2byte-fp': "TW96aWxsYS81LjAgKFgxMTsgTGludXggeDg2XzY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvMTQ4LjAuMC4wIFNhZmFyaS81MzcuMzZ8fDQ1MHx8MTAwMHx8MjR8fGFyLUFF",
  'origin': "https://m2.0xarm.com",
  'sec-fetch-site': "same-origin",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://m2.0xarm.com/stream",
  'accept-language': "ar-AE,ar;q=0.9,fr-MR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
  'priority': "u=1, i",
  'Cookie': "session=.eJxNjlGKwzAMRO-i71KiWJKtHKDXCLZlh9DWCUkKXZa9-waWwjJ_j-HNfMO4lu0ZW2kHDMf2KheI6zwey700GIBUvRllxJyoul6zVXMaMRM6Zg4x-6BOkzBiDJoMNRJ1yJWTVYJ_urG813n7ggF9QOocS7giobiOLvBYpqnY58Je9n1e2jifBExZfA3KXnxflUz6ajnFitEHJjk3XnvZ_spCQv6M-9AWn-Xkt-md4ecX7A9HAg.ai4MSw.XcOyK3YgX1UF-RpGW001wqglC1c"
}

response1 = requests.post(url1, data=json.dumps(payload1), headers=headers1)


time.sleep(5)




url = "https://m2.0xarm.com/api/realtime_status"

params = {
    't': "1781401961291"
}

headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
    'sec-ch-ua-platform': "\"Linux\"",
    'sec-ch-ua': "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
    'x-m2byte-ts': "1781401859",
    'sec-ch-ua-mobile': "?0",
    'x-api-key': "M2_PRIVATE_KEY_2026",
    'x-m2byte-token': "489febe4129933a3ef47f778a66a2c06072eb304aff067aab7877b803bd52f1c",
    'content-type': "application/json",
    'x-m2byte-fp': "TW96aWxsYS81LjAgKFgxMTsgTGludXggeDg2XzY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvMTQ4LjAuMC4wIFNhZmFyaS81MzcuMzZ8fDQ1MHx8MTAwMHx8MjR8fGFyLUFF",
    'sec-fetch-site': "same-origin",
    'sec-fetch-mode': "cors",
    'sec-fetch-dest': "empty",
    'referer': "https://m2.0xarm.com/stream",
    'accept-language': "ar-AE,ar;q=0.9,fr-MR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
    'priority': "u=1, i",
    'Cookie': "session=.eJxNjm1qxDAMRO-i30vxhyzZOUCvEeRYCqFdJyRZ2FJ69wbKQpl_j-HNfMO46X6Xrv2E4dwfegPZlvFcP7TDAJiLaVX0oZQYJaohG3MWIgmTI8dBa3QoZo5YpHJmrtnF2lIwP8E_3ajPbdm_YPCcPbrAid9yIFcy3-BznWdtrwuHHsey9nG5CLSSiC2XxMTBCjYK1qYq5oVzQro2Hofuf2VCQr4SX7TLXS_-Pj8n-PkFC3VHQg.ai4JZw.5VX-suzdPbk_8OO6820xEIq3UPI"
}



# رابط قاعدة البيانات
FIREBASE_URL = "https://rasid-e1af8-default-rtdb.firebaseio.com/"

player_id = "10985661938"

# -------------------------
# كود جلب البيانات الحالي
# -------------------------

response = requests.get(url, params=params, headers=headers)
data = response.json()

player = data.get(player_id, {})

status = player.get("status")

details = player.get("details", {})
game_mode = details.get("game_mode")
game_name = details.get("game_name")

last_update = player.get("last_update")

if last_update:
    dt = datetime.fromisoformat(last_update)
    mauritania_time = (dt - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")
else:
    mauritania_time = "Unknown"

# -------------------------
# حفظ الاتصال إذا كان Online
# -------------------------

if status != "offline":
    requests.post(
    "https://ntfy.sh/ff_alert_7x92kd81",
    data="سارة متصلة".encode("utf-8")
    )

    record = {
        "player_id": player_id,
        "status": status,
        "game_mode": game_mode,
        "game_name": game_name,
        "last_update": mauritania_time,
        "saved_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }

    firebase_endpoint = f"{FIREBASE_URL}/connections/{player_id}.json"

    requests.post(
        firebase_endpoint,
        json=record
    )

    print("تم حفظ الاتصال")

else:
    print("اللاعب غير متصل")
