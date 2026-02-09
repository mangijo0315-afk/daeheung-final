import streamlit as st
from datetime import datetime
import streamlit.components.v1 as components

# 앱 설정
st.set_page_config(page_title="대흥교회 스마트 보드", layout="wide")

# 데이터 초기화
for key, default in [('message_list', []), ('sheets', []), ('page', 0), ('permanent_storage', {}), ('temp_storage', {})]:
    if key not in st.session_state: st.session_state[key] = default

def move_page(delta):
    if st.session_state.sheets:
        st.session_state.page = (st.session_state.page + delta) % len(st.session_state.sheets)

# 디자인 CSS
st.markdown("""
    <style>
    .signal-box { background-color: #ff4b4b; color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 15px; border: 4px solid white; }
    .nav-btn button { height: 80px !important; font-size: 30px !important; background-color: #f0f2f6 !important; border-radius: 15px !important; }
    .stButton>button { width: 100%; font-weight: bold; border-radius: 12px; }
    </style>
""", unsafe_allow_html=True)

user_role = st.sidebar.radio("📢 역할 선택", ["인도자", "반주자/싱어"])

# 메인 화면 레이아웃
if st.session_state.sheets:
    # 1. 이동 버튼
    st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.button("◀ PREV", key="p_btn", on_click=move_page, args=(-1,))
    c2.button("NEXT ▶", key="n_btn", on_click=move_page, args=(1,))
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. 신호 배너
    current_msg = st.session_state.message_list[-1] if st.session_state.message_list else "대기 중"
    st.markdown(f'<div class="signal-box"><h1>{current_msg}</h1></div>', unsafe_allow_html=True)

    # 3. 악보 출력
    st.image(st.session_state.sheets[st.session_state.page], use_container_width=True)

    # 인도자 전용 컨트롤러 (우측 사이드바처럼 활용 가능)
    if user_role == "인도자":
        with st.expander("📢 신호 보내기 버튼들", expanded=True):
            btns = ["𝄇 후렴", "🌉 브릿지", "🔚 엔딩", "1절로", "한 키 업"]
            cols = st.columns(len(btns))
            for i, b in enumerate(btns):
                if cols[i].button(b):
                    st.session_state.message_list.append(b); st.rerun()
else:
    if user_role == "인도자":
        uploaded = st.file_uploader("악보 업로드", accept_multiple_files=True)
        if uploaded: st.session_state.sheets = uploaded; st.rerun()
    else:
        st.info("인도자가 악보를 올릴 때까지 기다려 주세요.")
