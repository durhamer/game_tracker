import streamlit as st
from api_search import search_game
from api_gemini import find_promo_codes

st.set_page_config(page_title="跨平台遊戲追蹤器", page_icon="🎮", layout="wide")

st.title("🎮 跨平台遊戲資訊與序號追蹤器")

# --- 步驟 1: 平台選擇與關鍵字輸入 ---
col1, col2 = st.columns([1, 2])
with col1:
    platform = st.selectbox("選擇遊戲平台", ["Roblox", "手遊", "Steam", "Switch"])
with col2:
    keyword = st.text_input("輸入遊戲名稱關鍵字 (支援多語言輸入)")

# --- 步驟 2: 顯示多個搜尋結果讓使用者確認 ---
if keyword:
    st.subheader("🔍 請確認你要查詢的遊戲：")
    
    # 呼叫 api_search 取得結果字典 { "顯示名稱": {詳細資料} }
    search_results = search_game(keyword, platform)
    
    if not search_results:
        st.warning("找不到相關遊戲，請嘗試其他關鍵字。")
    else:
        # 讓使用者從選單中挑選正確的遊戲
        selected_game_name = st.selectbox("搜尋結果：", list(search_results.keys()))
        selected_game_data = search_results[selected_game_name]

        # --- 步驟 3: 執行查詢 ---
        if st.button("🚀 獲取最新資訊與序號"):
            st.divider()
            info_col, code_col = st.columns(2)
            
            # 【右側】Promo Codes (Gemini)
            with code_col:
                st.header("🎁 最新 Promo Codes")
                with st.spinner("正在召喚 AI 尋找序號中..."):
                    codes_data = find_promo_codes(selected_game_name, platform)
                    
                    if codes_data and len(codes_data) > 0 and codes_data[0].get("code") != "系統錯誤":
                        st.dataframe(codes_data, use_container_width=True, hide_index=True)
                    else:
                        st.info(codes_data[0].get("reward", "目前找不到相關序號。"))

            # 【左側】遊戲即時更新與公告
            with info_col:
                st.header("📢 遊戲最新公告")
                if platform == "Roblox":
                    st.success("成功抓取 Roblox 遊戲資訊！")
                    st.write(f"**遊戲 ID (Universe ID):** {selected_game_data.get('universeId')}")
                    
                    # 取出說明欄位並稍微排版
                    description = selected_game_data.get('description', '無說明')
                    st.text_area("遊戲說明 (通常包含更新日誌與序號)", description, height=300)
                else:
                    st.info("其他平台的即時公告功能開發中...")
