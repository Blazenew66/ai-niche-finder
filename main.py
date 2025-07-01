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
    }
    .highlight {
        background-color: #e3f2fd;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 3px solid #2196f3;
    }
    .success-box {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #4caf50;
    }
</style>
""", unsafe_allow_html=True)

# AI副业机会数据
AI_NICHES = {
    "内容创作": {
        "description": "使用AI工具创作文章、视频、图片等内容",
        "技能要求": ["写作能力", "创意思维", "AI工具使用"],
        "投资成本": "低",
        "时间投入": "中等",
        "收入潜力": "中等",
        "市场需求": "高",
        "竞争程度": "中等",
        "适合人群": ["文字工作者", "创意人员", "自媒体从业者"],
        "工具推荐": ["ChatGPT", "Midjourney", "Canva", "剪映"],
        "学习资源": ["AI写作教程", "视频制作课程", "营销策略"],
        "启动步骤": [
            "学习AI内容创作工具",
            "确定内容主题和风格",
            "建立内容发布平台",
            "制定内容发布计划"
        ]
    },
    "AI应用开发": {
        "description": "开发基于AI的应用程序或工具",
        "技能要求": ["编程基础", "AI/ML知识", "产品思维"],
        "投资成本": "中等",
        "时间投入": "高",
        "收入潜力": "高",
        "市场需求": "高",
        "竞争程度": "中等",
        "适合人群": ["程序员", "产品经理", "技术爱好者"],
        "工具推荐": ["Python", "OpenAI API", "Hugging Face", "Streamlit"],
        "学习资源": ["Python编程", "机器学习基础", "API开发"],
        "启动步骤": [
            "学习Python和AI基础",
            "熟悉常用AI API",
            "确定应用场景",
            "开发MVP版本"
        ]
    },
    "AI咨询服务": {
        "description": "为企业或个人提供AI技术咨询和实施服务",
        "技能要求": ["AI专业知识", "沟通能力", "项目管理"],
        "投资成本": "低",
        "时间投入": "中等",
        "收入潜力": "高",
        "市场需求": "高",
        "竞争程度": "低",
        "适合人群": ["AI专业人士", "咨询师", "技术专家"],
        "工具推荐": ["ChatGPT", "Notion", "Zoom", "项目管理工具"],
        "学习资源": ["AI技术趋势", "咨询技巧", "行业知识"],
        "启动步骤": [
            "建立专业形象",
            "确定服务范围",
            "制定收费标准",
            "寻找潜在客户"
        ]
    },
    "AI教育培训": {
        "description": "教授他人如何使用AI工具和技术",
        "技能要求": ["教学能力", "AI知识", "课程设计"],
        "投资成本": "低",
        "时间投入": "中等",
        "收入潜力": "中等",
        "市场需求": "高",
        "竞争程度": "中等",
        "适合人群": ["教师", "培训师", "AI爱好者"],
        "工具推荐": ["在线教学平台", "录屏软件", "互动工具"],
        "学习资源": ["教学设计", "AI技术", "营销推广"],
        "启动步骤": [
            "设计课程大纲",
            "准备教学材料",
            "选择教学平台",
            "开始招生推广"
        ]
    },
    "AI数据标注": {
        "description": "为AI模型训练提供数据标注服务",
        "技能要求": ["注意力集中", "理解能力", "耐心"],
        "投资成本": "极低",
        "时间投入": "高",
        "收入潜力": "低",
        "市场需求": "中等",
        "竞争程度": "高",
        "适合人群": ["学生", "兼职工作者", "时间充裕者"],
        "工具推荐": ["标注平台", "时间管理工具"],
        "学习资源": ["标注规范", "效率提升技巧"],
        "启动步骤": [
            "注册标注平台",
            "学习标注规范",
            "提高标注效率",
            "建立稳定收入"
        ]
    },
    "AI产品代理": {
        "description": "代理销售AI相关产品和服务",
        "技能要求": ["销售能力", "市场洞察", "客户服务"],
        "投资成本": "中等",
        "时间投入": "中等",
        "收入潜力": "中等",
        "市场需求": "高",
        "竞争程度": "中等",
        "适合人群": ["销售人员", "创业者", "网络营销者"],
        "工具推荐": ["CRM系统", "社交媒体", "电商平台"],
        "学习资源": ["销售技巧", "AI产品知识", "营销策略"],
        "启动步骤": [
            "选择代理产品",
            "建立销售渠道",
            "制定营销策略",
            "开始推广销售"
        ]
    }
}

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
    
    # 侧边栏导航
    st.sidebar.title("导航菜单")
    page = st.sidebar.selectbox(
        "选择功能",
        ["🏠 首页", "📊 个人评估", "🎯 利基分析", "📈 市场趋势", "💡 个性化推荐", "📋 行动计划", "📚 学习资源"]
    )
    
    if page == "🏠 首页":
        show_homepage()
    elif page == "📊 个人评估":
        show_assessment()
    elif page == "🎯 利基分析":
        show_niche_analysis()
    elif page == "📈 市场趋势":
        show_market_trends()
    elif page == "💡 个性化推荐":
        show_personalized_recommendations()
    elif page == "📋 行动计划":
        show_action_plan()
    elif page == "📚 学习资源":
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
    
    # 快速开始按钮
    if st.button("🚀 开始我的AI副业之旅", type="primary", use_container_width=True):
        st.session_state.current_page = "assessment"
        st.rerun()

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

def show_niche_analysis():
    st.markdown('<h2 class="sub-header">🎯 AI副业利基市场分析</h2>', unsafe_allow_html=True)
    
    # 创建数据框用于可视化
    niches_data = []
    for niche_name, niche_info in AI_NICHES.items():
        niches_data.append({
            "利基市场": niche_name,
            "市场需求": niche_info["市场需求"],
            "竞争程度": niche_info["竞争程度"],
            "收入潜力": niche_info["收入潜力"],
            "投资成本": niche_info["投资成本"],
            "时间投入": niche_info["时间投入"]
        })
    
    df = pd.DataFrame(niches_data)
    
    # 市场需求 vs 竞争程度散点图
    fig1 = px.scatter(
        df, 
        x="竞争程度", 
        y="市场需求",
        size="收入潜力",
        color="投资成本",
        hover_name="利基市场",
        title="AI副业机会分析矩阵",
        labels={"竞争程度": "竞争程度", "市场需求": "市场需求", "收入潜力": "收入潜力", "投资成本": "投资成本"}
    )
    fig1.update_layout(height=500)
    st.plotly_chart(fig1, use_container_width=True)
    
    # 详细分析表格
    st.markdown("### 详细市场分析")
    
    for niche_name, niche_info in AI_NICHES.items():
        with st.expander(f"📊 {niche_name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**描述：** {niche_info['description']}")
                st.markdown(f"**技能要求：** {', '.join(niche_info['技能要求'])}")
                st.markdown(f"**适合人群：** {', '.join(niche_info['适合人群'])}")
                
            with col2:
                metrics_col1, metrics_col2 = st.columns(2)
                with metrics_col1:
                    st.metric("市场需求", niche_info["市场需求"])
                    st.metric("收入潜力", niche_info["收入潜力"])
                with metrics_col2:
                    st.metric("竞争程度", niche_info["竞争程度"])
                    st.metric("投资成本", niche_info["投资成本"])
            
            st.markdown("**推荐工具：**")
            for tool in niche_info["工具推荐"]:
                st.markdown(f"- {tool}")
            
            st.markdown("**启动步骤：**")
            for i, step in enumerate(niche_info["启动步骤"], 1):
                st.markdown(f"{i}. {step}")

def show_market_trends():
    st.markdown('<h2 class="sub-header">📈 AI副业市场趋势分析</h2>', unsafe_allow_html=True)
    
    # 模拟市场趋势数据
    trends_data = {
        "月份": ["2024-01", "2024-02", "2024-03", "2024-04", "2024-05", "2024-06"],
        "内容创作": [100, 120, 140, 160, 180, 200],
        "AI应用开发": [80, 100, 130, 170, 220, 280],
        "AI咨询服务": [60, 80, 110, 150, 200, 250],
        "AI教育培训": [90, 110, 130, 150, 170, 190],
        "AI数据标注": [70, 75, 80, 85, 90, 95],
        "AI产品代理": [50, 70, 90, 120, 150, 180]
    }
    
    df_trends = pd.DataFrame(trends_data)
    
    # 趋势线图
    fig = go.Figure()
    
    for niche in ["内容创作", "AI应用开发", "AI咨询服务", "AI教育培训", "AI数据标注", "AI产品代理"]:
        fig.add_trace(go.Scatter(
            x=df_trends["月份"],
            y=df_trends[niche],
            mode='lines+markers',
            name=niche,
            line=dict(width=3)
        ))
    
    fig.update_layout(
        title="AI副业市场趋势（2024年上半年）",
        xaxis_title="月份",
        yaxis_title="市场需求指数",
        height=500,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 市场洞察
    st.markdown("### 📊 市场洞察")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h4>🔥 快速增长领域</h4>
            <ul>
                <li><strong>AI应用开发</strong> - 增长250%</li>
                <li><strong>AI咨询服务</strong> - 增长317%</li>
                <li><strong>AI产品代理</strong> - 增长260%</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h4>📈 稳定增长领域</h4>
            <ul>
                <li><strong>内容创作</strong> - 增长100%</li>
                <li><strong>AI教育培训</strong> - 增长111%</li>
                <li><strong>AI数据标注</strong> - 增长36%</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # 未来预测
    st.markdown("### 🔮 未来趋势预测")
    st.markdown("""
    <div class="highlight">
        <h4>2024年下半年预测</h4>
        <ul>
            <li><strong>AI应用开发</strong>将继续保持高速增长，预计增长300%</li>
            <li><strong>AI咨询服务</strong>需求将进一步扩大，企业AI转型需求激增</li>
            <li><strong>内容创作</strong>将更加智能化，AI辅助创作工具普及</li>
            <li><strong>教育培训</strong>市场将出现更多细分领域</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def show_personalized_recommendations():
    st.markdown('<h2 class="sub-header">💡 个性化推荐</h2>', unsafe_allow_html=True)
    
    if "user_profile" not in st.session_state or not st.session_state.user_profile:
        st.warning("⚠️ 请先完成个人评估以获得个性化推荐")
        if st.button("去完成评估"):
            st.session_state.current_page = "assessment"
            st.rerun()
        return
    
    user_profile = st.session_state.user_profile
    
    # 计算匹配度
    recommendations = []
    for niche_name, niche_info in AI_NICHES.items():
        score = calculate_compatibility_score(user_profile, niche_info)
        recommendations.append({
            "利基市场": niche_name,
            "匹配度": score,
            "描述": niche_info["description"],
            "技能要求": niche_info["技能要求"],
            "收入潜力": niche_info["收入潜力"],
            "投资成本": niche_info["投资成本"]
        })
    
    # 按匹配度排序
    recommendations.sort(key=lambda x: x["匹配度"], reverse=True)
    
    # 显示推荐结果
    st.markdown("### 🎯 为你推荐的AI副业方向")
    
    # 雷达图
    top_3 = recommendations[:3]
    categories = [rec["利基市场"] for rec in top_3]
    scores = [rec["匹配度"] for rec in top_3]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=categories,
        fill='toself',
        name='匹配度',
        line_color='rgb(32, 201, 151)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False,
        title="前3个推荐方向的匹配度分析"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 详细推荐
    for i, rec in enumerate(recommendations[:3], 1):
        with st.expander(f"🥇 第{i}名：{rec['利基市场']} (匹配度: {rec['匹配度']}%)", expanded=i==1):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**描述：** {rec['描述']}")
                st.markdown(f"**收入潜力：** {rec['收入潜力']}")
                st.markdown(f"**投资成本：** {rec['投资成本']}")
                
            with col2:
                st.markdown("**所需技能：**")
                for skill in rec['技能要求']:
                    if skill in user_profile.get('skills', []):
                        st.markdown(f"✅ {skill}")
                    else:
                        st.markdown(f"❌ {skill}")
            
            # 个性化建议
            st.markdown("**💡 个性化建议：**")
            if rec['匹配度'] >= 80:
                st.success("🎉 这是一个非常适合你的方向！建议优先考虑。")
            elif rec['匹配度'] >= 60:
                st.info("👍 这是一个不错的选择，需要一些技能提升。")
            else:
                st.warning("⚠️ 这个方向需要较多准备，建议先学习相关技能。")

