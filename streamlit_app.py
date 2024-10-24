import streamlit as st

# タイトル
st.title("家事管理アプリ")

# セッション状態の初期化
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'button_state' not in st.session_state:
    st.session_state.button_state = {}
if 'tabs' not in st.session_state:
    st.session_state.tabs = []

# タブの追加処理
new_tab_name = st.text_input("新しいタブの名前を入力してください")
if st.button("タブを追加"):
    if new_tab_name and new_tab_name not in st.session_state.tabs:
        st.session_state.tabs.append(new_tab_name)

# タブの作成
tabs = st.session_state.tabs

if tabs:
    selected_tab = st.tabs(tabs)
    
    # 選択されたタブの内容
    for index, tab_name in enumerate(tabs):
        with selected_tab[index]:
            st.header(tab_name)
            
            # 最初のタブの場合のみタスク追加
            if index == 0:
                task_name = st.text_input(f"{tab_name} に追加する家事の名前を入力してください", key=f"task_input_{tab_name}")

                if st.button("追加", key=f"add_{tab_name}"):
                    if task_name and task_name not in st.session_state.tasks:
                        st.session_state.tasks.append(task_name)

            # 現在の家事リスト表示
            st.write("現在の家事リスト:")
            for i in range(0, len(st.session_state.tasks), 4):  # 4つごとに処理
                cols = st.columns(4)
                for j in range(4):
                    if i + j < len(st.session_state.tasks):
                        with cols[j]:
                            task = st.session_state.tasks[i + j]
                            button_key = f"{tab_name}_{i + j}"
                            
                            # ボタンの色を変更するためのスタイル
                            button_color = "lightgray" if task not in st.session_state.button_state else "green"
                            if st.button(task, key=button_key, help="このタスクを実行します", disabled=task in st.session_state.button_state):
                                st.session_state.button_state[task] = True
                                st.success(f"{task} を実行しました！")
                                
                            # ボタンの色を変更するためのHTMLスタイル
                            st.markdown(f"<style>div.stButton > button[data-testid='{button_key}'] {{ background-color: {button_color}; }}</style>", unsafe_allow_html=True)

            # 実行済みの家事表示
            st.write("実行済みの家事:")
            for task, completed in st.session_state.button_state.items():
                if completed:
                    st.write(f"✔️ {task}")
else:
    st.warning("タブがまだ追加されていませ。")
