import requests
import threading
import time

def banAll(guild_id, members_id, bot_token):
    session = requests.Session
    def start():
        r = session.put(f"https://discord.com/api/v9/guilds/{guild_id}/bans/{members_id}", headers={"Authorization": f"Bot {bot_token"})
        if r.status_code == 429:
            time.sleep(r.json()['retry_after'])
            
    threading.Thread(target=start).start()
    