def show_action_plan():
    st.markdown('<h2 class="sub-header">📋 个性化行动计划</h2>', unsafe_allow_html=True)
    
    if "user_profile" not in st.session_state or not st.session_state.user_profile:
        st.warning("⚠️ 请先完成个人评估以获得个性化行动计划")
        return
    
    user_profile = st.session_state.user_profile
    
    # 获取最佳推荐
    recommendations = []
    for niche_name, niche_info in AI_NICHES.items():
        score = calculate_compatibility_score(user_profile, niche_info)
        recommendations.append((niche_name, niche_info, score))
    
    recommendations.sort(key=lambda x: x[2], reverse=True)
    best_niche_name, best_niche_info, best_score = recommendations[0]
    
    st.markdown(f"### 🎯 基于你的评估，推荐方向：{best_niche_name}")
    st.markdown(f"**匹配度：{best_score}%**")
    
    # 30天行动计划
    st.markdown("### 📅 30天启动行动计划")
    
    # 第一周：学习准备
    with st.expander("📚 第1周：学习准备", expanded=True):
        st.markdown("**目标：** 掌握基础知识和技能")
        st.markdown("**具体任务：**")
        
        for i, resource in enumerate(best_niche_info["学习资源"], 1):
            st.markdown(f"{i}. 学习{resource}")
        
        st.markdown("**每日时间安排：**")
        st.markdown("- 工作日：1-2小时学习")
        st.markdown("- 周末：3-4小时实践")
        
        # 进度追踪
        week1_progress = st.slider("第1周完成度", 0, 100, 0, key="week1")
        if week1_progress >= 80:
            st.success("🎉 第1周目标完成！")
    
    # 第二周：工具熟悉
    with st.expander("🛠️ 第2周：工具熟悉"):
        st.markdown("**目标：** 熟悉相关工具和平台")
        st.markdown("**具体任务：**")
        
        for i, tool in enumerate(best_niche_info["工具推荐"], 1):
            st.markdown(f"{i}. 注册并试用{tool}")
        
        st.markdown("**每日时间安排：**")
        st.markdown("- 工作日：1小时工具学习")
        st.markdown("- 周末：2-3小时深度体验")
        
        week2_progress = st.slider("第2周完成度", 0, 100, 0, key="week2")
        if week2_progress >= 80:
            st.success("🎉 第2周目标完成！")
    
    # 第三周：项目实践
    with st.expander("🚀 第3周：项目实践"):
        st.markdown("**目标：** 完成第一个小项目")
        st.markdown("**具体任务：**")
        
        for i, step in enumerate(best_niche_info["启动步骤"], 1):
            st.markdown(f"{i}. {step}")
        
        st.markdown("**每日时间安排：**")
        st.markdown("- 工作日：2小时项目开发")
        st.markdown("- 周末：4-5小时集中攻关")
        
        week3_progress = st.slider("第3周完成度", 0, 100, 0, key="week3")
        if week3_progress >= 80:
            st.success("🎉 第3周目标完成！")
    
    # 第四周：市场验证
    with st.expander("📊 第4周：市场验证"):
        st.markdown("**目标：** 验证市场需求，获得反馈")
        st.markdown("**具体任务：**")
        st.markdown("1. 发布作品到相关平台")
        st.markdown("2. 收集用户反馈")
        st.markdown("3. 优化产品/服务")
        st.markdown("4. 制定下一步计划")
        
        st.markdown("**每日时间安排：**")
        st.markdown("- 工作日：1小时反馈收集")
        st.markdown("- 周末：3小时优化改进")
        
        week4_progress = st.slider("第4周完成度", 0, 100, 0, key="week4")
        if week4_progress >= 80:
            st.success("🎉 第4周目标完成！")
    
    # 总体进度
    total_progress = (week1_progress + week2_progress + week3_progress + week4_progress) / 4
    st.markdown(f"### 📈 总体进度：{total_progress:.1f}%")
    
    if total_progress >= 80:
        st.success("🎉 恭喜！你已经完成了启动计划，可以开始正式运营你的AI副业了！")
    elif total_progress >= 60:
        st.info("👍 进度不错，继续加油！")
    else:
        st.warning("⚠️ 需要加快进度，建议增加学习时间。")

