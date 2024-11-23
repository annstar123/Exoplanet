# exoplanet_table_filter.py
import streamlit as st
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

page_title = '系外行星資料表篩選器'
st.title(page_title)
st.info('藉由[Astroquery](https://astroquery.readthedocs.io/en/latest/ipac/nexsci/nasa_exoplanet_archive.html)套件取得[NASA系外行星資料庫](https://exoplanetarchive.ipac.caltech.edu/)提供的資料表，篩選出所需資料後匯出CSV檔。')


@st.cache_data(ttl=86400, show_spinner=False)
def get_exoplanet_table_by_astroquery():
    table_name = 'pscomppars'
    columns = 'pl_name,hostname,sy_dist,pl_orbper,pl_bmasse,pl_rade,disc_year,discoverymethod'
    exoplanet_table = NasaExoplanetArchive.query_criteria(
        table=table_name, select=columns
    )
    exoplanet_table = exoplanet_table.to_pandas()  
    exoplanet_table = exoplanet_table.rename(
        columns={
            'pl_name': '行星名稱',
            'hostname': '所屬恆星名稱',
            'sy_dist': '與地球的距離(單位：秒差距)',
            'pl_orbper': '行星軌道週期(單位：天)',
            'pl_bmasse': '行星質量(單位：地球質量)',
            'pl_rade': '行星半徑(單位：地球半徑)',
            'disc_year': '發現年份',
            'discoverymethod': '發現方法'
        }
    )
    exoplanet_table.sort_values(
        by='發現年份', ascending=False, inplace=True, ignore_index=True
    )

    return exoplanet_table
# 主邏輯: 獲取資料並顯示於界面
# 主邏輯: 獲取資料並顯示於界面
try:
    # 獲取完整的資料表
    exoplanet_table = get_exoplanet_table_by_astroquery()

    # 主頁面 - 名稱篩選
    st.subheader("行星名稱篩選")
    text_search = st.text_input("搜尋行星名稱 (可部分匹配):", value="")
    if text_search:
        exoplanet_table = exoplanet_table[
            exoplanet_table['行星名稱'].str.contains(text_search, case=False, na=False)
        ]

    # 側邊欄 - 年份篩選
    st.sidebar.subheader("篩選條件")
    if not exoplanet_table.empty:
        year_min = int(exoplanet_table['發現年份'].min())
        year_max = int(exoplanet_table['發現年份'].max())
        year_range = st.sidebar.select_slider(
            '發現年份區間:',
            options=list(range(year_min, year_max + 1)),
            value=(year_min, year_max),
        )
        # 篩選年份區間
        exoplanet_table = exoplanet_table[
            (exoplanet_table['發現年份'] >= year_range[0]) &
            (exoplanet_table['發現年份'] <= year_range[1])
        ]
    else:
        st.sidebar.warning("沒有可用的年份篩選選項，因為名稱篩選後的資料表為空。")

    # 側邊欄 - 發現方法篩選
    method_lst = sorted(list(exoplanet_table['發現方法'].unique()))
    selected_method = st.sidebar.selectbox(
        '發現方法:', ['不限'] + method_lst
    )
    if selected_method != '不限':
        exoplanet_table = exoplanet_table[exoplanet_table['發現方法'] == selected_method]

    # 側邊欄 - 去除空值的欄位篩選
    column_name_lst = list(exoplanet_table.columns)
    selected_columns = st.sidebar.multiselect(
        '移除某些欄位值為空值的行星:', column_name_lst
    )
    if selected_columns:
        exoplanet_table = exoplanet_table.dropna(subset=selected_columns)

    # 顯示篩選結果
    st.dataframe(exoplanet_table)

except Exception as e:
    st.error(f"資料獲取失敗: {e}")

# 使用 AgGrid 顯示資料表
gb = GridOptionsBuilder.from_dataframe(exoplanet_table)
gb.configure_column('行星名稱', pinned='left')
for col in exoplanet_table.columns.values.tolist():
    gb.configure_column(col, suppressMovable=True, suppressMenu=True)

gridOptions = gb.build()
AgGrid(
    exoplanet_table,
    gridOptions=gridOptions,
    allow_unsafe_jscode=True,
    height=400,
    theme='balham'
)

# 匯出資料功能
st.sidebar.download_button(
    label='將篩選資料表匯出成CSV檔',
    data=exoplanet_table.to_csv(index=False),
    file_name='exoplanet_table.csv',
    mime='text/csv'
)

# 清除快取按鈕
if st.sidebar.button('清除資料表快取'):
    st.cache_data.clear()
    st.balloons()
    st.sidebar.success('已清除快取，請重新載入頁面')
