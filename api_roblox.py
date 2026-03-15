import requests

def search_roblox_games(keyword):
    """透過關鍵字搜尋 Roblox 遊戲，回傳可能的遊戲清單與完整資訊"""
    url = f"https://games.roblox.com/v1/games/list?keyword={keyword}&maxRows=10"
    headers = {"Accept": "application/json"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json().get("games", [])
            # 回傳格式：[{"name": "Blox Fruits", "universeId": 12345, "description": "..."}]
            return data
        else:
            return []
    except Exception as e:
        print(f"Roblox API 發生錯誤: {e}")
        return []
