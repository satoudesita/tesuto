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
    return img

# バーコードを生成する関数
def generate_barcode(data):
    barcode_class = barcode.get_barcode_class('ean13')
    ean = barcode_class(data, writer=ImageWriter())
    
    # バーコードをバイナリストリームとして生成
    buffer = BytesIO()
    ean.write(buffer)
    buffer.seek(0)
    img = Image.open(buffer)
    return img

# Streamlit UI部分
st.title("QRコードとバーコードを生成")
st.write("以下のフォームに情報を入力してください。")

# 入力欄
input_data = st.text_input("QRコードとバーコードに変換するデータを入力:")

if input_data:
    st.subheader("生成されたQRコード")
    # QRコードの表示
    qr_img = generate_qrcode(input_data)
    st.image(qr_img, caption="QRコード", use_column_width=True)

    st.subheader("生成されたバーコード")
    # バーコードの表示
    barcode_img = generate_barcode(input_data)
    st.image(barcode_img, caption="バーコード", use_column_width=True)
