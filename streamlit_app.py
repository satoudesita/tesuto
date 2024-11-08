import streamlit as st
import datetime
import time

tab_titles = ['たいせい', 'はお']
tab1, tab2 = st.tabs(tab_titles)
 
# 各タブにコンテンツを追加
with tab1:
    st.header('Topic A')
    st.write('Topic Aのコンテンツ')
    def main():
        st.title("Streamlit 目覚まし時計")

        # 現在時刻の表示
        current_time_placeholder = st.empty()

        # アラーム設定
        alarm_time = st.time_input("アラーム時刻を設定してください")
        
        if st.button("アラームをセット"):
            st.success(f"アラームを {alarm_time.strftime('%H:%M')} にセットしました。")

        # アラームのオン/オフ切り替え
        alarm_enabled = st.checkbox("アラームを有効にする", value=True)

        while True:
            now = datetime.datetime.now()
            current_time_placeholder.header(f"現在時刻: {now.strftime('%H:%M:%S')}")

            if alarm_enabled and now.time().strftime("%H:%M") == alarm_time.strftime("%H:%M"):
                st.warning("アラーム時刻です！")
                break

            time.sleep(1)

    if __name__ == "__main__":
        main()

with tab2:

    # 初期化
    if 'input_count' not in st.session_state:
        st.session_state.input_count = 3  # 最初に表示する入力フィールドの数

    nyuuryokusuu = st.number_input("入力するフィールド数を決める", value=0, step=1)

    # ボタンが押されたときに入力フィールドの数を増やす
    if st.button("入力フィールドを増やす"):
        st.session_state.input_count += nyuuryokusuu  # 追加した数だけ入力フィールドを増やす

    # ぐるーぷA
    st.write("ぐるーぷA")

    # 入力値を保存するリストを初期化
    goukeia = 0
    aa = []

    # ぐるーぷAの入力フィールドを表示し、合計とリストに値を追加
    for i in range(st.session_state.input_count):
        input_value = st.number_input(f"数字を入力してください {i+1}", value=0.0, step=0.5, key=f"A_{i+1}")
        aa.append(input_value)  # 入力値をリストに追加
        goukeia += input_value

    # 合計と平均を表示
    st.text(f"ぐるーぷAの合計: {goukeia}")
    heikin = goukeia / st.session_state.input_count
    st.text(f"ぐるーぷAの平均: {heikin}")

    # 各入力値と平均との差を表示
    squared_deviations = []  # 偏差の二乗を保存するリスト
    for i in range(st.session_state.input_count):
        deviation = aa[i] - heikin
        squared_deviation = deviation ** 2
        squared_deviations.append(squared_deviation)
        st.text(f"{i+1}: {aa[i]} と 平均との差: {deviation} と 偏差の二乗: {squared_deviation}")

    # 偏差の二乗の平均（分散）を計算
    variance = sum(squared_deviations) / st.session_state.input_count
    st.text(f"ぐるーぷAの分散: {variance}")

    # 標準偏差を計算（分散の平方根）
    standard_deviation = variance ** 0.5
    st.text(f"ぐるーぷAの標準偏差: {standard_deviation}")

    # ぐるーぷB
    st.write("ぐるーぷB")

    # ぐるーぷBの入力値を保存するリストを初期化
    goukeib = 0
    aaa = []

    # ぐるーぷBの入力フィールドを表示し、合計とリストに値を追加
    for i in range(st.session_state.input_count):
        input_value_b = st.number_input(f"数字を入力してください {i+1}", value=0.0, step=0.5, key=f"C_{i+1}")
        aaa.append(input_value_b)  # 入力値をリストに追加
        goukeib += input_value_b

    # 合計と平均を表示
    st.text(f"ぐるーぷBの合計: {goukeib}")
    heikin_b = goukeib / st.session_state.input_count
    st.text(f"ぐるーぷBの平均: {heikin_b}")

    # 各入力値と平均との差を表示
    squared_deviations_b = []  # 偏差の二乗を保存するリスト
    for i in range(st.session_state.input_count):
        deviation_b = aaa[i] - heikin_b
        squared_deviation_b = deviation_b ** 2
        squared_deviations_b.append(squared_deviation_b)
        st.text(f"{i+1}: {aaa[i]} と 平均との差: {deviation_b} と 偏差の二乗: {squared_deviation_b}")

    # 偏差の二乗の平均（分散）を計算
    variance_b = sum(squared_deviations_b) / st.session_state.input_count
    st.text(f"ぐるーぷBの分散: {variance_b}")

    # 標準偏差を計算（分散の平方根）
    standard_deviation_b = variance_b ** 0.5
    st.text(f"ぐるーぷBの標準偏差: {standard_deviation_b}")

    # 共分散の計算
    covariance = 0
    for i in range(st.session_state.input_count):
        covariance += (aa[i] - heikin) * (aaa[i] - heikin_b)

    covariance /= st.session_state.input_count
    st.text(f"ぐるーぷAとぐるーぷBの共分散: {covariance}")
