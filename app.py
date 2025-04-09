import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime
import hashlib

# 页面配置
st.set_page_config(
    page_title="渠道管理系统",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 常量定义
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# 用户认证
def check_password():
    """检查用户密码"""
    def password_entered():
        if st.session_state["password"] == hashlib.sha256("admin123".encode()).hexdigest():
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("请输入密码", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("密码错误，请重试", type="password", on_change=password_entered, key="password")
        return False
    else:
        return True

# 数据加载和保存函数
def load_data(file_name):
    path = os.path.join(DATA_DIR, file_name)
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()

def save_data(df, file_name):
    path = os.path.join(DATA_DIR, file_name)
    df.to_csv(path, index=False)

# 主页面
if check_password():
    st.title("📊 渠道管理系统")
    
    # 侧边栏
    with st.sidebar:
        st.header("功能导航")
        page = st.radio(
            "选择功能",
            ["数据概览", "渠道管理", "产品管理", "流水管理", "结算管理", "回款管理"]
        )
    
    if page == "数据概览":
        st.header("📈 数据概览")
        col1, col2 = st.columns(2)
        
        with col1:
            df_flow = load_data("渠道流水.csv")
            if not df_flow.empty:
                fig = px.line(df_flow, x="日期", y="充值流水", title="渠道流水趋势")
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            df_payment = load_data("回款进度.csv")
            if not df_payment.empty:
                fig = px.bar(df_payment, x="渠道", y="回款金额", title="回款情况")
                st.plotly_chart(fig, use_container_width=True)
    
    elif page == "渠道管理":
        st.header("📋 渠道信息管理")
        df = load_data("渠道信息.csv")
        
        # 添加新渠道
        with st.expander("添加新渠道"):
            with st.form("new_channel"):
                channel_name = st.text_input("渠道名称")
                contact = st.text_input("联系人")
                phone = st.text_input("联系电话")
                submit = st.form_submit_button("添加")
                if submit:
                    new_row = pd.DataFrame({
                        "渠道名称": [channel_name],
                        "联系人": [contact],
                        "联系电话": [phone]
                    })
                    df = pd.concat([df, new_row], ignore_index=True)
                    save_data(df, "渠道信息.csv")
                    st.success("添加成功！")
        
        st.dataframe(df, use_container_width=True)
    
    elif page == "产品管理":
        st.header("📦 签约产品管理")
        df = load_data("签约产品.csv")
        
        # 添加新产品
        with st.expander("添加新产品"):
            with st.form("new_product"):
                product_name = st.text_input("产品名称")
                channel = st.text_input("签约渠道")
                start_date = st.date_input("开始日期")
                end_date = st.date_input("结束日期")
                submit = st.form_submit_button("添加")
                if submit:
                    new_row = pd.DataFrame({
                        "产品名称": [product_name],
                        "签约渠道": [channel],
                        "开始日期": [start_date],
                        "结束日期": [end_date]
                    })
                    df = pd.concat([df, new_row], ignore_index=True)
                    save_data(df, "签约产品.csv")
                    st.success("添加成功！")
        
        st.dataframe(df, use_container_width=True)
    
    elif page == "流水管理":
        st.header("📈 渠道流水管理")
        df = load_data("渠道流水.csv")
        
        # 添加新流水
        with st.expander("添加新流水"):
            with st.form("new_flow"):
                channel = st.text_input("渠道")
                date = st.date_input("日期")
                amount = st.number_input("充值流水", min_value=0.0)
                submit = st.form_submit_button("添加")
                if submit:
                    new_row = pd.DataFrame({
                        "渠道": [channel],
                        "日期": [date],
                        "充值流水": [amount],
                        "分成金额": [amount * 0.3]  # 30%分成
                    })
                    df = pd.concat([df, new_row], ignore_index=True)
                    save_data(df, "渠道流水.csv")
                    st.success("添加成功！")
        
        st.dataframe(df, use_container_width=True)
    
    elif page == "结算管理":
        st.header("💰 结算账期管理")
        df = load_data("结算账期.csv")
        
        # 添加新账期
        with st.expander("添加新账期"):
            with st.form("new_settlement"):
                channel = st.text_input("渠道")
                period = st.text_input("账期")
                amount = st.number_input("结算金额", min_value=0.0)
                status = st.selectbox("状态", ["待结算", "已结算"])
                submit = st.form_submit_button("添加")
                if submit:
                    new_row = pd.DataFrame({
                        "渠道": [channel],
                        "账期": [period],
                        "结算金额": [amount],
                        "状态": [status]
                    })
                    df = pd.concat([df, new_row], ignore_index=True)
                    save_data(df, "结算账期.csv")
                    st.success("添加成功！")
        
        st.dataframe(df, use_container_width=True)
    
    elif page == "回款管理":
        st.header("🧾 回款进度管理")
        df = load_data("回款进度.csv")
        
        # 添加新回款
        with st.expander("添加新回款"):
            with st.form("new_payment"):
                channel = st.text_input("渠道")
                amount = st.number_input("回款金额", min_value=0.0)
                date = st.date_input("回款日期")
                submit = st.form_submit_button("添加")
                if submit:
                    new_row = pd.DataFrame({
                        "渠道": [channel],
                        "回款金额": [amount],
                        "回款日期": [date]
                    })
                    df = pd.concat([df, new_row], ignore_index=True)
                    save_data(df, "回款进度.csv")
                    st.success("添加成功！")
        
        st.dataframe(df, use_container_width=True)
