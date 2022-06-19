import pandas as pd
import plotly.express as px
from pyrsistent import m
from pytz import HOUR
import streamlit as st 
from streamlit_option_menu import option_menu
from datetime import datetime, timedelta

st.set_page_config(page_title="SLA_Metrics",
                   page_icon=":bar_chart:",
                   layout="wide") 
st.title(":bar_chart:Dashboard")
df=pd.read_excel(
        io="SLA_Metrics.xlsx",
        engine='openpyxl',
        sheet_name='Data',
        usecols='A:O',
        nrows=1000,
)
df[["Date","Months","Clusters","Incident","Downtime(Start)","Downtime(End)"]] = df[["Date","Months","Clusters","Incident","Downtime(Start)","Downtime(End)"]].astype('string')
df["Total Downtime(hrs)"] = (df["Total Downtime(hrs)"]).astype("string")
df[["Repair time(end)","Time since last failure(hrs)","Time to repair(hrs)"]] = df[["Repair time(end)","Time since last failure(hrs)","Time to repair(hrs)"]].astype('string')
df[["Downtime%","SLA_Uptime%"]] =df[["Downtime%","SLA_Uptime%"]].astype('float')


df1=pd.read_excel(
    io="SLA_Metrics.xlsx",
    engine='openpyxl',
    sheet_name='MTBF&MTTR',
    usecols='A:D',
    nrows=1000,
    )
df1[["Month"]] = df1[["Month"]].astype('string')
df1[["MTBF (Hrs)","MTTR (Hrs)"]] = df1[["MTBF (Hrs)","MTTR (Hrs)"]].astype('int')

# 1. as sidebar menu
with st.sidebar: 
    selected = option_menu("Menu", ["Home","Monthly SLA's","MTTR & MTBF"], 
        icons=['house', 'bar-chart-line','bar-chart-line','bar-chart-line'], menu_icon="cast", default_index=1,
        styles={
            "container": {"padding": "0!important", "background-color": "light blue"},
            "icon": {"color": "orange", "font-size": "25px"}, 
            "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px","font-color":"black","--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "blue"},
            },

)



if selected =="Home": 
    st.title("SLA_Entries")
   

if selected =="Monthly SLA's": 
    st.text("Sla_Metrics table for cluster's with downtime") 
    st.dataframe(df)

#-----sidebar-------
    st.sidebar.header("Please Filter Clusters by month:")
    Clusters=st.sidebar.multiselect(
        "Select Clusters:",
        options=df["Clusters"].unique(),
        default=df["Clusters"].unique()
    )

    Months=st.sidebar.multiselect(
        "Select Months:",
        options=df["Months"].unique(),
        default=df["Months"].unique()
    )
    df_selection=df.query(
        "Clusters== @Clusters & Months == @Months")
    
    st.markdown("##")
    st.text("View Filtered records") 
    st.dataframe(df_selection)

#-----mainpage------

    st.markdown("##")

#-----TOP KPI's-----
    average_sla=round(df_selection["SLA_Uptime%"].mean(),2)
    average_downtime=round(df_selection["Downtime%"].mean(),2)


    left_column,right_column=st.columns(2)
    with left_column:
        st.subheader("Average_SLA:")
        st.subheader(f"{average_sla}")
    
   

    with right_column:
        st.subheader("Average Downtime")
        st.subheader(f"{average_downtime}")
    
    st.markdown("---")
#------SLA's by clusters[barchart]---------

    sla_by_clusters=(
        df_selection.groupby(by=["Months"]).mean()[["SLA_Uptime%"]].sort_values(by="SLA_Uptime%")
    )
    st.dataframe(sla_by_clusters)

    fig_clusters=px.bar(
        sla_by_clusters,
        y="SLA_Uptime%",
        x=sla_by_clusters.index,
        title="<b> Monthly SLA's Chart</b>",
        color_discrete_sequence=["#008388"] * len(sla_by_clusters),
        template="plotly_white",
    )

    fig_clusters.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )
    st.plotly_chart(fig_clusters)


if selected == "MTTR & MTBF":
    st.text("MTBF & MTTR TABLE ") 
    st.dataframe(df1)

#-----sidebar-------
    st.sidebar.header("Please Filter Month:")
    Month=st.sidebar.multiselect(
        "Select Month:",
        options=df1["Month"].unique(),
        default=df1["Month"].unique()
    )
    df1_selection=df1.query("Month == @Month")
    st.markdown("##")
    st.text("View Filtered records") 
    st.dataframe(df1_selection)

#-----mainpage------
    st.markdown("##")

#-----TOP KPI's-----
    average_Mtbf=int(df1_selection["MTBF (Hrs)"].mean())
    average_rating=round(df1_selection["Rating"].mean(),2)
    star_rating=":star:"*int(round(average_rating,0))
    average_mttr=int(df1_selection["MTTR (Hrs)"].mean())


    left_column,middle_column,right_column=st.columns(3)
    with left_column:
        st.subheader("MTBF")
        st.subheader(f"{average_Mtbf}")
    
    with middle_column:
        st.subheader("Average Rating of SLA:")
        st.subheader(f"{average_mttr} {star_rating}")

    with right_column:
        st.subheader("MTTR")
        st.subheader(f"{average_mttr}")
    
    st.markdown("---")

#------MTBF [barchart]---------

    sla_by_clusters=(
        df1_selection.groupby(by=["Month"]).sum()[["MTBF (Hrs)"]].sort_values(by="MTBF (Hrs)")
    )
#st.dataframe(MTBF)

    fig_mtbf=px.bar(
        sla_by_clusters,
        y="MTBF (Hrs)",
        x=sla_by_clusters.index,
        title="<b>Monthly MTBF Chart</b>",
        color_discrete_sequence=["#0B3479 "] * len(sla_by_clusters),
        template="plotly_white",
    )

    fig_mtbf.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )
    
    sla_by_clusters=(
        df1_selection.groupby(by=["Month"]).sum()[["MTTR (Hrs)"]].sort_values(by="MTTR (Hrs)")
    )
#st.dataframe(MTTR)

    fig_mttr=px.bar(
        sla_by_clusters,
        y="MTTR (Hrs)",
        x=sla_by_clusters.index,
        title="<b>Monthly MTTR Chart</b>",
        color_discrete_sequence=["#AA432D "] * len(sla_by_clusters),
        template="plotly_white",
    )

    fig_mttr.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )

    left_column,right_column=st.columns(2)

    left_column.plotly_chart(fig_mtbf,use_container_width=True)
    right_column.plotly_chart(fig_mttr,use_container_width=True)


#-------hide streamlit stlye------
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            
            """
st.markdown(hide_st_style,unsafe_allow_html=True)    