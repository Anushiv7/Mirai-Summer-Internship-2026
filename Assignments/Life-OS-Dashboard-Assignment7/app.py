import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from google import genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="Life-OS Dashboard", layout="wide", initial_sidebar_state="expanded")

# ==================== PHASE 1: DATA PIPELINE ====================

def generate_screentime_csv():
    """Generate 14 days of realistic screen time data if CSV doesn't exist"""
    if not os.path.exists("screentime.csv"):
        dates = [datetime.now() - timedelta(days=i) for i in range(13, -1, -1)]
        data = []
        
        apps = {
            "Social Media": ["TikTok", "Instagram", "Twitter"],
            "Coding": ["VS Code", "GitHub", "Cursor"],
            "Entertainment": ["YouTube", "Netflix", "Discord"],
            "Education": ["Kaggle", "CS50", "Coursera"],
            "Productivity": ["Notion", "Todoist", "Obsidian"]
        }
        
        for date in dates:
            for category, app_list in apps.items():
                for app in app_list:
                    minutes = np.random.randint(15, 180)
                    data.append({
                        "Date": date.strftime("%Y-%m-%d"),
                        "App_Name": app,
                        "Category": category,
                        "Minutes_Used": minutes
                    })
        
        df = pd.DataFrame(data)
        df.to_csv("screentime.csv", index=False)
        return df
    
    return pd.read_csv("screentime.csv")

# Load data
df = generate_screentime_csv()
df["Date"] = pd.to_datetime(df["Date"])

# ==================== PHASE 2: DASHBOARD UI ====================

st.title("📱 Life-OS: Your Digital Wellness Command Center")
st.markdown("*Take control of your screen time before it controls you.*")

# Sidebar Controls
with st.sidebar:
    st.header("⚙️ Command Controls")
    
    selected_date = st.selectbox(
        "📅 Select Date",
        sorted(df["Date"].unique(), reverse=True),
        format_func=lambda x: x.strftime("%Y-%m-%d")
    )
    
    daily_goal = st.slider(
        "🎯 Daily Screen Goal (minutes)",
        min_value=60,
        max_value=480,
        value=180,
        step=15
    )

# Filter data for selected date
today_data = df[df["Date"] == selected_date]
today_total_minutes = today_data["Minutes_Used"].sum()
today_total_hours = round(today_total_minutes / 60, 1)

# Most used app
most_used_app = today_data.loc[today_data["Minutes_Used"].idxmax(), "App_Name"]
most_used_time = today_data["Minutes_Used"].max()

# Delta calculation
delta = today_total_minutes - daily_goal
delta_color = "inverse"

# KPI Row
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "⏱️ Screen Time Today",
        f"{today_total_hours}h",
        f"{delta} min vs goal",
        delta_color=delta_color
    )

with col2:
    st.metric(
        "📲 Most Used App",
        most_used_app,
        f"{most_used_time} min"
    )

with col3:
    if delta <= 0:
        status = "✅ On Track!"
    elif delta <= 30:
        status = "⚠️ Slightly Over"
    else:
        status = "🔴 Way Over"
    st.metric("Status", status)

st.divider()

# Visualizations
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 14-Day Trend")
    daily_totals = df.groupby("Date")["Minutes_Used"].sum().reset_index()
    st.line_chart(data=daily_totals.set_index("Date"), height=300)

with col2:
    st.subheader("📈 Today's Breakdown by Category")
    category_breakdown = today_data.groupby("Category")["Minutes_Used"].sum()
    st.bar_chart(category_breakdown)

st.divider()

# ==================== PHASE 3: AI INTEGRATION ====================

st.subheader("🤖 Your AI Life Coach Analysis")

# Convert data to string for Gemini
data_summary = today_data.groupby("Category")["Minutes_Used"].sum().to_string()

system_prompt = f"""You are a brutally honest but supportive digital wellness coach. 
A user just shared their screen time data for today. Analyze it like a coach analyzing athlete performance.

TODAY'S SCREEN TIME BY CATEGORY:
{data_summary}

INSTRUCTIONS:
1. Be specific. Don't say "use your phone less" — that's useless.
2. For each category with excessive time, suggest a REAL-WORLD alternative activity.
3. If they spent 2 hours on TikTok, suggest: "Go for a 45-min run, meal prep for tomorrow, or read a book."
4. Keep it under 200 words.
5. Use encouraging but honest tone.
6. End with ONE actionable habit they can start TODAY."""

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=system_prompt
    )
    coaching_text = response.text
    
    # Display based on severity
    if today_total_minutes > daily_goal + 60:
        st.warning(f"🔴 **Critical Analysis**\n\n{coaching_text}")
    elif today_total_minutes > daily_goal:
        st.info(f"⚠️ **Coach's Insight**\n\n{coaching_text}")
    else:
        st.success(f"✅ **Coach's Feedback**\n\n{coaching_text}")
        
except Exception as e:
    st.error(f"⚠️ AI Coach unavailable: {str(e)}")

st.divider()

# ==================== PHASE 4: INNOVATION - SHAREABLE LINK ====================

st.subheader("🔗 Accountability Partner Share")

# Encode today's data in URL
accountability_url = f"?date={selected_date.strftime('%Y-%m-%d')}&screen_time={today_total_minutes}&goal={daily_goal}"
share_link = f"https://your-app-name.streamlit.app{accountability_url}"

st.markdown("**Share your screen time with an accountability partner:**")
st.code(share_link, language="text")
st.markdown("They can click this link to see your stats for today. Use it to stay honest.")

# Read query params if shared
query_params = st.query_params
if "screen_time" in query_params:
    shared_time = int(query_params["screen_time"][0])
    shared_goal = int(query_params["goal"][0])
    shared_date = query_params.get("date", ["Unknown"])[0]
    
    st.info(f"""
    📊 **Accountability Check-in**
    
    Your friend used **{shared_time} minutes** on {shared_date}
    Their goal was **{shared_goal} minutes**
    
    Delta: **{shared_time - shared_goal:+d} minutes**
    """)