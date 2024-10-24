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
    if task_name and len(st.session_state.tasks) < 4:
        st.session_state.tasks.append(task_name)
    elif len(st.session_state.tasks) >= 4:
        st.warning("最大4個までの家事を追加できます。")

# 現在の家事リストを表示
st.write("現在の家事リスト:")

# 家事ボタンを横に並べる
if st.session_state.tasks:
    cols = st.columns(min(4, len(st.session_state.tasks)))
    for i, task in enumerate(st.session_state.tasks):
        with cols[i]:
            if st.button(task):
                st.success(f"{task} を実行しました！")
