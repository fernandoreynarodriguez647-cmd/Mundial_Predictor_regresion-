CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main > div {
        background-color: #E0F7F5;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: #1B2A4A;
    }

    .stApp {
        background-color: #E0F7F5;
    }

    p, li, .stMarkdown, .stText {
        color: #1B2A4A;
    }

    section[data-testid="stSidebar"] {
        background-color: #1B2A4A;
        background-image: linear-gradient(180deg, #1B2A4A 0%, #243B5E 100%);
    }

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: #FFFFFF !important;
        font-weight: 400;
    }

    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label {
        color: #B0C4DE !important;
        font-size: 0.85rem;
    }

    div[data-testid="stSidebarNav"] ul li a {
        color: #B0C4DE !important;
        font-weight: 400;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        transition: all 0.2s ease;
    }

    div[data-testid="stSidebarNav"] ul li a:hover {
        background-color: rgba(255,255,255,0.12);
        color: #FFFFFF !important;
    }

    div[data-testid="stSidebarNav"] ul li a.active {
        background-color: rgba(255,255,255,0.18);
        color: #FFFFFF !important;
        font-weight: 600;
    }

    .card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1.5px solid #CBD5E1;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
        transition: box-shadow 0.2s ease;
    }

    .card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.06);
    }

    .card h3 {
        margin-top: 0;
        font-size: 1.1rem;
        color: #1B2A4A;
    }

    .card p {
        color: #1B2A4A !important;
        font-size: 0.9rem;
        line-height: 1.6;
    }

    .metric-card {
        background: #FFFFFF;
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
        border: 1.5px solid #CBD5E1;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }

    .metric-card .label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #1B2A4A;
        margin-bottom: 0.3rem;
        font-weight: 600;
    }

    .metric-card .value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1B2A4A;
        line-height: 1.2;
    }

    .metric-card .value.accent {
        color: #00A896;
    }

    .metric-card .value.warning {
        color: #E67E22;
    }

    .header-section {
        background: linear-gradient(135deg, #1B2A4A 0%, #2C5F8A 100%);
        border-radius: 14px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        color: white;
    }

    .header-section h1 {
        color: white !important;
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
    }

    .header-section p {
        color: rgba(255,255,255,0.85) !important;
        margin: 0.3rem 0 0 0;
        font-size: 0.95rem;
    }

    .stMetric {
        background: #FFFFFF;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        border: 1.5px solid #CBD5E1;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }

    .stMetric label {
        color: #1B2A4A !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 600 !important;
    }

    .stMetric div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #1B2A4A !important;
    }

    div.stDataFrame {
        border: 1.5px solid #CBD5E1;
        border-radius: 10px;
        overflow: hidden;
    }

    div.stDataFrame table {
        border-collapse: collapse;
    }

    div.stDataFrame th {
        background-color: #F0F4F8 !important;
        color: #1B2A4A !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        border-bottom: 2px solid #CBD5E1 !important;
        padding: 0.6rem 0.8rem !important;
    }

    div.stDataFrame td {
        border-bottom: 1px solid #E2E8F0 !important;
        padding: 0.5rem 0.8rem !important;
        color: #1B2A4A !important;
    }

    div.stDataFrame tr:hover td {
        background-color: #F8FAFC !important;
    }

    .stAlert {
        border-radius: 10px;
        border: 1px solid;
    }

    .stAlert.stInfo {
        background-color: #EBF5FB;
        border-color: #B8D4E8;
        color: #1A5276;
    }

    .stAlert.stSuccess {
        background-color: #E8F8F5;
        border-color: #A8E6CF;
        color: #0E6655;
    }

    .stAlert.stWarning {
        background-color: #FEF5E7;
        border-color: #F0D5A8;
        color: #935116;
    }

    .stAlert.stError {
        background-color: #FDEDEC;
        border-color: #F5B7B1;
        color: #922B21;
    }

    hr {
        margin: 1.5rem 0;
        border: 0;
        height: 2px;
        background: #CBD5E1;
        border-radius: 2px;
    }

    div.st-bd {
        border-color: #CBD5E1 !important;
    }

    .stSelectbox div[data-baseweb="select"] > div {
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }

    .stMultiSelect div[data-baseweb="select"] > div {
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }

    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
        background-color: rgba(255,255,255,0.1) !important;
        border: 1.5px solid rgba(255,255,255,0.2) !important;
        color: white !important;
    }

    section[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] > div {
        background-color: rgba(255,255,255,0.1) !important;
        border: 1.5px solid rgba(255,255,255,0.2) !important;
        color: white !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }

    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        border-bottom: none !important;
    }
</style>
"""