def show_learning_resources():
    st.markdown('<h2 class="sub-header">📚 学习资源推荐</h2>', unsafe_allow_html=True)
    
    # 通用AI学习资源
    st.markdown("### 🤖 通用AI学习资源")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h4>📖 入门书籍</h4>
            <ul>
                <li>《人工智能：一种现代方法》</li>
                <li>《深度学习》- Ian Goodfellow</li>
                <li>《Python机器学习》</li>
                <li>《AI商业应用指南》</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h4>🎥 在线课程</h4>
            <ul>
                <li>吴恩达机器学习课程</li>
                <li>CS50 AI课程</li>
                <li>Fast.ai深度学习</li>
                <li>李宏毅机器学习</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h4>🌐 学习平台</h4>
            <ul>
                <li>Coursera - 机器学习专项课程</li>
                <li>edX - AI和机器学习</li>
                <li>Udacity - AI纳米学位</li>
                <li>B站 - AI相关教程</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h4>🔧 实践工具</h4>
            <ul>
                <li>Google Colab - 免费GPU</li>
                <li>Kaggle - 数据科学竞赛</li>
                <li>Hugging Face - 模型库</li>
                <li>GitHub - 开源项目</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # 各利基市场专项资源
    st.markdown("### 🎯 专项学习资源")
    
    for niche_name, niche_info in AI_NICHES.items():
        with st.expander(f"📚 {niche_name}专项资源"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**推荐工具：**")
                for tool in niche_info["工具推荐"]:
                    st.markdown(f"- {tool}")
                
                st.markdown("**学习资源：**")
                for resource in niche_info["学习资源"]:
                    st.markdown(f"- {resource}")
            
            with col2:
                st.markdown("**启动步骤：**")
                for i, step in enumerate(niche_info["启动步骤"], 1):
                    st.markdown(f"{i}. {step}")
    
    # 社区和论坛
    st.markdown("### 👥 社区和论坛")
    st.markdown("""
    <div class="highlight">
        <h4>加入这些社区，与同行交流学习：</h4>
        <ul>
            <li><strong>知乎</strong> - AI相关话题讨论</li>
            <li><strong>CSDN</strong> - 技术博客和教程</li>
            <li><strong>掘金</strong> - 前端和AI开发</li>
            <li><strong>V2EX</strong> - 程序员社区</li>
            <li><strong>Reddit</strong> - r/MachineLearning</li>
            <li><strong>Discord</strong> - AI开发者社区</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 