import google.generativeai as genai
import streamlit as st
import json

# 直接從環境讀取金鑰，不依賴本機檔案
API_KEY = st.secrets.get("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)

def get_gemini_model():
    # 加入 Google 搜尋工具，讓 AI 可以即時上網找最新序號
    return genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        tools='google_search_retrieval' # 加上這行開啟搜尋能力
    )

def find_promo_codes(game_name, platform):
    if not API_KEY:
        return [{"code": "系統錯誤", "reward": "未設定 API 金鑰", "status": "失敗"}]
        
    model = get_gemini_model()
    prompt = f"""
    請幫我尋找 {platform} 平台上的遊戲「{game_name}」目前最新、最可能有效的 Promo Codes (兌換碼/序號)。
    請以嚴格的 JSON 陣列 (Array) 格式回傳，不要包含其他 markdown 說明文字。
    格式範例：
    [
        {{"code": "VIP2024", "reward": "1000 金幣", "status": "可能有效"}},
        {{"code": "FREESWORD", "reward": "新手劍", "status": "測試中"}}
    ]
    如果找不到任何序號，請回傳空的 JSON 陣列：[]
    """
    try:
        response = model.generate_content(prompt)
        text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(text)
    except Exception as e:
        return [{"code": "API 錯誤", "reward": "解析失敗", "status": str(e)}]
