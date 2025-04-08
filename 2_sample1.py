import time

import streamlit as st

import numpy as np
import pandas as pd

st.title('我的第一個應用程式')

st.write("嘗試創建**表格**：")

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})
df


chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])
st.line_chart(chart_data)


map_data = pd.DataFrame(
    np.random.randn(100, 2) / [50, 50] + [22.6, 120.4],
    columns=['lat', 'lon'])
st.map(map_data)


if st.button('不要按!'):
    st.text("不是叫你不要按了嗎！")


if st.checkbox('顯示地圖圖表'):
    map_data = pd.DataFrame(
        np.random.randn(100, 2) / [50, 50] + [22.6, 120.4],
        columns=['lat', 'lon'])
    st.map(map_data)


# option = st.selectbox(
#     '你喜歡哪種動物？',
#     ['狗', '貓', '鸚鵡', '天竺鼠'])
# st.text(f'你的答案：{option}')



option = st.sidebar.selectbox(
    '你喜歡哪種動物？',
    ['狗', '貓', '鸚鵡', '天竺鼠'])
st.sidebar.text(f'你的答案：{option}')


expander = st.expander("點擊來展開...")
expander.write("如果你要顯示很多文字，但又不想佔大半空間，可以使用這種方式。")


bar = st.progress(0)
for i in range(100):
    bar.progress(i + 1, f'目前進度 {i+1} %')
    time.sleep(0.05)

bar.progress(100, '載入完成！')