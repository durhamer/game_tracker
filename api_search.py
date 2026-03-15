from api_roblox import search_roblox_games

def search_game(keyword, platform):
    """
    根據不同平台，切換不同的搜尋邏輯。
    目前先實作 Roblox 的真實搜尋，其他平台暫時用模擬資料代替。
    """
    if platform == "Roblox":
        roblox_results = search_roblox_games(keyword)
        # 把詳細資料包裝成方便 UI 顯示的字典
        return {game["name"]: game for game in roblox_results}
        
    else:
        # 其他平台 (手遊, Steam, Switch) 暫時的模擬結果
        return {
            f"{keyword} (官方原版)": {"name": f"{keyword}", "description": "官方遊戲介紹..."},
            f"{keyword} (粉絲重製版)": {"name": f"{keyword} Remake", "description": "粉絲製作的介紹..."}
        }
