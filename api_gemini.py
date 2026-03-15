import google.generativeai as genai
import streamlit as st

API_KEY = st.secrets.get("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)

def get_gemini_model():
    return genai.GenerativeModel('gemini-2.5-flash')

def find_promo_codes(game_name, platform):
    if not API_KEY:
        return "⚠️ **系統錯誤**：未設定 API 金鑰"
        
    model = get_gemini_model()
    
    # Prompt 回歸單純，請它直接給出像 App 一樣的條列式結果
    prompt = f"""
    請幫我尋找 {platform} 平台上的遊戲「{game_name}」目前最新、最可能有效的 Promo Codes (兌換碼/序號)。
    請用 Markdown 格式清楚列出（例如使用條列式），並附上對應的獎勵說明。
    如果找不到任何序號，請直接告訴我目前找不到。
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ **API 發生錯誤**：\n{str(e)}"
