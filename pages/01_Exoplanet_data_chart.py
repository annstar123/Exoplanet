import streamlit as st
import plotly.express as px
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive

def plot_discovery_method_piechart(exoplanet_table):
    fig = px.pie(
        exoplanet_table, names='發現方法', color='發現方法', title='各種發現系外行星方法的佔比'
    )

    return st.plotly_chart(fig, use_container_width=True)


def plot_histogram(exoplanet_table, column_name):
 fig = px.histogram(
        exoplanet_table, x=column_name, nbins=100,
    )
 fig.update_layout(
  yaxis_title='數量'
 )

 return st.plotly_chart(fig, use_container_width=True)

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
exoplanet_table=get_exoplanet_table_by_astroquery()
col1, col2 = st.columns(2)
with col1:
    plot_discovery_method_piechart(exoplanet_table)

with col2:
    column_name = st.radio(
        '切換直方圖要統計數量的欄位',
        ['發現年份', '行星質量(單位：地球質量)', '行星半徑(單位：地球半徑)', '行星軌道週期(單位：天)'],
        horizontal=True
    )
    plot_histogram(exoplanet_table, column_name)