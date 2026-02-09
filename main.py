import streamlit as st

# 앱 설정
st.set_page_config(page_title="대흥교회 스마트 보드", layout="wide")

# 데이터 초기화
for key, default in [('message_list', []), ('sheets', []), ('page', 0)]:
    if key not in st.session_state: st.session_state[key] = default

def move_page(delta):
    if st.session_state.sheets:
        st.session_state.page = (st.session_state.page + delta) % len(st.session_state.sheets)

# 디자인 CSS
st.markdown("""
    <style>
    .signal-box { background-color: #ff4b4b; color: white; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; }
    .stButton>button { width: 100%; height: 50px; font-weight: bold; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 사이드바 (여기에 모든 컨트롤러를 넣었어!) ---
with st.sidebar:
    st.title("🎮 컨트롤러")
    user_role = st.radio("📢 역할", ["인도자", "반주자/싱어"])
    
    st.divider()
    
    if st.session_state.sheets:
        st.subheader("📄 페이지 조절")
        c1, c2 = st.columns(2)
        c1.button("◀ 이전", on_click=move_page, args=(-1,))
        c2.button("다음 ▶", on_click=move_page, args=(1,))
        
        if user_role == "인도자":
            st.divider()
            st.subheader("⚡ 실시간 신호")
            btns = ["𝄇 후렴", "🌉 브릿지", "🔚 엔딩", "1절로", "한 키 업"]
            for b in btns:
                if st.button(b):
                    st.session_state.message_list.append(b)
                    st.rerun()
            
            if st.button("🗑️ 신호 초기화", type="secondary"):
                st.session_state.message_list = []
                st.rerun()

# --- 메인 화면 ---
if st.session_state.sheets:
    # 현재 신호 표시
    current_msg = st.session_state.message_list[-1] if st.session_state.message_list else "대기 중"
    st.markdown(f'<div class="signal-box"><h1>현재 신호: {current_msg}</h1></div>', unsafe_allow_html=True)
    
    # 악보 출력
    st.image(st.session_state.sheets[st.session_state.page], use_container_width=True)
else:
    st.info("먼저 악보 파일을 업로드해주세요.")
    uploaded = st.file_uploader("악보 업로드", accept_multiple_files=True)
    if uploaded:
        st.session_state.sheets = uploaded
        st.rerun()
