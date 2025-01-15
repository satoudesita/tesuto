import streamlit as st
import qrcode
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from PIL import Image

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
st.title("QRコードとバーコードを生成")
st.write("以下のフォームに情報を入力してください。")

# ユーザーが追加する情報の入力項目
fields = ["high school", "glade", "class","name"]

# 初期の入力項目を表示
user_input = {field: st.text_input(field) for field in fields}

# 追加情報の項目をテキストボックスで動的に入力
st.subheader("追加情報を入力（任意)")
additional_fields = []
add_field = st.text_input("項目名")
add_value = st.text_input("その値")

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

    # Code128バーコードに日本語が含まれているか確認
    if any(ord(c) > 127 for c in combined_data):  # 日本語や非ASCII文字を含むかチェック
        st.error("Code128バーコードはASCII文字のみサポートしています。QRコードを使用します。")
    else:
        # バーコードを生成
        st.subheader("生成されたバーコード（Code128）")
        barcode_img = generate_code128_barcode(combined_data)
        st.image(barcode_img, caption="Code128バーコード", use_container_width=True)
