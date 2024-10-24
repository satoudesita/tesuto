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
    num_buttons = len(st.session_state.tasks)
    
    for i in range(0, num_buttons, 4):  # 4つごとに処理
        cols = st.columns(4)
        for j in range(4):
            if i + j < num_buttons:  # ボタンが存在する場合のみ表示
                with cols[j]:
                    if st.button(st.session_state.tasks[i + j]):
                        st.success(f"{st.session_state.tasks[i + j]} を実行しました！")
