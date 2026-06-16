import requests
import json
from datetime import datetime, timedelta

session = requests.Session()

player_id = "10985661938"

# -------------------------
# 1. add_player request
# -------------------------
url1 = "https://m2.0xarm.com/api/add_player"

payload1 = {
    "player_id": player_id
}

headers1 = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
    'Accept-Encoding': "gzip, deflate, br, zstd",
    'Content-Type': "application/json",
    'sec-ch-ua-platform': "\"Linux\"",
    'sec-ch-ua': "\"Chromium;v=148\", \"Google Chrome;v=148\", \"Not/A)Brand;v=99\"",
    'sec-ch-ua-mobile': "?0",
    'x-m2byte-ts': "1781402669",
    'x-m2byte-token': "4997dd4c11cb4f329cdfd39a1c4135558ac78939b6511a89bd19a44015f5bdf4",
    'x-m2byte-fp': "TW96aWxsYS81LjAgKFgxMTsgTGludXggeDg2XzY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvMTQ4LjAuMC4wIFNhZmFyaS81MzcuMzZ8fDQ1MHx8MTAwMHx8MjR8fGFyLUFF",
    'origin': "https://m2.0xarm.com",
    'referer': "https://m2.0xarm.com/stream",
    'Cookie': "session=.eJxNjlGKwzAMRO-i71KiWJKtHKDXCLZlh9DWCUkKXZa9-waWwjJ_j-HNfMO4lu0ZW2kHDMf2KheI6zwey700GIBUvRllxJyoul6zVXMaMRM6Zg4x-6BOkzBiDJoMNRJ1yJWTVYJ_urG813n7ggF9QOocS7giobiOLvBYpqnY58Je9n1e2jifBExZfA3KXnxflUz6ajnFitEHJjk3XnvZ_spCQv6M-9AWn-Xkt-md4ecX7A9HAg.ai4MSw.XcOyK3YgX1UF-RpGW001wqglC1c"
}

session.post(
    url1,
    json=payload1,
    headers=headers1,
    timeout=5
)

# -------------------------
# 2. realtime status request
# -------------------------
url = "https://m2.0xarm.com/api/realtime_status"

params = {
    't': "1781401961291"
}

headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
    'x-m2byte-ts': "1781401859",
    'x-api-key': "M2_PRIVATE_KEY_2026",
    'x-m2byte-token': "489febe4129933a3ef47f778a66a2c06072eb304aff067aab7877b803bd52f1c",
    'x-m2byte-fp': "TW96aWxsYS81LjAgKFgxMTsgTGludXggeDg2XzY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvMTQ4LjAuMC4wIFNhZmFyaS81MzcuMzZ8fDQ1MHx8MTAwMHx8MjR8fGFyLUFF",
    'Cookie': "session=.eJxNjm1qxDAMRO-i30vxhyzZOUCvEeRYCqFdJyRZ2FJ69wbKQpl_j-HNfMO46X6Xrv2E4dwfegPZlvFcP7TDAJiLaVX0oZQYJaohG3MWIgmTI8dBa3QoZo5YpHJmrtnF2lIwP8E_3ajPbdm_YPCcPbrAid9yIFcy3-BznWdtrwuHHsey9nG5CLSSiC2XxMTBCjYK1qYq5oVzQro2Hofuf2VCQr4SX7TLXS_-Pj8n-PkFC3VHQg.ai4JZw.5VX-suzdPbk_8OO6820xEIq3UPI"
}

response = session.get(
    url,
    params=params,
    headers=headers,
    timeout=5
)

data = response.json()

player = data.get(player_id, {})

status = player.get("status")

# -------------------------
# 3. إيقاف مبكر إذا Offline
# -------------------------
if status == "offline":
    print("اللاعب غير متصل")
    exit()

# -------------------------
# 4. استخراج البيانات
# -------------------------
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
# 5. إرسال إشعار
# -------------------------
session.post(
    "https://ntfy.sh/ff_alert_7x92kd81",
    data="سارة متصلة".encode("utf-8"),
    timeout=5
)

# -------------------------
# 6. حفظ في Firebase
# -------------------------
FIREBASE_URL = "https://rasid-e1af8-default-rtdb.firebaseio.com/"

record = {
    "player_id": player_id,
    "status": status,
    "game_mode": game_mode,
    "game_name": game_name,
    "last_update": mauritania_time,
    "saved_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
}

firebase_endpoint = f"{FIREBASE_URL}/connections/{player_id}.json"

session.post(
    firebase_endpoint,
    json=record,
    timeout=5
)

print("تم حفظ الاتصال")
