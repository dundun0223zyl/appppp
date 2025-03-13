import os

# Install missing dependencies
os.system("pip install plotly")
import streamlit as st
import requests
import pandas as pd
import streamlit.components.v1 as components
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime, timedelta
from streamlit_lightweight_charts import renderLightweightCharts
import json
import plotly.io as pio


# Set API Base URL
API_BASE_URL = "http://127.0.0.1:8000"

# Force Wide Mode Layout
st.set_page_config(page_title="FinNews", layout="wide")

# Define the path to the local placeholder image
LOCAL_PLACEHOLDER_IMAGE = os.path.join(os.getcwd(), "1.jpg")  # Ensure this file exists

# Custom Styling for Newspaper Look
# Custom Styling for Newspaper Look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@400;700&family=Playfair+Display:wght@400;700&display=swap');

    /* Global Styles */
    html, body, [class*="st-"] {
        background-color: #F5EAD6 !important;  /* Old newspaper style */
        font-family: 'Libre Baskerville', serif !important;
        color: #3D2B1F !important; /* Dark Sepia */
    }

    /* Button Styling - Transparent with Softer Border */
    .stButton > button {
        background-color: transparent !important;  /* Fully Transparent */
        color: #3D2B1F !important; /* Dark Sepia */
        font-size: 18px !important;
        padding: 6px 14px !important;
        border-radius: 6px !important;
        border: 2px solid #C4A484 !important;  /* Softer Brown */
        width: auto !important;
        display: inline-block !important;
        text-align: center !important;
    }

    /* Remove background even when active */
    .stButton > button:active, .stButton > button:focus {
        background-color: transparent !important;
        color: #3D2B1F !important;
        border: 2px solid #C4A484 !important;  /* Softer Brown */
    }
    /* Fix for stRadio buttons */
    .stRadio > div {
        display: flex !important;  /* Align horizontally */
        justify-content: start !important;  /* Align to the left */
        gap: 15px !important;  /* Add spacing between buttons */
    }

    /* Fix radio button labels */
    .stRadio > div label {
        background-color: transparent !important; /* Remove any unwanted background */
        border: 1px solid #8B5E3B !important; /* Subtle border */
        padding: 6px 14px !important; /* Add padding */
        border-radius: 6px !important; /* Rounded corners */
        font-size: 16px !important;
        color: #3D2B1F !important; /* Sepia tone for consistency */
        font-weight: bold !important;
    }

    /* Make sure selected option is clear */
    .stRadio > div label[aria-checked="true"] {
        background-color: #D4B996 !important; /* Light beige when selected */
        color: #3D2B1F !important; /* Keep text readable */
    }

    /* Hover effect */
    .stRadio > div label:hover {
        background-color: #E7D3A8 !important; /* Subtle hover color */
        cursor: pointer !important;
    }
    /* Styling for Radio Button Group */
    .stRadio div[role="radiogroup"] {
        display: flex !important; /* Align horizontally */
        gap: 14px !important; /* Add spacing */
        justify-content: start !important; /* Align left */
    }

    /* Fix for Read More Button */
    .read-more-btn {
        background-color: #6B4226 !important;
        color: white !important;
        font-size: 16px !important;
        padding: 10px 15px !important;
        border-radius: 8px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-decoration: none !important;
        border: none !important;
        width: auto !important;
    }

    .read-more-btn:hover {
        background-color: #8B5E3B !important;
        color: white !important;
    }

     /* Sidebar Styles */
    .sidebar .sidebar-content {
        background-color: #F5EAD6 !important;  /* Matches main background */
        padding: 20px !important;
    }

    /* Remove border from "Go to:" */
    .stRadio > label {
        background-color: transparent !important;  /* No background */
        color: #3D2B1F !important;
        font-size: 16px !important;
        font-weight: bold;
        padding: 10px 14px !important;
        display: inline-block;
    }

    /* Sidebar Links Hover Effect */
    .stRadio > label:hover {
        background-color: transparent !important;
        color: white !important;
        border-color: #8B5E3B !important;
    }


    /* Ticker Dropdown Styling */
    .stSelectbox > div {
        background-color: #F0E0C1 !important;
        border: 2px solid #6B4226 !important;
        color: #3D2B1F !important;
        border-radius: 8px !important;
        padding: 8px !important;
    }

    /* Align search fields */
    .search-container {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 15px;
    }

    /* Section Headers */
    .header-card {
        background-color: #E7D3A8 !important;  /* Muted Beige */
        padding: 12px;
        border-radius: 8px;
        text-align: left;
        font-size: 22px;
        font-weight: bold;
        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
    }

    /* Metric Cards */
    .metric-card {
        background-color: #DFB98A !important;  /* Aged Paper */
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        color: #3D2B1F !important;
    }
    

    /* Market Cap Gauge Chart */
    .stPlotlyChart {
        background-color: #F5EAD6 !important;
        border-radius: 8px;
    }

    /* Description Box */
    .description-box {
        background-color: #F0E0C1 !important;
        padding: 15px;
        border-radius: 8px;
        font-size: 16px;
        text-align: justify;
        color: #3D2B1F !important;
    }

    /* Expander Styling */
    .stExpander {
        background-color: #E7D3A8 !important;
        border-radius: 8px;
        font-size: 16px;
    }

    /* Calendar Styling */
    .stDateInput {
        background-color: #F5EAD6 !important;  /* Light Beige Background */
        color: #E8D9C4 !important;  /* Dark Brown Text */
        border-radius: 8px !important;
        border: 1px solid #C8AB7F !important;  /* Soft Border */
        padding: 8px !important;
    }

    /* Improve Calendar Dropdown */
    .stDateInput .st-bc {
        background-color: #F5EAD6 !important;
        border-radius: 8px !important;
        box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.1) !important;
    }

    /* Selected Date */
    .stDateInput .st-bb {
    .stDateInput .st-bb span {
        background-color: #E8D9C4 !important;  /* Darker Brown for Selected */
        color: #E8D9C4 !important;  /* White Text */
        font-weight: bold !important;
        border-radius: 50% !important;  /* Circular Highlight */
    }

    /* Hover Effect on Dates */
    .stDateInput .st-ba:hover {
        background-color: #C8AB7F !important;
        color: #3D2B1F !important;
        border-radius: 50% !important;
    }

    /* Improve Month & Year Selection */
    .stDateInput .st-ae {
        background-color: #F5EAD6 !important;
        color: #3D2B1F !important;
        font-weight: bold !important;
        border-radius: 6px !important;
        padding: 4px 8px !important;
    }

    /* Arrows for Navigation */
    .stDateInput .st-ad {
        color: #755C3B !important;
        font-size: 18px !important;
    }
    
    .main .block-container {
        max-width: 95% !important;
        padding-left: 2rem;
        padding-right: 2rem;
        background-color: #F5E6CC !important;
    }
    .stTextInput > div > input {
        width: 100% !important;
        min-width: 350px !important;
        padding: 12px 16px !important;
        font-size: 18px !important;
        color: #3D2B1F !important;
        border: 2px solid #6B4226 !important;
        border-radius: 8px !important;
        background-color: #F0E0C1 !important;
        text-align: left !important;
    }
    
    </style>
""", unsafe_allow_html=True)





if 'articles' not in st.session_state:
    st.session_state['articles'] = []

if 'selected_analysis' not in st.session_state:
    st.session_state['selected_analysis'] = {}

if 'page' not in st.session_state:
    st.session_state['page'] = "About the Company"


# Define function to check image validity
def is_valid_image(urlToImage):
    """ Check if the image URL is accessible, return False if blocked. """
    try:
        response = requests.head(urlToImage, timeout=5)
        if response.status_code == 200:
            return True
    except:
        pass
    return False

# Sidebar Navigation

def streamlit_app():
    st.sidebar.markdown("<div class='sidebar-title'>📌 News & Markets Hub</div>", unsafe_allow_html=True)
    st.session_state.page = st.sidebar.radio("Go to:", ["🏢 About the Company", "📰 Search News", "🏛 News Analysis", "📈 Stock Data", "📉 Stock Prediction"])
    # st.session_state.page = page_choice
    # ---- PAGE 1: ABOUT THE COMPANY ----
    if st.session_state.page == "🏢 About the Company":
        # 🏢 Title
        st.markdown("<h1 class='stTitle'>Search for a Company</h1>", unsafe_allow_html=True)
        
        # 🔍 Search Section with Improved Layout
        search_method = st.radio(
            "🔍Search by:",
            ["Company Name", "Ticker"],
            horizontal=True
        )

        # Define `selected_ticker` initially to avoid "not defined" error
        selected_ticker = None
    
        # 📌 **Fetch available companies & tickers dynamically**
        company_list_response = requests.get(f"{API_BASE_URL}/companies")
        ticker_list_response = requests.get(f"{API_BASE_URL}/tickers")
    
        company_list = company_list_response.json().get("companies", []) if company_list_response.status_code == 200 else []
        ticker_list = ticker_list_response.json().get("tickers", []) if ticker_list_response.status_code == 200 else []
    
        # ✅ **User selects search method**
        if search_method == "Company Name":
            col1, col2 = st.columns([2, 2])
    
            with col1:
                company_name = st.text_input("✍ Enter Company Name")
                
            with col2:
                if company_name:
                    response = requests.get(f"{API_BASE_URL}/search/{company_name}")
                    if response.status_code == 200:
                        tickers = response.json().get("matching_tickers", [])
                        if tickers:
                            selected_ticker = st.selectbox("📌 Select a Ticker", tickers, key="ticker_select")
                        else:
                            st.warning("⚠ No matching ticker found.")
                    else:
                        st.error("❌ Failed to fetch tickers.")
    
        elif search_method == "Ticker":
            col1, col2 = st.columns([2, 2])
    
            with col1:
                selected_ticker = st.selectbox("📌 Select a Ticker", ticker_list) if ticker_list else None
            with col2:
                manual_ticker = st.text_input("✏ Enter Ticker (e.g., AAPL, TSLA, AMZN)").upper()
                if manual_ticker:
                    selected_ticker = manual_ticker  # Allow manual entry
    
        # 🏢 **Company Overview**
        if selected_ticker:
            st.markdown(f"<div class='header-card'>📊 {selected_ticker} Overview</div>", unsafe_allow_html=True)
    
            # Fetch company info from API
            company_info = requests.get(f"{API_BASE_URL}/company/{selected_ticker}")
            if company_info.status_code == 200:
                data = company_info.json()
    
                # ✅ **Basic Info Layout**
                col1, col2 = st.columns([2, 3])
    
                with col1:
                    st.markdown(f"**Industry**: {data.get('industry', 'N/A')}")
                    employees = data.get("employees", "N/A")
                    employees = f"{int(employees):,}" if isinstance(employees, (int, float, str)) and employees != "N/A" else "N/A"
                    st.markdown(f"**Employees**: {employees}")
                    website = data.get("website", "N/A")
                    st.markdown(f"**Website**: [{website}]({website})" if website != "N/A" else "**Website**: N/A")
    
                with col2:
                    short_desc = data['description'][:400] + "..." if len(data['description']) > 400 else data['description']
                    st.markdown(f"📜 **Description:** {short_desc}")
    
                    if len(data['description']) > 400:
                        with st.expander("📖 Read More"):
                            st.markdown(f"**📜 Full Description:** {data['description']}")
    
                # 📌 **Market Cap Gauge Chart**
                st.markdown("<div class='header-card'>🌍 Market Capitalization</div>", unsafe_allow_html=True)
    
                market_cap = float(data.get("market_cap", 0))
                max_cap = 3e12  # Adjust scale for large companies
    
                background_color = "#F5EAD6"  
                gauge_colors = ["#d9c2a3", "#c8ab7f", "#a88f5d", "#755c3b"]
    
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=market_cap,
                    title={"text": f"{data['company_name']} Market Cap", "font": {"color": "#3D2B1F"}},
                    gauge={
                        "axis": {"range": [0, max_cap], "tickcolor": "#3D2B1F"},
                        "bar": {"color": "#5a4632"},
                        "steps": [
                            {"range": [0, 2e9], "color": gauge_colors[0]},
                            {"range": [2e9, 1e10], "color": gauge_colors[1]},
                            {"range": [1e10, 2e11], "color": gauge_colors[2]},
                            {"range": [2e11, max_cap], "color": gauge_colors[3]}
                        ],
                        "bgcolor": background_color
                    }
                ))
    
                fig.update_layout(paper_bgcolor=background_color, font={"color": "#3D2B1F"})
                st.plotly_chart(fig)
    
                # 🔑 **Key Financial Metrics**
                st.markdown("### 🔑 Key Metrics")
    
                def format_large_number(value):
                    try:
                        value = float(value)
                        if value >= 1e9:
                            return f"${value / 1e9:.2f}B"
                        elif value >= 1e6:
                            return f"${value / 1e6:.2f}M"
                        return f"${value:,.2f}"
                    except:
                        return "N/A"
    
                def format_percentage(value):
                    try:
                        return f"{float(value) * 100:.2f}%"
                    except:
                        return "N/A"
    
                # ✅ Styled Metric Cards
                col1, col2, col3 = st.columns(3)
    
                with col1:
                    st.metric(label="💰 Revenue", value=format_large_number(data['key_metrics'].get('revenue', 0)))
                    st.metric(label="📈 Net Income", value=format_large_number(data['key_metrics'].get('net_income', 0)))
    
                with col2:
                    st.metric(label="📊 Gross Margin", value=format_percentage(data['key_metrics'].get('gross_margin', 0)))
                    st.metric(label="⚖ Debt-to-Equity", value=f"{data['key_metrics'].get('debt_to_equity', 'N/A')}")
    
                with col3:
                    st.metric(label="🏆 Return on Equity", value=format_percentage(data['key_metrics'].get('return_on_equity', 0)))
                    st.metric(label="📉 EPS", value=f"{data['key_metrics'].get('eps', 'N/A')}")
    
            else:
                st.error("⚠️ Could not retrieve company details.")
    
    # ---- PAGE 2: SEARCH NEWS ----
    elif st.session_state.page == "📰 Search News":
        st.markdown("<h1 class='title'>Financial News</h1>", unsafe_allow_html=True)
        
        # Search Filters
        col1, col2, col3, col4 = st.columns(4)
        with col1: company_name = st.text_input("🔎 Company")
        with col2: from_date = st.date_input("📅 From Date", datetime.today())
        with col3: to_date = st.date_input("📅 To Date", datetime.today())
        with col4: sort_by = st.selectbox("📊 Sort By", ["publishedAt", "relevancy", "popularity"])
        language = st.selectbox("🌍 Language", ["ar", "de", "en", "es", "fr", "he", "it", "nl", "no", "pt", "ru", "sv", "ud", "zh"], index=2)
        fetch_news_btn = st.markdown(
            "<style>.fetch-btn button {background-color: #6B4226 !important; color: white !important; font-size: 18px !important; padding: 12px 24px !important; border-radius: 8px !important; border: none !important; width: auto !important; display: flex !important; align-items: center !important; justify-content: center !important;}</style>",
            unsafe_allow_html=True
        )
    

        fetch_news_button = st.button("🔍 Fetch News", help="Click to fetch news")
        if fetch_news_button:
            news_url = f"{API_BASE_URL}/news/?query={company_name}&from_date={from_date}&to_date={to_date}&sort_by={sort_by}&language={language}"
            news_response = requests.get(news_url)
            
            if news_response.status_code == 200:
                st.session_state.articles = news_response.json().get("articles", [])
                if not st.session_state.articles:
                    st.warning("⚠️ No news articles found.")
        if st.session_state.articles:
            for idx, article in enumerate(st.session_state.articles):
                col1, col2 = st.columns([1, 3])
                with col1:
                    image_url = article.get("urlToImage", None)
                    if image_url and is_valid_image(image_url):
                        st.image(image_url, use_container_width=True)
                    else:
                        st.image(LOCAL_PLACEHOLDER_IMAGE, use_container_width=True)
                
                with col2:
                    st.markdown(f"### {article['title']}")
                    st.markdown(f"**🗓️ Published:** {article.get('publishedAt', 'N/A')}")
                    with st.expander("📰 Show Description"):
                        st.write(article.get("description", "No description available."))
                    st.markdown(f"[🔗 Read Full Article]({article['url']})", unsafe_allow_html=True)
                    analyze_button = st.button(f"📊 Analyze - {article['title']}", key=f"analyze_{idx}")
                    # Button to Analyze News
                    if analyze_button:
                        st.session_state.selected_analysis = {
                            "title": article["title"],
                            "description": article["description"],
                            "url": article["url"],
                            "content": article.get("content", "Content not available")
                        }
                        # st.session_state.analysis_type = None  # Reset analysis choice
                        st.session_state.page = "News Analysis"
                    #     print("✅ Session State after button click:", st.session_state)
                        # st.experimental_rerun()  # Ensure Streamlit refreshes with new state

                        
    # ---- PAGE 3: ANALYSIS RESULTS ----
    elif st.session_state.page == "🏛 News Analysis":
        if st.session_state.selected_analysis:
            article = st.session_state.selected_analysis

            # 🎯 News Analysis Title
            with st.container():
                st.markdown(
                    f"""
                    <div style="
                        background-color: #F5EAD6;
                        padding: 20px;
                        border-radius: 12px;
                        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
                        margin-bottom: 20px;
                        text-align: left;">
                        <h1 style="font-size: 28px; font-weight: 700; color: #3D2B1F; margin-bottom: 5px;">
                            📚 News Analysis for:
                        </h1>
                        <h2 style="font-size: 24px; font-weight: 600; color: #755C3B; margin-bottom: 10px;">
                            {article['title']}
                        </h2>
                        <hr style="border: none; height: 2px; background-color: #C8AB7F; width: 60%; margin: auto;">
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
            
            # 🔗 Full Article Link
            st.markdown(f"[🔗 Read Full Article]({article['url']})", unsafe_allow_html=True)

            # 📝 Article Preview Card
            with st.container():
                st.markdown(
                    """
                    <div style="
                        background-color: #F5EAD6; 
                        padding: 15px; 
                        border-radius: 12px; 
                        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                        margin-bottom: 15px;">
                        <h3>📝 Article Preview</h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.write(article["description"])

            # 🎛 Choose Analysis Type
            analysis_type = st.radio("Choose Analysis Type:", ["Summary", "Sentiment"], horizontal=True, key="analysis_choice")

            if st.button("🔍 Run Analysis"):
                st.session_state.analysis_type = analysis_type.lower()

                # ✅ Send API Request for Analysis
                analysis_url = (
                    f"{API_BASE_URL}/analyze/?"
                    f"title={article['title']}&description={article['description']}"
                    f"&url={article['url']}&content={article['content']}"
                    f"&action={st.session_state.analysis_type}"
                )

                response = requests.get(analysis_url)

                if response.status_code == 200:
                    result = response.json()
                    analysis_result = result["analysis_result"]

                    # 📌 **Display Each Section in a Card**
                    with st.container():
                        st.markdown(
                            f"""
                            <div style="
                                background-color: #F5EAD6; 
                                padding: 15px; 
                                border-radius: 12px; 
                                box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                                margin-bottom: 15px;">
                                <h3>📊 {analysis_type} Result</h3>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

        
                        if len(analysis_result) > 500:
                            with st.expander("📖 Show Full Analysis"):
                                st.write(analysis_result)
                        else:
                            st.write(analysis_result)

                else:
                    st.error("❌ Failed to analyze news.")

        else:
            st.warning("⚠️ No article selected. Please go to 'Search News' and choose an article.")

        

    # ---- PAGE 4: Stock Data Dashboard ----
    # Ensure session state for navigation
    elif st.session_state.page == "📈 Stock Data":
        st.header("Stock Market Dashboard")
    
        # Search Section with Improved Layout
        st.markdown("### 🔍 Search for a Company")
        search_method = st.radio("Search by:", ["Company Name", "Ticker"], horizontal=True)

        # Fetch tickers dynamically
        company_list_response = requests.get(f"{API_BASE_URL}/companies")
        ticker_list_response = requests.get(f"{API_BASE_URL}/tickers")
        company_list = company_list_response.json().get("companies", []) if          company_list_response.status_code == 200 else []
        ticker_list = ticker_list_response.json().get("tickers", []) if ticker_list_response.status_code == 200 else []

        selected_ticker = None

        if search_method == "Company Name":
            col1, col2 = st.columns([2, 2])
            with col1:
                company_name = st.text_input("📝 Enter Company Name")
            with col2:
                if company_name:
                    response = requests.get(f"{API_BASE_URL}/search/{company_name}")
                    if response.status_code == 200:
                        tickers = response.json().get("matching_tickers", [])
                        if tickers:
                            selected_ticker = st.selectbox("📌 Select a Ticker", tickers, key="ticker_select")
                        else:
                            st.warning("⚠ No matching ticker found.")
                    else:
                        st.error("❌ Failed to fetch tickers.")
        elif search_method == "Ticker":
            col1, col2 = st.columns([2, 2])
            with col1:
                selected_ticker = st.selectbox("📌 Select a Ticker", ticker_list) if ticker_list else None
            with col2:
                manual_ticker = st.text_input("📝 Enter Ticker (e.g., AAPL, TSLA, AMZN)").upper()
                if manual_ticker:
                    selected_ticker = manual_ticker

        # Timeframe Selection
        timeframe_options = ["1W", "1M", "6M", "1Y", "5Y", "Custom"]
        timeframe = st.selectbox("⏳ Select Timeframe", timeframe_options, index=3)

        if timeframe == "Custom":
            start_date = st.date_input("📅 Start Date", datetime.today() - timedelta(days=365))
            end_date = st.date_input("📅 End Date", datetime.today())
        else:
            period_mapping = {"1W": "7d", "1M": "1mo", "6M": "6mo", "1Y": "1y", "5Y": "5y"}
            selected_period = period_mapping[timeframe]
        if selected_ticker:
            stock = yf.Ticker(selected_ticker)
            if timeframe == "Custom":
                data = stock.history(start=start_date, end=end_date)
            else:
                data = stock.history(period=selected_period)

            sp500 = yf.Ticker("^GSPC")
            if timeframe == "Custom":
                sp500_data = sp500.history(start=start_date, end=end_date)
            else:
                sp500_data = sp500.history(period=selected_period)

            # Compute SMA and EMA
            data["SMA_50"] = data["Close"].rolling(window=50).mean()
            data["EMA_50"] = data["Close"].ewm(span=50, adjust=False).mean()

            # Prepare data for Lightweight Chart
            price_volume_chart = [
                {
                    "type": "Candlestick",
                    "data": [{"time": str(index.date()), "open": row.Open, "high": row.High, "low": row.Low, "close": row.Close}
                            for index, row in data.iterrows()],
                    "options": {
                        "upColor": "#2E8B57", "downColor": "#B22222",
                        "borderUpColor": "#2E8B57", "borderDownColor": "#B22222"
                    }
                },
                {
                    "type": "Line",
                    "data": [{"time": str(index.date()), "value": row.SMA_50} for index, row in data.iterrows() if not pd.isna(row.SMA_50)],
                    "options": {"color": "#FFD700", "lineWidth": 2, "title": "SMA 50"}
                },
                {
                    "type": "Line",
                    "data": [{"time": str(index.date()), "value": row.EMA_50} for index, row in data.iterrows() if not pd.isna(row.EMA_50)],
                    "options": {"color": "#4682B4", "lineWidth": 2, "title": "EMA 50"}
                },
                {
                    "type": "Histogram",
                    "data": [{"time": str(index.date()), "value": row.Volume} for index, row in data.iterrows()],
                    "options": {
                        "color": "rgba(38,198,218,0.6)",
                        "priceFormat": {"type": "volume"},
                        "priceScaleId": "", 
                        "title": "Trading Volume"
                    }
                }
            ]

            
            st.subheader(f"📊 {selected_ticker} Price & Volume Chart")
            renderLightweightCharts([{"chart": {
                "height": 600,
                "layout": {
                    "background": {"type": "solid", "color": "#F5E6CC"},
                    "textColor": "#3D2B1F"
                },
                "grid": {
                    "vertLines": {"color": "rgba(42, 46, 57, 0.2)"},
                    "horzLines": {"color": "rgba(42, 46, 57, 0.2)"}
                }
            }, 
            "series": price_volume_chart
        }], "priceAndVolume")


            # Stock vs S&P 500 Performance
            data["Stock Change (%)"] = (data["Close"] / data["Close"].iloc[0] - 1) * 100
            sp500_data["S&P 500 Change (%)"] = (sp500_data["Close"] / sp500_data["Close"].iloc[0] - 1) * 100

            comparison_chart = [
                {"type": "Line", "data": [{"time": str(index.date()), "value": row} for index, row in data["Stock Change (%)"].items()],
                 "options": {"color": "#FFD700", "lineWidth": 2, "title": f"{selected_ticker.upper()} Change (%)"}},
                {"type": "Line", "data": [{"time": str(index.date()), "value": row} for index, row in sp500_data["S&P 500 Change (%)"].items()],
                 "options": {"color": "#26a69a", "lineWidth": 2, "title": "S&P 500 Change (%)"}}
            ]

            st.subheader("📊 Stock vs S&P 500 Performance")
            renderLightweightCharts([{
                "chart": {
                    "height": 600,
                    "layout": {
                        "background": {"type": "solid", "color": "#F5E6CC"},
                        "textColor": "#3D2B1F"
                    },
                    "grid": {
                        "vertLines": {"color": "rgba(42, 46, 57, 0.2)"},
                        "horzLines": {"color": "rgba(42, 46, 57, 0.2)"}
                    }
                }, 
                "series": comparison_chart
            }], "sp500Comparison")

    # ---- PAGE 5: Stock Data Prediction ----
    # Ensure session state for navigation
    elif st.session_state.page == "📉 Stock Prediction":
        st.header("Stock Price Prediction")

        # Fetch tickers dynamically from API
        #response = requests.get(f"{API_BASE_URL}/tickers")
        #ticker_list = response.json().get("tickers", []) if response.status_code == 200 else []

        # User Input: Select Stock Ticker
        col1, col2 = st.columns([2, 2])
        with col1:
            #selected_ticker = st.selectbox("🔍 Select a Ticker", ticker_list, key="prediction_ticker")
            selected_ticker = st.text_input("🔍 Enter a Ticker", "").strip().upper()
    
        # User Input: Select Forecast Period (Max 30 Days)
        with col2:
            days_ahead = st.slider("⏳ Select Forecast Days", min_value=1, max_value=30, value=7)
    
        # Fetch Predictions when user clicks button
        if st.button("🔮 Get Prediction"):
            if selected_ticker:
                pred_response = requests.get(f"{API_BASE_URL}/predict/{selected_ticker}?days_ahead={days_ahead}")
                hist_response = requests.get(f"{API_BASE_URL}/stock/{selected_ticker}")
                if pred_response.status_code == 200 and hist_response.status_code == 200:
                    pred_data = pred_response.json()
                    hist_prices = hist_response.json().get("historical_prices", [])

                    # Ensure we have valid data
                    if not hist_prices or "predictions" not in pred_data:
                        st.error("❌ Data retrieval issue. Please try another stock.")
                        st.stop()
                
                    # Fetch Historical Data for Last Month for Comparison
                    end_date = datetime.today()
                    start_date = end_date - timedelta(days=90)
                    historical_chart = [
                        {"time": entry["date"], "value": entry["close"]}
                        for entry in hist_prices if datetime.strptime(entry["date"], "%Y-%m-%d") >= start_date
                    ]

                    # Prepare prediction data (start after last historical date)
                    future_chart = [
                        {"time": (end_date + timedelta(days=i)).strftime("%Y-%m-%d"), "value": pred}
                        for i, pred in enumerate(pred_data["predictions"])
                    ]

                    
                    # Combine data into chart series
                    chart_series = [
                        {"type": "Line", "data": historical_chart, "options": {"color": "#4682B4", "lineWidth": 3}},  # Blue: Historical
                        {"type": "Line", "data": future_chart, "options": {"color": "#FFA500", "lineWidth": 4, "lineStyle": 1}},  # Orange: Prediction
                    ]
                    # Render the chart
                    st.subheader(f"📉 {selected_ticker.upper()} Stock Price Forecast")
                    renderLightweightCharts([{
                    "chart": {
                        "height": 600,
                        "layout": {
                            "background": {"type": "solid", "color": "#F5E6CC"},
                            "textColor": "#3D2B1F"
                        },
                        "grid": {
                            "vertLines": {"color": "rgba(42, 46, 57, 0.2)"},
                            "horzLines": {"color": "rgba(42, 46, 57, 0.2)"}
                        }
                    },
                    "series": chart_series
                }], "predictionChart")
            else:
                st.error("❌ Failed to fetch predictions or historical data.")
        else:
            st.warning("⚠ Please enter a valid ticker before proceeding.")

if __name__ == "__main__":
    st.write("Run the app using: `streamlit run app.py`")
    streamlit_app()