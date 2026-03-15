from google import genai
from google.genai import types
import streamlit as st

API_KEY = st.secrets.get("GEMINI_API_KEY")

def find_promo_codes(game_name, platform):
    if not API_KEY:
        return "⚠️ **系統錯誤**：未設定 API 金鑰"
        
    # 新版 SDK 的初始化方式
    client = genai.Client(api_key=API_KEY)
    
    prompt = f"""
    請幫我使用 Google 搜尋，尋找 {platform} 平台上的遊戲「{game_name}」目前最新、最可能有效的 Promo Codes (兌換碼/序號)。
    請用 Markdown 格式清楚列出（例如使用條列式），並附上對應的獎勵說明。
    如果網路上真的完全找不到任何序號，請直接告訴我目前找不到。
    """
    
    try:
        # 新版 SDK 呼叫 API 的寫法
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                # 【關鍵】這就是新版 SDK 成功啟動聯網搜尋的正確參數！
                tools=[{"google_search": {}}]
            )
        )
        return response.text
    except Exception as e:
        return f"⚠️ **API 發生錯誤**：\n{str(e)}"
