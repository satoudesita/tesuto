import streamlit as st

# タイトル
st.title("家事管理アプリ")

# 家事の名前を入力
task_name = st.text_input("家事の名前を入力してくださ")

# ボタンを追加するためのリスト
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# ボタン追加の処理
if st.button("追加"):
    if task_name:
        st.session_state.tasks.append(task_name)

# 現在の家事リストを表示
st.write("現在の家事リスト:")
for task in st.session_state.tasks:
    if st.button(task):
        st.success(f"{task} を実行しました！")
