import streamlit as st
from datetime import datetime
import qrcode
import barcode
import requests
from barcode.writer import ImageWriter
from io import BytesIO
from PIL import Image
import pytz
import sqlite3
import hashlib
import random
 
# POSTリクエストを送信する関数
def send_post_request(url, data):
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            st.write("成功: ", response.json())
        else:
            st.write("エラー: ", response.status_code)
    except Exception as e:
        st.write(f"リクエストエラー: {e}")
 
# QRコードを生成する関数
def generate_qrcode(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
 
    img = qr.make_image(fill='black', back_color='white')
 
    # QRコードをバイナリデータとして返す
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
 
    return img_byte_arr.getvalue()  # バイナリデータを返す
 
# バーコードを生成する関数
def generate_code128_barcode(data):
    barcode_class = barcode.get_barcode_class('code128')
    code128 = barcode_class(data, writer=ImageWriter())
 
    # バーコードをバイナリデータとして生成
    buffer = BytesIO()
    code128.write(buffer)
    buffer.seek(0)
 
    return buffer.getvalue()  # バイナリデータを返す
 
# タブを作成
tab1, tab2 ,tab3,tab4,tab5 = st.tabs(["QR", "BR", "test", "遅刻証明", "遅刻証明読み取り"])
 
with tab1:
    # ユーザー入力の取得
    st.write("以下のフォームに情報を入力してください。")
    fields = ["high school", "glade", "class", "name"]
    user_input = {field: st.text_input(field) for field in fields}
   
    st.subheader("add information")
    additional_fields = []
    add_field = st.text_input("the name")
    add_value = st.text_input("the value")
    if add_field and add_value:
        additional_fields.append((add_field, add_value))
   
    # 入力が全て埋まった場合にQRコードを生成
    if all(user_input[field] for field in fields):
        combined_data = "\n".join([f"{key}: {value}" for key, value in user_input.items()])
        for field_name, field_value in additional_fields:
            combined_data += f"\n{field_name}: {field_value}"
       
        qr_img_data = generate_qrcode(combined_data)
        data = {"combined_data": combined_data, "qr_image": qr_img_data}
       
        # APIに送信
        send_post_request('API_URL', data)
        st.image(qr_img_data, caption="生成されたQRコード", use_container_width=True)
 
    # バーコード生成
    with st.expander("バーコード"):
        text_input = st.text_input("バーコードにするテキストを入力してください。:")
        if text_input:
            barcode_data = generate_code128_barcode(text_input)
            st.image(barcode_data, caption="生成されたCODE128バーコード", use_container_width=True)
 
with tab2:
    with st.form(key='my_form', clear_on_submit=True):
        st.text('テキストボックスの内容と時刻を取得')            
        user_input = st.text_input(label='テキストを入力してください:', key='input')
        submit_button = st.form_submit_button(label='送信')
 
    if submit_button and user_input:
        japan_tz = pytz.timezone('Asia/Tokyo')
        current_time_japan = datetime.now(japan_tz)
        current_time = current_time_japan.strftime('%m-%d %H:%M')
       
        st.text(f"入力されたテキスト: {user_input}")
        st.text(f"入力時刻: {current_time}")
        data = {"名前": user_input, "時間": current_time}
        send_post_request('https://prod-08.japaneast.logic.azure.com:443/workflows/2dad7268f2844042bae005c2ec7916f6/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=V-60f4bGMzshRcghrvSV7qt-WEgKqbgQGfGk2F8BQPk', data)
 
with tab3:
    API_URL = "https://api.jancodelookup.com/"
    API_ID = "96385e12558d53c366efb3c187ef0440"
   
    def search_product_by_code(jan_code):
        params = {'appId': API_ID, 'query': jan_code, 'hits': 1, 'page': 1, 'type': 'code'}
        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'product' in data and len(data['product']) > 0:
                product = data['product'][0]
                return product
            else:
                st.warning("商品が見つかりませんでした")  
                return None
        else:
            st.error(f"APIリクエストに失敗しました: {response.status_code} - {response.text}")
            return None
   
    st.subheader("JANコードで商品検索")
    with st.form(key='my2_form', clear_on_submit=True):
        jan_code = st.text_input(label="JANコードを入力してください", key="search")          
        submit_button = st.form_submit_button(label='送信')
 
    if jan_code:
        product = search_product_by_code(jan_code)
        if product:
            st.text("商品情報:")
            st.text(f"商品名: {product.get('itemName', '不明')}")
            st.text(f"ブランド名: {product.get('brandName', '不明')}")
            st.text(f"メーカー名: {product.get('makerName', '不明')}")
            st.text(f"詳細ページ: [商品ページ](https://www.jancodelookup.com/code/{product['codeNumber']})")
            st.image(product.get('itemImageUrl'))
 
with tab4:
 
    # POSTリクエストを送信する関数
    def send_post_request(url, data):
        try:

            request_data = {
                "body": str(data)  # データを文字列として 'body' フィールドに格納
            }
           
            response = requests.post(url, json=request_data)  # json形式でPOSTリクエストを送信
            if response.status_code == 200:
                st.write("成功: ", response.json())
            else:
                st.write("エラー: ", response.status_code)
                st.write("エラーメッセージ: ", response.text)  # エラーメッセージを表示
        except Exception as e:
            st.write(f"リクエストエラー: {e}")
 
    # ユーザーのDB初期化
    def init_db():
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
 
    # パスワードをハッシュ化
    def hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
 
    # ユーザーをDBに保存
    def save_user(username, password):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        hashed_password = hash_password(password)
        try:
            cursor.execute('''
                INSERT INTO users (username, password)
                VALUES (?, ?)
            ''', (username, hashed_password))
            conn.commit()
        except sqlite3.IntegrityError:
            st.error("このユーザー名はすでに存在します")
        conn.close()
 
    # ユーザー認証
    def authenticate_user(username, password):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        hashed_password = hash_password(password)
        cursor.execute('''
            SELECT * FROM users WHERE username = ? AND password = ?
        ''', (username, hashed_password))
        user = cursor.fetchone()
        conn.close()
        return user
 
    # 初期化
    init_db()
 
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""
 
    if st.session_state.logged_in:
        selected_option2 = st.radio("選択肢", ["遅刻証明", "ログアウト"])
        if selected_option2 == "遅刻証明":
            st.text(f"{st.session_state.username} ログイン")
            st.subheader("遅刻証明書発行")
            reason = st.text_input(label="理由", key="why")
            late_button = st.button(label="発行", key="hakkou")
            if late_button:
                japan_time = pytz.timezone('Asia/Tokyo')
                get_time_japan = datetime.now(japan_time)
                get_time = get_time_japan.strftime('%m月%d %H時%M分 ')
                get_day = get_time_japan.strftime('%A')
 
                # 日本時間の時刻部分
                user_time = get_time_japan.time()
                if get_day == "Monday":
                    if datetime.strptime('09:15', '%H:%M').time()>= user_time >= datetime.strptime('08:25', '%H:%M').time():
                        zigen=st.subheader("1限")
                    elif datetime.strptime('09:24', '%H:%M').time() >=user_time >= datetime.strptime('09:16', '%H:%M').time():
                        zigen=st.subheader("1限と2限の間")
                    elif datetime.strptime('10:15', '%H:%M').time() >=user_time >= datetime.strptime('09:25', '%H:%M').time():
                        zigen=st.subheader("2限")
                    elif datetime.strptime('10:24', '%H:%M').time() >=user_time >= datetime.strptime('10:16', '%H:%M').time():
                        zigen=st.subheader("2限と3限の間")
                    elif datetime.strptime('11:15', '%H:%M').time() >=user_time >= datetime.strptime('10:25', '%H:%M').time():
                        zigen=st.subheader("3限")
                    elif datetime.strptime('11:24', '%H:%M').time() >=user_time >= datetime.strptime('11:16', '%H:%M').time():
                        zigen=st.subheader("3限と4限の間")
                    elif datetime.strptime('12:15', '%H:%M').time() >=user_time >= datetime.strptime('11:25', '%H:%M').time():
                        zigen=st.subheader("4限")
                    elif datetime.strptime('12:55', '%H:%M').time() >=user_time >= datetime.strptime('12:16', '%H:%M').time():
                        zigen=st.subheader("昼休み")
                    elif datetime.strptime('13:10', '%H:%M').time() >=user_time >= datetime.strptime('12:56', '%H:%M').time():
                        zigen=st.subheader("掃除")
                    elif datetime.strptime('13:19', '%H:%M').time() >=user_time >= datetime.strptime('13:11', '%H:%M').time():
                        zigen=st.subheader("掃除と5限の間")
                    elif datetime.strptime('14:10', '%H:%M').time() >=user_time >= datetime.strptime('13:20', '%H:%M').time():
                        zigen=st.subheader("5限")
                    elif datetime.strptime('14:19', '%H:%M').time() >=user_time >= datetime.strptime('14:11', '%H:%M').time():
                        zigen=st.subheader("5限と6限の間")
                    elif datetime.strptime('15:10', '%H:%M').time() >=user_time >= datetime.strptime('14:20', '%H:%M').time():
                        zigen=st.subheader("6限")
                    elif datetime.strptime('15:19', '%H:%M').time() >=user_time >= datetime.strptime('15:11', '%H:%M').time():
                        zigen=st.subheader("6限とHRAの間")
                    elif datetime.strptime('15:35', '%H:%M').time() >=user_time >= datetime.strptime('15:20', '%H:%M').time():
                        zigen=st.subheader("HRA")
                    else:
                        zigen=st.subheader("放課後")
                elif get_day == "Wednesday":
                    if datetime.strptime('09:15', '%H:%M').time()>= user_time >= datetime.strptime('08:25', '%H:%M').time():
                        zigen=st.subheader("1限")
                    elif datetime.strptime('09:24', '%H:%M').time() >=user_time >= datetime.strptime('09:16', '%H:%M').time():
                        zigen=st.subheader("1限と2限の間")
                    elif datetime.strptime('10:15', '%H:%M').time() >=user_time >= datetime.strptime('09:25', '%H:%M').time():
                        zigen=st.subheader("2限")
                    elif datetime.strptime('10:24', '%H:%M').time() >=user_time >= datetime.strptime('10:16', '%H:%M').time():
                        zigen=st.subheader("2限と3限の間")
                    elif datetime.strptime('11:15', '%H:%M').time() >=user_time >= datetime.strptime('10:25', '%H:%M').time():
                        zigen=st.subheader("3限")
                    elif datetime.strptime('11:24', '%H:%M').time() >=user_time >= datetime.strptime('11:16', '%H:%M').time():
                        zigen=st.subheader("3限と4限の間")
                    elif datetime.strptime('12:15', '%H:%M').time() >=user_time >= datetime.strptime('11:25', '%H:%M').time():
                        zigen=st.subheader("4限")
                    elif datetime.strptime('12:55', '%H:%M').time() >=user_time >= datetime.strptime('12:16', '%H:%M').time():
                        zigen=st.subheader("昼休み")
                    elif datetime.strptime('13:10', '%H:%M').time() >=user_time >= datetime.strptime('12:56', '%H:%M').time():
                        zigen=st.subheader("掃除")
                    elif datetime.strptime('13:19', '%H:%M').time() >=user_time >= datetime.strptime('13:11', '%H:%M').time():
                        zigen=st.subheader("掃除と5限の間")
                    elif datetime.strptime('14:10', '%H:%M').time() >=user_time >= datetime.strptime('13:20', '%H:%M').time():
                        zigen=st.subheader("5限")
                    elif datetime.strptime('14:19', '%H:%M').time() >=user_time >= datetime.strptime('14:11', '%H:%M').time():
                        zigen=st.subheader("5限と6限の間")
                    elif datetime.strptime('15:10', '%H:%M').time() >=user_time >= datetime.strptime('14:20', '%H:%M').time():
                        zigen=st.subheader("6限")
                    elif datetime.strptime('15:19', '%H:%M').time() >=user_time >= datetime.strptime('15:11', '%H:%M').time():
                        zigen=st.subheader("6限とHRAの間")
                    elif datetime.strptime('15:35', '%H:%M').time() >=user_time >= datetime.strptime('15:20', '%H:%M').time():
                        zigen=st.subheader("HRA")
                    else:
                        zigen=st.subheader("放課後")
                else:
                    if datetime.strptime('09:15', '%H:%M').time()>= user_time >= datetime.strptime('08:25', '%H:%M').time():
                        zigen=st.subheader("1限")
                    elif datetime.strptime('09:24', '%H:%M').time() >=user_time >= datetime.strptime('09:16', '%H:%M').time():
                        zigen=st.subheader("1限と2限の間")
                    elif datetime.strptime('10:15', '%H:%M').time() >=user_time >= datetime.strptime('09:25', '%H:%M').time():
                        zigen=st.subheader("2限")
                    elif datetime.strptime('10:24', '%H:%M').time() >=user_time >= datetime.strptime('10:16', '%H:%M').time():
                        zigen=st.subheader("2限と3限の間")
                    elif datetime.strptime('11:15', '%H:%M').time() >=user_time >= datetime.strptime('10:25', '%H:%M').time():
                        zigen=st.subheader("3限")
                    elif datetime.strptime('11:24', '%H:%M').time() >=user_time >= datetime.strptime('11:16', '%H:%M').time():
                        zigen=st.subheader("3限と4限の間")
                    elif datetime.strptime('12:15', '%H:%M').time() >=user_time >= datetime.strptime('11:25', '%H:%M').time():
                        zigen=st.subheader("4限")
                    elif datetime.strptime('12:55', '%H:%M').time() >=user_time >= datetime.strptime('12:16', '%H:%M').time():
                        zigen=st.subheader("昼休み")
                    elif datetime.strptime('13:10', '%H:%M').time() >=user_time >= datetime.strptime('12:56', '%H:%M').time():
                        zigen=st.subheader("掃除")
                    elif datetime.strptime('13:19', '%H:%M').time() >=user_time >= datetime.strptime('13:11', '%H:%M').time():
                        zigen=st.subheader("掃除と5限の間")
                    elif datetime.strptime('14:10', '%H:%M').time() >=user_time >= datetime.strptime('13:20', '%H:%M').time():
                        zigen=st.subheader("5限")
                    elif datetime.strptime('14:19', '%H:%M').time() >=user_time >= datetime.strptime('14:11', '%H:%M').time():
                        zigen=st.subheader("5限と6限の間")
                    elif datetime.strptime('15:10', '%H:%M').time() >=user_time >= datetime.strptime('14:20', '%H:%M').time():
                        zigen=st.subheader("6限")
                    elif datetime.strptime('15:19', '%H:%M').time() >=user_time >= datetime.strptime('15:11', '%H:%M').time():
                        zigen=st.subheader("6限と7限の間")
                    elif datetime.strptime('16:10', '%H:%M').time() >=user_time >= datetime.strptime('15:20', '%H:%M').time():
                        zigen=st.subheader("7限")
                    elif datetime.strptime('16:19', '%H:%M').time() >=user_time >= datetime.strptime('16:11', '%H:%M').time():
                        zigen=st.subheader("7限とHRAの間")
                    elif datetime.strptime('16:35', '%H:%M').time() >=user_time >= datetime.strptime('16:20', '%H:%M').time():
                        zigen=st.subheader("HRA")
                    else:
                        zigen=st.subheader("放課後")
 
                
               
                # 遅刻証明の情報を表示
                st.subheader(f"名前: {st.session_state.username}")
                st.subheader(f"入力時刻: {get_time}({get_day})")
                st.subheader(f"理由: {reason}")
 
               
                ranndamu = random.randint(100, 999)  # ランダムな3桁の数字
                ranndamu1 = str(ranndamu)  # 文字列に変換
 
                # 文字列として「1221+ranndamu1」を表示
                tikokuninnsyou = "1221" + ranndamu1  # 結果を文字列として設定
 
                # st.text() に渡す際は tikokuninnsyou をそのまま渡す
                st.subheader(f"認証番号{tikokuninnsyou}")  # 正しい文字列を表示
 
                # 遅刻証明書発行のために必要なデータ（ランダムな数字を追加）
                data1 = {"名前": st.session_state.username, "時間": get_time, "理由": reason}
               
                # データ送信 (遅刻証明用)
                send_post_request('https://prod-07.japaneast.logic.azure.com:443/workflows/e30f108c25324d62bfa50133e41c47bb/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=d3BzwwA54bqFHmhHwvCPZaXdScGUHJRS8pWwoXx-pds', data1)
               
                # ランダムな数字を別のURLに送信
                send_post_request('https://prod-01.japaneast.logic.azure.com:443/workflows/38f7b8c8d476411d8d4351e0638c6750/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=DQl_g5amg0IRCFIs1lRiIBvicQ1Z9JI9i7uNgWKKu2g', tikokuninnsyou)
 
                # QRコードを生成して表示
                qr_path = generate_qrcode(data1)  # `generate_qrcode` は独自関数なので、適切に定義が必要です。
                st.image(qr_path, caption="遅刻証明書QRコード")
               
        else:
            if st.button("ログアウト"):
                st.session_state.logged_in = False
                st.session_state.username = ""
                st.success("ログアウトしました")
    else:
        st.subheader("ログイン / サインアップ")
        selected_option = st.radio("選択肢", ["サインアップ", "ログイン"])
 
        if selected_option == "サインアップ":
            signup_username = st.text_input("ユーザー名")
            signup_password = st.text_input("パスワード", type="password")
            signup_confirm_password = st.text_input("パスワード確認", type="password")
            signup_button = st.button("サインアップ")
 
            if signup_button:
                if signup_password == signup_confirm_password:
                    save_user(signup_username, signup_password)
                    st.success("サインアップが完了しました！ログインしてください。")
                else:
                    st.error("パスワードが一致しません。")
 
        if selected_option == "ログイン":
            login_username = st.text_input("ユーザー名", key="login_username")
            login_password = st.text_input("パスワード", type="password", key="login_password")
            login_button = st.button("ログイン")
 
            if login_button:
                user = authenticate_user(login_username, login_password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = login_username
                    st.success(f"ようこそ、{login_username}さん！")
                else:
                    st.error("ユーザー名またはパスワードが間違っています。")
 
with tab5:
    st.text("aa")