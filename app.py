import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 页面配置
st.set_page_config(
    page_title="AI副业利基市场确定工具",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 顶部静态HTML导航栏
st.markdown('''<div style="text-align:center;margin-bottom:1rem;">
    <a href="#" onclick="window.location.reload()" style="margin:0 10px;font-weight:bold;">🏠 首页</a>
    <a href="#" onclick="window.location.hash='个人评估'" style="margin:0 10px;">📊 个人评估</a>
    <a href="#" onclick="window.location.hash='利基分析'" style="margin:0 10px;">🎯 利基分析</a>
    <a href="#" onclick="window.location.hash='市场趋势'" style="margin:0 10px;">📈 市场趋势</a>
    <a href="#" onclick="window.location.hash='个性化推荐'" style="margin:0 10px;">💡 个性化推荐</a>
    <a href="#" onclick="window.location.hash='行动计划'" style="margin:0 10px;">📋 行动计划</a>
    <a href="#" onclick="window.location.hash='学习资源'" style="margin:0 10px;">📚 学习资源</a>
</div>''', unsafe_allow_html=True)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin-bottom: 1rem;
        color: #222;
    }
    .highlight {
        background-color: #e3f2fd;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 3px solid #2196f3;
        color: #222;
    }
    .success-box {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #4caf50;
    }
    .card h3, .card h4, .card ul, .card ol, .highlight h3, .highlight h4, .highlight ul, .highlight ol {
        color: #222 !important;
    }
</style>
""", unsafe_allow_html=True)

# 导入数据模块
from data import AI_NICHES

def calculate_compatibility_score(user_profile, niche):
    """计算用户与利基市场的匹配度"""
    score = 0
    max_score = 100
    
    # 技能匹配度 (40分)
    skill_match = 0
    for skill in niche["技能要求"]:
        if skill in user_profile.get("skills", []):
            skill_match += 1
    score += (skill_match / len(niche["技能要求"])) * 40
    
    # 时间投入匹配度 (20分)
    time_preference = user_profile.get("time_availability", "中等")
    time_scores = {"低": 1, "中等": 2, "高": 3}
    niche_time = time_scores.get(niche["时间投入"], 2)
    user_time = time_scores.get(time_preference, 2)
    time_match = 1 - abs(niche_time - user_time) / 2
    score += time_match * 20
    
    # 投资能力匹配度 (20分)
    investment_preference = user_profile.get("investment_capacity", "中等")
    investment_scores = {"低": 1, "中等": 2, "高": 3}
    niche_investment = investment_scores.get(niche["投资成本"], 2)
    user_investment = investment_scores.get(investment_preference, 2)
    investment_match = 1 - abs(niche_investment - user_investment) / 2
    score += investment_match * 20
    
    # 兴趣匹配度 (20分)
    interest_match = 0
    for interest in user_profile.get("interests", []):
        if interest in niche["适合人群"] or interest in niche["description"]:
            interest_match += 1
    score += min(interest_match * 10, 20)
    
    return round(score, 1)

def main():
    st.markdown('<h1 class="main-header">🤖 AI副业利基市场确定工具</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">帮助小白找到最适合的AI副业方向</p>', unsafe_allow_html=True)
    
    # 侧边栏导航菜单
    st.sidebar.title("导航菜单")
    page = st.sidebar.selectbox(
        "选择功能",
        ["首页", "个人评估", "利基分析", "市场趋势", "个性化推荐", "行动计划", "学习资源"]
    )
    
    # 页面路由
    if page == "首页":
        show_homepage()
    elif page == "个人评估":
        show_assessment()
    elif page == "利基分析":
        show_niche_analysis()
    elif page == "市场趋势":
        show_market_trends()
    elif page == "个性化推荐":
        show_personalized_recommendations()
    elif page == "行动计划":
        show_action_plan()
    elif page == "学习资源":
        show_learning_resources()

def show_homepage():
    st.markdown('<h2 class="sub-header">欢迎使用AI副业利基市场确定工具</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>🎯 工具功能</h3>
            <ul>
                <li>个人能力与兴趣评估</li>
                <li>AI副业机会分析</li>
                <li>市场需求趋势分析</li>
                <li>个性化推荐系统</li>
                <li>详细行动计划制定</li>
                <li>学习资源推荐</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>🚀 使用步骤</h3>
            <ol>
                <li>完成个人评估问卷</li>
                <li>查看利基市场分析</li>
                <li>了解市场趋势</li>
                <li>获得个性化推荐</li>
                <li>制定行动计划</li>
                <li>开始学习实践</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="highlight">
        <h3>💡 为什么选择AI副业？</h3>
        <p>AI技术正在改变各行各业，为普通人创造了大量副业机会。无论是内容创作、应用开发、还是咨询服务，AI都能帮助你提高效率、降低成本、创造价值。</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 新增支付宝打赏区块
    st.markdown("""
    <div style='text-align:center;margin:2rem 0;'>
        <h3 style='color:#1f77b4;'>☕ 觉得好用请请我喝杯奶茶</h3>
        <p style='color:#444;'>你的支持是我持续优化的最大动力！</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    st.image("alipay_qr.png", caption="支付宝扫码支持作者", width=220)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 快速开始按钮
    if st.button("🚀 开始我的AI副业之旅", type="primary", use_container_width=True):
        st.info("请在左侧菜单选择“个人评估”开始你的AI副业探索之旅。")

