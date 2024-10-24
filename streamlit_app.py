import streamlit as st

# タイトル
st.title("家事管理アプリ")

# セッション状態の初期化
if 'tabs' not in st.session_state:
    st.session_state.tabs = {}
if 'button_state' not in st.session_state:
    st.session_state.button_state = {}

# タブの追加処理
new_tab_name = st.text_input("新しいタブの名前を入力してください")
if st.button("タブを追加"):
    if new_tab_name and new_tab_name not in st.session_state.tabs:
        st.session_state.tabs[new_tab_name] = []

# タブの作成
tabs = st.session_state.tabs
tab_names = list(tabs.keys())
if tab_names:
    selected_tab = st.selectbox("タブを選択", tab_names)
else:
    selected_tab = None

if selected_tab:
    st.header(selected_tab)
    
    # タスク追加
    task_name = st.text_input("家事の名前を入力してください")

    if st.button("追加"):
        if task_name:
            tabs[selected_tab].append(task_name)

    # 現在の家事リスト表示
    st.write("現在の家事リスト:")
    for i in range(0, len(tabs[selected_tab]), 4):  # 4つごとに処理
        cols = st.columns(4)
        for j in range(4):
            if i + j < len(tabs[selected_tab]):
                with cols[j]:
                    button_key = f"{selected_tab}_{i + j}"
                    if st.button(tabs[selected_tab][i + j], key=button_key):
                        st.success(f"{tabs[selected_tab][i + j]} を実行しました！")
                        st.session_state.button_state[tabs[selected_tab][i + j]] = True

    # 実行済みの家事表示
    st.write("実行済みの家事:")
    for task, completed in st.session_state.button_state.items():
        if completed:
            st.write(f"✔️ {task}")
