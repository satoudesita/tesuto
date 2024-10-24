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

# タブを表示
if tab_names:
    selected_tab = st.tabs(tab_names)
    
    # 選択されたタブの内容
    for tab_name in tab_names:
        with selected_tab[tab_names.index(tab_name)]:
            st.header(tab_name)
            
            # タスク追加
            task_name = st.text_input(f"{tab_name} に追加する家事の名前を入力してください")

            if st.button("追加", key=f"add_{tab_name}"):
                if task_name:
                    tabs[tab_name].append(task_name)

            # 現在の家事リスト表示
            st.write("現在の家事リスト:")
            for i in range(0, len(tabs[tab_name]), 4):  # 4つごとに処理
                cols = st.columns(4)
                for j in range(4):
                    if i + j < len(tabs[tab_name]):
                        with cols[j]:
                            button_key = f"{tab_name}_{i + j}"
                            if st.button(tabs[tab_name][i + j], key=button_key):
                                st.success(f"{tabs[tab_name][i + j]} を実行しました！")
                                st.session_state.button_state[tabs[tab_name][i + j]] = True

            # 実行済みの家事表示
            st.write("実行済みの家事:")
            for task, completed in st.session_state.button_state.items():
                if completed:
                    st.write(f"✔️ {task}")
else:
    st.warning("タブがまだ追加されていません。")