def show_assessment():
    st.markdown('<h2 class="sub-header">📊 个人能力与兴趣评估</h2>', unsafe_allow_html=True)
    
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = {}
    
    with st.form("assessment_form"):
        st.markdown("### 基本信息")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("姓名（可选）")
            age = st.selectbox("年龄段", ["18-25岁", "26-35岁", "36-45岁", "46岁以上"])
            education = st.selectbox("教育背景", ["高中", "大专", "本科", "硕士", "博士"])
        
        with col2:
            occupation = st.text_input("当前职业")
            experience_years = st.selectbox("工作经验", ["无经验", "1-3年", "4-6年", "7-10年", "10年以上"])
            available_time = st.selectbox("每周可用于副业的时间", ["5小时以下", "5-10小时", "10-20小时", "20小时以上"])
        
        st.markdown("### 技能评估")
        st.markdown("请选择你具备的技能（可多选）：")
        
        skills = st.multiselect(
            "技能选择",
            ["编程基础", "写作能力", "设计能力", "营销能力", "项目管理", "数据分析", 
             "沟通能力", "创意思维", "学习能力", "时间管理", "客户服务", "销售能力"],
            default=[]
        )
        
        st.markdown("### 兴趣偏好")
        interests = st.multiselect(
            "感兴趣的领域",
            ["技术开发", "内容创作", "教育培训", "咨询服务", "销售推广", "数据分析", 
             "创意设计", "写作编辑", "视频制作", "音频制作", "游戏开发", "电商运营"],
            default=[]
        )
        
        st.markdown("### 投资能力")
        investment = st.selectbox(
            "可用于副业的投资金额",
            ["1000元以下", "1000-5000元", "5000-20000元", "20000元以上"]
        )
        
        st.markdown("### 目标期望")
        income_goal = st.selectbox(
            "副业收入目标",
            ["每月1000元以下", "每月1000-3000元", "每月3000-8000元", "每月8000元以上"]
        )
        
        risk_tolerance = st.selectbox(
            "风险承受能力",
            ["保守型", "稳健型", "积极型", "激进型"]
        )
        
        submitted = st.form_submit_button("提交评估", type="primary")
        
        if submitted:
            st.session_state.user_profile = {
                "name": name,
                "age": age,
                "education": education,
                "occupation": occupation,
                "experience_years": experience_years,
                "time_availability": available_time,
                "skills": skills,
                "interests": interests,
                "investment_capacity": investment,
                "income_goal": income_goal,
                "risk_tolerance": risk_tolerance,
                "assessment_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            st.success("✅ 评估完成！请查看个性化推荐。")
            st.balloons()

# 导入其他页面函数
from pages import (
    show_niche_analysis, 
    show_market_trends, 
    show_personalized_recommendations,
    show_action_plan, 
    show_learning_resources
)

# 测试推送

if __name__ == "__main__":
    main() 