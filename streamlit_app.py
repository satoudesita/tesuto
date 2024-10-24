import streamlit as st
import sqlite3

# SQLiteデータベースの初期化
def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tabs (name TEXT PRIMARY KEY, color TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (task_name TEXT, completed INTEGER)''')
    conn.commit()
    conn.close()

def add_tab_to_db(tab_name, tab_color):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('INSERT INTO tabs (name, color) VALUES (?, ?)', (tab_name, tab_color))
    conn.commit()
    conn.close()

def get_tabs_from_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('SELECT name, color FROM tabs')
    tabs = c.fetchall()
    conn.close()
    return tabs

def get_tasks_from_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('SELECT task_name, completed FROM tasks')
    tasks = c.fetchall()
    conn.close()
    return tasks

def add_task_to_db(task_name):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('INSERT INTO tasks (task_name, completed) VALUES (?, ?)', (task_name, 0))
    conn.commit()
    conn.close()

def mark_task_completed(task_name):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('UPDATE tasks SET completed = 1 WHERE task_name = ?', (task_name,))
    conn.commit()
    conn.close()

def delete_all_data():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('DELETE FROM tabs')
    c.execute('DELETE FROM tasks')
    conn.commit()
    conn.close()

# 初期化
init_db()

# タイトル
st.title("家事管理アプリ")

# セッション状態の初期化
if 'tabs' not in st.session_state:
    st.session_state.tabs = [name for name, _ in get_tabs_from_db()]
if 'tab_colors' not in st.session_state:
    st.session_state.tab_colors = {name: color for name, color in get_tabs_from_db()}

# データ削除ボタン
if st.button("全てのデータを削除"):
    delete_all_data()
    st.session_state.tabs = []
    st.session_state.tab_colors = {}
    st.success("全てのデータが削除されました。")

# タブの追加処理
new_tab_name = st.text_input("新しいタブの名前を入力してください")
tab_color = st.color_picker("タブの色を選択してください", "#00f900")
if st.button("タブを追加"):
    if new_tab_name and new_tab_name not in st.session_state.tabs:
        st.session_state.tabs.append(new_tab_name)
        st.session_state.tab_colors[new_tab_name] = tab_color
        add_tab_to_db(new_tab_name, tab_color)

# タブの作成
tabs = st.session_state.tabs

if tabs:
    selected_tab = st.tabs(tabs)

    for index, tab_name in enumerate(tabs):
        with selected_tab[index]:
            st.header(tab_name)

            # タブの色を変更するボタン
            new_tab_color = st.color_picker(f"{tab_name} の色を選択", st.session_state.tab_colors[tab_name])
            if st.button("色を変更", key=f"change_color_{tab_name}"):
                st.session_state.tab_colors[tab_name] = new_tab_color
                add_tab_to_db(tab_name, new_tab_color)

            # タスク追加
            task_name = st.text_input(f"{tab_name} に追加する家事の名前を入力してください", key=f"task_input_{tab_name}")

            if st.button("追加", key=f"add_{tab_name}"):
                if task_name:
                    add_task_to_db(task_name)
                    st.success(f"{task_name} を追加しました。")

            # 現在の家事リスト表示
            tasks = get_tasks_from_db()
            st.write("現在の家事リスト:")
            
            if tasks:
                cols_count = min(len(tasks), 4)
                cols = st.columns(cols_count)

                for i, (task_name, completed) in enumerate(tasks):
                    button_color = st.session_state.tab_colors[tab_name]

                    with cols[i % cols_count]:
                        if completed:
                            st.markdown(f"<div style='background-color: {button_color}; padding: 10px; border-radius: 5px;'>{task_name} (実行済み)</div>", unsafe_allow_html=True)
                        else:
                            if st.button(task_name, key=f"{tab_name}_{task_name}", disabled=completed):
                                mark_task_completed(task_name)
                                st.success(f"{task_name} を実行しました！")

            # 実行済みの家事表示
            st.write("実行済みの家事:")
            for task_name, completed in tasks:
                if completed:
                    st.write(f"✔️ {task_name}")
else:
    st.warning("タブがまだ追加されていません。")
