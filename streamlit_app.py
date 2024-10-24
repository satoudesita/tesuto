import streamlit as st

# タイトル
st.title("家事管理アプリ")

# 家事の名前を入力
task_name = st.text_input("家事の名前を入力してください")

# ボタンを追加するためのリスト
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# ボタン追加の処理
if st.button("追加"):
    if task_name:
        st.session_state.tasks.append(task_name)

# 現在の家事リストを表示
st.write("現在の家事リスト:")

# 家事ボタンを横に並べる
if st.session_state.tasks:
    for i in range(0, len(st.session_state.tasks), 4):  # 4つごとに処理
        cols = st.columns(4)
        for j in range(4):
            if i + j < len(st.session_state.tasks):  # ボタンが存在する場合のみ表示
                with cols[j]:
                    if st.button(st.session_state.tasks[i + j]):
                        # ボタンを押した場合の処理
                        st.success(f"{st.session_state.tasks[i + j]} を実行しました！")
                        # ボタンの状態をセッションに保存
                        if 'button_state' not in st.session_state:
                            st.session_state.button_state = {}
                        st.session_state.button_state[st.session_state.tasks[i + j]] = True
                        
# 連動するボタンの状態を表示
if 'button_state' in st.session_state:
    st.write("実行済みの家事:")
    for task, completed in st.session_state.button_state.items():
        if completed:
            st.write(f"✔️ {task}")
