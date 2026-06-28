import asyncio
import httpx
from datetime import datetime, timedelta

PLAYER_ID = "10985661938"

ADD_PLAYER_URL = "https://m2.0xarm.com/api/add_player"
REALTIME_URL = "https://m2.0xarm.com/api/realtime_status"

FIREBASE_URL = "https://rasid-e1af8-default-rtdb.firebaseio.com/"
NTFY_URL = "https://ntfy.sh/yyyhyhujjjmj"

ADD_PLAYER_HEADERS = {
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

REALTIME_HEADERS = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
    'x-m2byte-ts': "1781401859",
    'x-api-key': "M2_PRIVATE_KEY_2026",
    'x-m2byte-token': "489febe4129933a3ef47f778a66a2c06072eb304aff067aab7877b803bd52f1c",
    'x-m2byte-fp': "TW96aWxsYS81LjAgKFgxMTsgTGludXggeDg2XzY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvMTQ4LjAuMC4wIFNhZmFyaS81MzcuMzZ8fDQ1MHx8MTAwMHx8MjR8fGFyLUFF",
    'Cookie': "session=.eJxNjm1qxDAMRO-i30vxhyzZOUCvEeRYCqFdJyRZ2FJ69wbKQpl_j-HNfMO46X6Xrv2E4dwfegPZlvFcP7TDAJiLaVX0oZQYJaohG3MWIgmTI8dBa3QoZo5YpHJmrtnF2lIwP8E_3ajPbdm_YPCcPbrAid9yIFcy3-BznWdtrwuHHsey9nG5CLSSiC2XxMTBCjYK1qYq5oVzQro2Hofuf2VCQr4SX7TLXS_-Pj8n-PkFC3VHQg.ai4JZw.5VX-suzdPbk_8OO6820xEIq3UPI"
}


async def add_player(client):
    try:
        await client.post(
            ADD_PLAYER_URL,
            json={"player_id": PLAYER_ID},
            headers=ADD_PLAYER_HEADERS
        )
    except Exception:
        pass


async def main():
    async with httpx.AsyncClient(
        timeout=5,
        http2=True
    ) as client:

        # إرسال add_player مرتين بالتوازي
        await asyncio.gather(
            add_player(client),
            add_player(client)
        )
        await asyncio.sleep(3)


        response = await client.get(
            REALTIME_URL,
            params={"t": str(int(datetime.now().timestamp() * 1000))},
            headers=REALTIME_HEADERS
        )

        data = response.json()

        player = data.get(PLAYER_ID, {})
        status = player.get("status")

        if status == "offline":
            print("اللاعب غير متصل")
            return

        details = player.get("details", {})

        game_mode = details.get("game_mode")
        game_name = details.get("game_name")

        last_update = player.get("last_update")

        if last_update:
            dt = datetime.fromisoformat(last_update)
            mauritania_time = (
                dt - timedelta(hours=3)
            ).strftime("%Y-%m-%d %H:%M:%S")
        else:
            mauritania_time = "Unknown"

        record = {
            "player_id": PLAYER_ID,
            "status": status,
            "game_mode": game_mode,
            "game_name": game_name,
            "last_update": mauritania_time,
            "saved_at": datetime.utcnow().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        firebase_endpoint = (
            f"{FIREBASE_URL}/connections/{PLAYER_ID}.json"
        )

        await asyncio.gather(
    client.post(
        NTFY_URL,
        content=str(status).encode("utf-8")
    ),
    client.post(
        firebase_endpoint,
        json=record
    )
)

        print("تم حفظ الاتصال")


if __name__ == "__main__":
    asyncio.run(main())
