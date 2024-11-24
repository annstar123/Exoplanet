# Home.py
import streamlit as st

page_title = '太陽系外行星資料分析app'
st.set_page_config(page_title=page_title, page_icon=':milky_way', layout='wide')
st.title(page_title)

st.markdown('* Exoplanet data chart頁面呈現從[NASA系外行星資料庫](https://exoplanetarchive.ipac.caltech.edu/)取得的資料表而繪製而成的圖表。')
st.markdown('* Exoplanet table filter頁面呈現從[NASA系外行星資料庫](https://exoplanetarchive.ipac.caltech.edu/)取得的資料表，並提供資料篩選及匯出CSV檔的功能。')