import streamlit as st
from datetime import datetime
import qrcode
import barcode
import requests
from barcode.writer import ImageWriter
from io import BytesIO
from PIL import Image
import pytz

def send_post_request(url, data):
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            st.write("成功: ", response.json())
        else:
            st.write("エラー: ", response.status_code)
    except Exception as e:
        st.write(f"リクエストエラー: {e}")

# タブを作成
tab1, tab2 ,tab3= st.tabs(["QR", "BR","test"])

with tab1:

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

        # PIL Imageをバイナリストリームに変換
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        return img_byte_arr

    # Code128バーコードを生成する関数
    def generate_code128_barcode(data):
        # Code128はASCIIのみサポート
        barcode_class = barcode.get_barcode_class('code128')
        code128 = barcode_class(data, writer=ImageWriter())

        # バーコードをバイナリストリームとして生成
        buffer = BytesIO()
        code128.write(buffer)
        buffer.seek(0)

        return buffer

    # Streamlit UI部分
    st.write("以下のフォームに情報を入力してください。")
    st.write("QRコードは日本語対応可バーコードは日本語対応不可")

    # ユーザーが追加する情報の入力項目
    fields = ["high school", "glade", "class", "name"]

    # 初期の入力項目を表示
    user_input = {field: st.text_input(field) for field in fields}

    # 追加情報の項目をテキストボックスで動的に入力
    st.subheader("add information")
    additional_fields = []
    add_field = st.text_input("the name")
    add_value = st.text_input("the value")

    if add_field and add_value:
        additional_fields.append((add_field, add_value))

    # 入力フォームがすべて埋まった場合
    if all(user_input[field] for field in fields):
        # 名前、電話番号、住所を1つの文字列にまとめる
        combined_data = "\n".join([f"{key}: {value}" for key, value in user_input.items()])

        # 追加された情報を組み合わせ
        for field_name, field_value in additional_fields:
            combined_data += f"\n{field_name}: {field_value}"

        # QRコードを生成
        st.subheader("生成されたQRコード")
        qr_img = generate_qrcode(combined_data)
        st.image(qr_img, caption="QRコード", use_container_width=True)

    with st.expander("バーコード"):
        # ユーザーからの入力を受け取る
        text_input = st.text_input("バーコードにするテキストを入力してください。:")

        # 入力されたテキストでCODE39バーコードを生成
        if text_input:
            try:
                # CODE39バーコードを作成
                code39 = barcode.get_barcode_class('code39')

                # ImageWriterのオプションを設定
                writer = ImageWriter()
                writer_options = {
                    'module_width': 0.1,  # バーコードのモジュール幅
                    'module_height': 3   # バーコードの高さ
                }

                # チェックサムなしのバーコードを作成
                barcode_img = code39(text_input, writer=writer)
                barcode_img = barcode_img.__class__(text_input, writer=writer, add_checksum=False)

                # バーコード画像をメモリ上で保存
                buf = BytesIO()
                barcode_img.write(buf, writer_options)
                buf.seek(0)

                # バーコード画像をStreamlitに表示
                st.image(buf, caption="生成されたCODE39バーコード", use_container_width=True)

            except Exception as e:
                st.error(f"バーコード生成に失敗しました: {e}")

with tab2:

    with st.form(key='my_form', clear_on_submit=True):
        st.text('テキストボックスの内容と時刻を取得')            
        user_input = st.text_input(label='テキストを入力してください:', key='input')

        
        submit_button = st.form_submit_button(label='送信')

    if submit_button and user_input:
        # 日本のタイムゾーンを指定
        japan_tz = pytz.timezone('Asia/Tokyo')
        # 現在の日本時刻を取得
        current_time_japan = datetime.now(japan_tz)
        current_time=current_time_japan.strftime('%m-%d %H:%M')
        # 日本時刻を表示
        st.text(f"入力されたテキスト: {user_input}")
        st.text(f"入力時刻: {current_time}")
        data = {
            "名前": user_input,
            "時間": current_time,
        }
        send_post_request('https://prod-08.japaneast.logic.azure.com:443/workflows/2dad7268f2844042bae005c2ec7916f6/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=V-60f4bGMzshRcghrvSV7qt-WEgKqbgQGfGk2F8BQPk', data)
with tab3:
    API_URL = "https://api.jancodelookup.com/"
    API_ID = "96385e12558d53c366efb3c187ef0440" 

    def search_product_by_code(jan_code):

        params = {
            'appId': API_ID,     # アプリID（
            'query': jan_code,    # JANコード
            'hits': 1,            # 取得件数（1件だけ取得）
            'page': 1,            # 1ページ目を指定
            'type': 'code',       # コード番号検索
        }
        
        # APIにリクエストを送信
        response = requests.get(API_URL, params=params)
        
        # レスポンスのステータスコードを確認
        if response.status_code == 200:
            data = response.json()  # JSONレスポンスをパース
            
        
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
        jan_code = st.text_input(label="JANコードを入力してください",key="search")           
        
        submit_button = st.form_submit_button(label='送信')

    

    if jan_code:
        # 商品を検索
        product = search_product_by_code(jan_code)
        if product:
            st.text("商品情報:")
            st.text(f"商品名: {product.get('itemName', '不明')}")
            st.text(f"品番: {product.get('itemModel', '不明')}")
            st.text(f"ブランド名: {product.get('brandName', '不明')}")
            st.text(f"メーカー名: {product.get('makerName', '不明')}")
            st.text(f"詳細ページ: [商品ページ](https://www.jancodelookup.com/code/{product['codeNumber']})")
            st.image(product.get('itemImageUrl')) 
    else:
        st.text("JANコードを入力してください")
