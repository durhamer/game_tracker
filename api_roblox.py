import requests
import uuid

def search_roblox_games(keyword):
    """透過關鍵字搜尋 Roblox 遊戲，回傳可能的遊戲清單與完整資訊"""
    
    # 1. 產生亂數 Session ID (新版搜尋 API 必備參數)
    session_id = str(uuid.uuid4())
    
    # 2. 改用 Roblox 最新的 omni-search API
    url = f"https://apis.roblox.com/search-api/omni-search?searchQuery={keyword}&sessionId={session_id}&pageType=all"
    
    # 3. 偽裝成真實瀏覽器，防止 Streamlit 雲端主機被 Roblox 當成機器人封鎖
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        # 加上 timeout 避免雲端主機一直卡住
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("searchResults", [])
            parsed_games = []
            
            # 解析新版 API 的 JSON 結構
            for item in results:
                # 確保我們只抓取「遊戲」類別的結果
                if item.get("contentType") == "Game" or "contents" in item:
                    contents = item.get("contents", [])
                    # 有些資料包在 contents 陣列裡，有些在 item 本身
                    items_to_check = contents if contents else [item]
                    
                    for content in items_to_check:
                        name = content.get("name")
                        universe_id = content.get("universeId")
                        
                        if name and universe_id:
                            # 避免重複加入同一個遊戲
                            if not any(g['universeId'] == universe_id for g in parsed_games):
                                parsed_games.append({
                                    "name": name,
                                    "universeId": universe_id,
                                    "description": content.get("description", "無詳細說明")
                                })
            
            return parsed_games[:10]
            
        else:
            # 如果還是被擋，回傳一個明確的錯誤選項讓 UI 顯示，方便 debug
            print(f"Roblox API 錯誤碼: {response.status_code}")
            return [{"name": f"{keyword} (搜尋失敗: 伺服器拒絕連線 {response.status_code})", "universeId": "00000", "description": "API 請求被阻擋"}]
            
    except Exception as e:
        print(f"Roblox API 發生例外錯誤: {e}")
        return [{"name": f"{keyword} (連線發生錯誤)", "universeId": "00000", "description": str(e)}]
