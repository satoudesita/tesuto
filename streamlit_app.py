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

# 入力欄
input_data = st.text_input("QRコードとバーコードに変換するデータを入力:")

if input_data:
    st.subheader("生成されたQRコード")
    # QRコードの表示
    qr_img = generate_qrcode(input_data)
    st.image(qr_img, caption="QRコード", use_container_width=True)

    # Code128バーコードに日本語が含まれているか確認
    if any(ord(c) > 127 for c in input_data):  # 日本語や非ASCII文字を含むかチェック
        st.error("Code128バーコードはASCII文字のみサポートしています。QRコードを使用します。")
    else:
        st.subheader("生成されたバーコード（Code128）")
        # Code128バーコードの表示
        barcode_img = generate_code128_barcode(input_data)
        st.image(barcode_img, caption="Code128バーコード", use_container_width=True)
