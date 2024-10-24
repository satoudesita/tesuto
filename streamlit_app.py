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
if 'tab_colors' not in st.session_state:
    st.session_state.tab_colors = {}

# タブの追加処理
new_tab_name = st.text_input("新しいタブの名前を入力してください")
tab_color = st.color_picker("タブの色を選択してください", "#00f900")  # デフォルト色を緑に設定
if st.button("タブを追加"):
    if new_tab_name and new_tab_name not in st.session_state.tabs:
        st.session_state.tabs.append(new_tab_name)
        st.session_state.tab_colors[new_tab_name] = tab_color  # 色を保存

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
                            
                            # ボタンの押下を反映
                            button_color = st.session_state.tab_colors[tab_name]
                            if task in st.session_state.button_state:
                                st.markdown(f"<div style='background-color: {button_color}; padding: 10px; border-radius: 5px;'>{task} (実行済み)</div>", unsafe_allow_html=True)
                            else:
                                if st.button(task, key=button_key):
                                    st.session_state.button_state[task] = True
                                    st.success(f"{task} を実行しました！")

            # 実行済みの家事表示
            st.write("実行済みの家事:")
            for task, completed in st.session_state.button_state.items():
                if completed:
                    st.write(f"✔️ {task}")
else:
    st.warning("タブがまだ追加されていません。")
