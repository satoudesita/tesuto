import streamlit as st

# タイトル
st.title("家事管理アプリ")

# セッション状態の初期化
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'button_state' not in st.session_state:
    st.session_state.button_state = {}

# タブの作成
tab1, tab2 = st.tabs(["家事リスト 1", "家事リスト 2"])

# 家事リスト 1
with tab1:
    st.header("家事リスト 1")
    task_name1 = st.text_input("家事の名前を入力してください (リスト 1)")

    if st.button("追加 (リスト 1)"):
        if task_name1:
            st.session_state.tasks.append(task_name1)

    st.write("現在の家事リスト:")
    for i in range(0, len(st.session_state.tasks), 4):  # 4つごとに処理
        cols = st.columns(4)
        for j in range(4):
            if i + j < len(st.session_state.tasks):
                with cols[j]:
                    # ボタンにユニークなキーを割り当てる
                    button_key = f"task1_{i + j}"
                    if st.button(st.session_state.tasks[i + j], key=button_key):
                        st.success(f"{st.session_state.tasks[i + j]} を実行しました！")
                        st.session_state.button_state[st.session_state.tasks[i + j]] = True

    st.write("実行済みの家事:")
    for task, completed in st.session_state.button_state.items():
        if completed:
            st.write(f"✔️ {task}")

# 家事リスト 2
with tab2:
    st.header("家事リスト 2")
    task_name2 = st.text_input("家事の名前を入力してください (リスト 2)")

    # リスト 1の家事をリスト 2にも追加
    if st.button("追加 (リスト 2)"):
        if task_name2:
            st.session_state.tasks.append(task_name2)  # 直接リスト 2 から追加
        else:
            st.warning("家事の名前を入力してください。")

    st.write("現在の家事リスト:")
    for i in range(0, len(st.session_state.tasks), 4):  # 4つごとに処理
        cols = st.columns(4)
        for j in range(4):
            if i + j < len(st.session_state.tasks):
                with cols[j]:
                    # ボタンにユニークなキーを割り当てる
                    button_key = f"task2_{i + j}"
                    if st.button(st.session_state.tasks[i + j], key=button_key):
                        st.success(f"{st.session_state.tasks[i + j]} を実行しました！")
                        st.session_state.button_state[st.session_state.tasks[i + j]] = True

    st.write("実行済みの家事:")
    for task, completed in st.session_state.button_state.items():
        if completed:
            st.write(f"✔️ {task}")
