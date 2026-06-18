import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Restaurant Analytics Dashboard",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .main { background-color: #0e0e16; }
    .block-container { padding: 1.5rem 2rem 3rem; max-width: 1400px; }

    /* Header */
    .dash-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border: 1px solid rgba(99,102,241,0.3);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    .dash-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
        border-radius: 50%;
    }
    .dash-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1, #a855f7, #22d3ee);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .dash-subtitle {
        color: #9495a7;
        font-size: 0.95rem;
        margin-top: 0.3rem;
    }

    /* KPI Cards */
    .kpi-container {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
        flex-wrap: wrap;
    }
    .kpi-card {
        flex: 1;
        min-width: 150px;
        background: #16161f;
        border: 1px solid rgba(148,149,167,0.12);
        border-radius: 14px;
        padding: 1.25rem 1.5rem;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    .kpi-card:hover { border-color: rgba(99,102,241,0.4); transform: translateY(-2px); }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        border-radius: 14px 14px 0 0;
    }
    .kpi-1::before { background: linear-gradient(90deg, #6366f1, #a855f7); }
    .kpi-2::before { background: linear-gradient(90deg, #f43f5e, #fb923c); }
    .kpi-3::before { background: linear-gradient(90deg, #22d3ee, #3b82f6); }
    .kpi-4::before { background: linear-gradient(90deg, #34d399, #059669); }
    .kpi-5::before { background: linear-gradient(90deg, #fbbf24, #f97316); }
    .kpi-6::before { background: linear-gradient(90deg, #a855f7, #d946ef); }
    .kpi-icon { font-size: 1.4rem; margin-bottom: 0.5rem; }
    .kpi-value { font-size: 1.7rem; font-weight: 800; color: #f0f0f5; letter-spacing: -0.03em; }
    .kpi-label { font-size: 0.75rem; color: #9495a7; font-weight: 500; margin-top: 0.2rem; }
    .kpi-sub { font-size: 0.68rem; color: #5e5f72; margin-top: 0.4rem; }

    /* Section Headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 2rem 0 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid rgba(148,149,167,0.1);
    }
    .section-icon {
        width: 38px; height: 38px;
        background: rgba(99,102,241,0.1);
        border: 1px solid rgba(99,102,241,0.2);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
    }
    .section-title { font-size: 1.1rem; font-weight: 700; color: #f0f0f5; }
    .section-sub { font-size: 0.78rem; color: #9495a7; }

    /* Insight Cards */
    .insight-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin-bottom: 1rem;
    }
    .insight-card {
        background: #16161f;
        border: 1px solid rgba(148,149,167,0.1);
        border-radius: 14px;
        padding: 1.25rem;
    }
    .insight-card:hover { border-color: rgba(99,102,241,0.3); }
    .insight-emoji { font-size: 1.2rem; margin-bottom: 0.5rem; }
    .insight-title { font-size: 0.9rem; font-weight: 600; color: #f0f0f5; margin-bottom: 0.4rem; }
    .insight-text { font-size: 0.8rem; color: #9495a7; line-height: 1.6; }
    .highlight { color: #22d3ee; font-weight: 600; }

    /* Top 3 Cards */
    .top3-card {
        border-radius: 16px;
        padding: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    .top3-gold { background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(168,85,247,0.08)); border: 1px solid rgba(99,102,241,0.4); }
    .top3-silver { background: linear-gradient(135deg, rgba(244,63,94,0.1), rgba(251,146,60,0.06)); border: 1px solid rgba(244,63,94,0.3); }
    .top3-bronze { background: linear-gradient(135deg, rgba(251,191,36,0.1), rgba(249,115,22,0.06)); border: 1px solid rgba(251,191,36,0.3); }

    /* Divider */
    hr { border-color: rgba(148,149,167,0.1); margin: 1.5rem 0; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #111118;
        border-right: 1px solid rgba(148,149,167,0.1);
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiselect label { color: #9495a7 !important; }

    /* Plotly charts background */
    .js-plotly-plot { border-radius: 12px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Country Map ───────────────────────────────────────────────
COUNTRY_MAP = {
    1: 'India', 14: 'Australia', 30: 'Brazil', 37: 'Canada',
    94: 'Indonesia', 148: 'New Zealand', 162: 'Philippines',
    166: 'Qatar', 184: 'Singapore', 189: 'South Africa',
    191: 'Sri Lanka', 208: 'Turkey', 214: 'UAE',
    215: 'United Kingdom', 216: 'United States'
}

# ── Plotly Theme ─────────────────────────────────────────────
PLOTLY_THEME = {
    'paper_bgcolor': '#16161f',
    'plot_bgcolor': '#16161f',
    'font': {'color': '#9495a7', 'family': 'Inter'},
    'title': {'font': {'color': '#f0f0f5', 'size': 14, 'family': 'Inter'}},
}
COLORS = px.colors.qualitative.Plotly
ACCENT_COLORS = ['#6366f1','#22d3ee','#34d399','#fbbf24','#f43f5e','#a855f7',
                 '#fb923c','#3b82f6','#14b8a6','#ec4899','#84cc16','#38bdf8']


# ═══════════════════════════════════════════════════════════════
#  DATA LOADING & CLEANING
# ═══════════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def load_and_clean_data():
    """Load the dataset and perform all cleaning steps."""
    df = pd.read_csv('../DataSet/Dataset .csv', encoding='utf-8', on_bad_lines='skip')

    # ── Rename columns ──
    df.columns = [c.strip() for c in df.columns]

    # ── Map country codes ──
    df['Country'] = df['Country Code'].map(COUNTRY_MAP).fillna('Unknown')

    # ── Type corrections ──
    df['Aggregate rating'] = pd.to_numeric(df['Aggregate rating'], errors='coerce').fillna(0)
    df['Votes'] = pd.to_numeric(df['Votes'], errors='coerce').fillna(0).astype(int)
    df['Average Cost for two'] = pd.to_numeric(df['Average Cost for two'], errors='coerce').fillna(0)
    df['Price range'] = pd.to_numeric(df['Price range'], errors='coerce').fillna(0).astype(int)
    df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
    df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')

    # ── Boolean columns ──
    df['Has Table booking'] = df['Has Table booking'].str.strip().eq('Yes')
    df['Has Online delivery'] = df['Has Online delivery'].str.strip().eq('Yes')

    # ── Clean text ──
    df['Restaurant Name'] = df['Restaurant Name'].str.strip()
    df['City'] = df['City'].str.strip()
    df['Cuisines'] = df['Cuisines'].fillna('Unknown').str.strip()

    # ── Price range labels ──
    df['Price Label'] = df['Price range'].map({
        1: '💚 Budget', 2: '💙 Mid-Range',
        3: '💛 Premium', 4: '🔴 Luxury'
    }).fillna('Unknown')

    # ── Rating category ──
    def rate_cat(r):
        if r == 0: return 'Not Rated'
        elif r < 2: return 'Poor (< 2)'
        elif r < 3: return 'Average (2-3)'
        elif r < 3.5: return 'Good (3-3.5)'
        elif r < 4: return 'Very Good (3.5-4)'
        elif r < 4.5: return 'Excellent (4-4.5)'
        else: return 'Outstanding (4.5+)'
    df['Rating Category'] = df['Aggregate rating'].apply(rate_cat)

    # ── Revenue index ──
    df['Revenue Index'] = df['Average Cost for two'] * df['Votes'].clip(lower=1)

    # ── Remove exact duplicates ──
    df = df.drop_duplicates(subset=['Restaurant ID'])

    return df


# ═══════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════
def explode_cuisines(df):
    """Return a DataFrame with one row per cuisine."""
    rows = []
    for _, row in df.iterrows():
        for c in str(row['Cuisines']).split(','):
            c = c.strip()
            if c and c != 'Unknown':
                rows.append({'Cuisine': c, 'Revenue Index': row['Revenue Index'],
                             'Votes': row['Votes'], 'Rating': row['Aggregate rating'],
                             'Cost': row['Average Cost for two']})
    return pd.DataFrame(rows)


def fmt(n):
    if n >= 1_000_000: return f"{n/1_000_000:.1f}M"
    if n >= 1_000: return f"{n/1_000:.1f}K"
    return f"{n:,.0f}"


def make_chart(fig):
    """Apply standard dark theme to any plotly figure."""
    fig.update_layout(
        paper_bgcolor='#16161f',
        plot_bgcolor='#16161f',
        font=dict(color='#9495a7', family='Inter', size=12),
        title_font=dict(color='#f0f0f5', size=14, family='Inter'),
        legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='rgba(148,149,167,0.2)'),
        margin=dict(l=10, r=10, t=40, b=10),
        hoverlabel=dict(
            bgcolor='#1e1e2a', bordercolor='rgba(99,102,241,0.5)',
            font=dict(color='#f0f0f5', family='Inter', size=12)
        )
    )
    fig.update_xaxes(gridcolor='rgba(148,149,167,0.07)', zerolinecolor='rgba(148,149,167,0.1)')
    fig.update_yaxes(gridcolor='rgba(148,149,167,0.07)', zerolinecolor='rgba(148,149,167,0.1)')
    return fig


# ═══════════════════════════════════════════════════════════════
#  LOAD DATA
# ═══════════════════════════════════════════════════════════════
with st.spinner("🔄 Loading & cleaning dataset..."):
    df = load_and_clean_data()

cuisine_df = explode_cuisines(df)
rated_df   = df[df['Aggregate rating'] > 0]


# ═══════════════════════════════════════════════════════════════
#  SIDEBAR FILTERS
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🎛️ Filters")
    st.markdown("---")

    countries = st.multiselect(
        "🌍 Country",
        options=sorted(df['Country'].unique()),
        default=[],
        placeholder="All countries"
    )

    price_opts = ['💚 Budget','💙 Mid-Range','💛 Premium','🔴 Luxury']
    prices = st.multiselect(
        "💰 Price Range",
        options=price_opts,
        default=[],
        placeholder="All price ranges"
    )

    min_rating = st.slider("⭐ Minimum Rating", 0.0, 5.0, 0.0, 0.5)

    st.markdown("---")
    st.markdown("### 📂 About")
    st.markdown(f"""
    <div style='font-size:0.8rem;color:#9495a7;line-height:1.7'>
    📊 <b style='color:#f0f0f5'>{fmt(len(df))}</b> Restaurants<br>
    🌍 <b style='color:#f0f0f5'>{df['Country'].nunique()}</b> Countries<br>
    🏙️ <b style='color:#f0f0f5'>{df['City'].nunique()}</b> Cities<br>
    🍽️ <b style='color:#f0f0f5'>{cuisine_df['Cuisine'].nunique()}</b> Cuisines
    </div>
    """, unsafe_allow_html=True)


# ── Apply Filters ──
fdf = df.copy()
if countries: fdf = fdf[fdf['Country'].isin(countries)]
if prices:    fdf = fdf[fdf['Price Label'].isin(prices)]
if min_rating > 0: fdf = fdf[fdf['Aggregate rating'] >= min_rating]
fdf_cuisine = explode_cuisines(fdf)
fdf_rated   = fdf[fdf['Aggregate rating'] > 0]


# ═══════════════════════════════════════════════════════════════
#  HEADER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="dash-header">
    <p class="dash-title">🍽️ Restaurant Analytics Dashboard</p>
    <p class="dash-subtitle">
        Exploratory Data Analysis · 9,500+ Restaurants · 15 Countries · 10 Interactive Visualizations
    </p>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  KPI CARDS
# ═══════════════════════════════════════════════════════════════
k1, k2, k3, k4, k5, k6 = st.columns(6)

with k1:
    st.markdown(f"""
    <div class='kpi-card kpi-1'>
        <div class='kpi-icon'>🏢</div>
        <div class='kpi-value'>{fmt(len(fdf))}</div>
        <div class='kpi-label'>Total Restaurants</div>
        <div class='kpi-sub'>{fdf['Country'].nunique()} countries</div>
    </div>""", unsafe_allow_html=True)

with k2:
    avg_r = fdf_rated['Aggregate rating'].mean() if len(fdf_rated) else 0
    st.markdown(f"""
    <div class='kpi-card kpi-2'>
        <div class='kpi-icon'>⭐</div>
        <div class='kpi-value'>{avg_r:.2f}</div>
        <div class='kpi-label'>Avg Rating</div>
        <div class='kpi-sub'>{fmt(len(fdf_rated))} rated</div>
    </div>""", unsafe_allow_html=True)

with k3:
    tot_votes = fdf['Votes'].sum()
    st.markdown(f"""
    <div class='kpi-card kpi-3'>
        <div class='kpi-icon'>🗳️</div>
        <div class='kpi-value'>{fmt(tot_votes)}</div>
        <div class='kpi-label'>Total Votes</div>
        <div class='kpi-sub'>Avg {fmt(fdf['Votes'].mean())} / restaurant</div>
    </div>""", unsafe_allow_html=True)

with k4:
    n_cuisines = fdf_cuisine['Cuisine'].nunique()
    st.markdown(f"""
    <div class='kpi-card kpi-4'>
        <div class='kpi-icon'>🍽️</div>
        <div class='kpi-value'>{n_cuisines}</div>
        <div class='kpi-label'>Unique Cuisines</div>
        <div class='kpi-sub'>Across all regions</div>
    </div>""", unsafe_allow_html=True)

with k5:
    od_pct = fdf['Has Online delivery'].mean() * 100
    st.markdown(f"""
    <div class='kpi-card kpi-5'>
        <div class='kpi-icon'>📦</div>
        <div class='kpi-value'>{od_pct:.1f}%</div>
        <div class='kpi-label'>Online Delivery</div>
        <div class='kpi-sub'>{fmt(fdf['Has Online delivery'].sum())} restaurants</div>
    </div>""", unsafe_allow_html=True)

with k6:
    tb_pct = fdf['Has Table booking'].mean() * 100
    st.markdown(f"""
    <div class='kpi-card kpi-6'>
        <div class='kpi-icon'>📅</div>
        <div class='kpi-value'>{tb_pct:.1f}%</div>
        <div class='kpi-label'>Table Booking</div>
        <div class='kpi-sub'>{fmt(fdf['Has Table booking'].sum())} restaurants</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  SECTION 1: EXECUTIVE INSIGHTS
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class='section-header'>
    <div class='section-icon'>💡</div>
    <div>
        <div class='section-title'>Executive Insights</div>
        <div class='section-sub'>Key business findings from the data</div>
    </div>
</div>""", unsafe_allow_html=True)

top_country  = fdf['Country'].value_counts().idxmax()
top_city     = fdf['City'].value_counts().idxmax()
top_cuisine  = fdf_cuisine['Cuisine'].value_counts().idxmax()
excellent_pct = (len(fdf_rated[fdf_rated['Aggregate rating'] >= 4.5]) / max(len(fdf_rated),1)) * 100

i1, i2, i3, i4 = st.columns(4)
for col, emoji, title, text in [
    (i1, "🌏", "Market Leader",
     f"<span class='highlight'>{top_country}</span> dominates with "
     f"<span class='highlight'>{fmt(fdf[fdf['Country']==top_country].shape[0])}</span> listings"),
    (i2, "🏆", "Top Cuisine",
     f"<span class='highlight'>{top_cuisine}</span> is the most popular cuisine. "
     f"<span class='highlight'>{top_city}</span> is the top restaurant city."),
    (i3, "⭐", "Quality Split",
     f"<span class='highlight'>{excellent_pct:.1f}%</span> of restaurants are rated ≥4.5 (Outstanding). "
     f"Avg rating: <span class='highlight'>{avg_r:.2f}/5</span>"),
    (i4, "📱", "Digital Gap",
     f"Only <span class='highlight'>{od_pct:.1f}%</span> offer delivery & "
     f"<span class='highlight'>{tb_pct:.1f}%</span> allow booking — a massive growth opportunity")
]:
    with col:
        st.markdown(f"""
        <div class='insight-card'>
            <div class='insight-emoji'>{emoji}</div>
            <div class='insight-title'>{title}</div>
            <div class='insight-text'>{text}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  SECTION 2: TOP 3 REVENUE-DRIVING CATEGORIES
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class='section-header'>
    <div class='section-icon'>🏆</div>
    <div>
        <div class='section-title'>Top 3 Revenue-Driving Menu Categories</div>
        <div class='section-sub'>Ranked by Revenue Index = Avg Cost × Customer Votes</div>
    </div>
</div>""", unsafe_allow_html=True)

top3 = (fdf_cuisine.groupby('Cuisine')
        .agg(Revenue=('Revenue Index','sum'), Count=('Cuisine','count'),
             Avg_Rating=('Rating','mean'), Avg_Cost=('Cost','mean'),
             Total_Votes=('Votes','sum'))
        .reset_index()
        .query("Count >= 10")
        .sort_values('Revenue', ascending=False)
        .head(3))

medals = ['🥇', '🥈', '🥉']
card_classes = ['top3-gold', 'top3-silver', 'top3-bronze']
c1, c2, c3 = st.columns(3)
for col, (_, row), medal, cls in zip([c1,c2,c3], top3.iterrows(), medals, card_classes):
    with col:
        st.markdown(f"""
        <div class='top3-card {cls}'>
            <div style='font-size:2rem;margin-bottom:0.5rem'>{medal}</div>
            <div style='font-size:1.3rem;font-weight:800;color:#f0f0f5;margin-bottom:1rem'>
                {row['Cuisine']}
            </div>
            <table style='width:100%;font-size:0.8rem;border-collapse:collapse'>
                <tr><td style='color:#9495a7;padding:4px 0'>Revenue Index</td>
                    <td style='color:#f0f0f5;font-weight:600;text-align:right'>{fmt(row['Revenue'])}</td></tr>
                <tr><td style='color:#9495a7;padding:4px 0'>Restaurants</td>
                    <td style='color:#f0f0f5;font-weight:600;text-align:right'>{fmt(row['Count'])}</td></tr>
                <tr><td style='color:#9495a7;padding:4px 0'>Avg Rating</td>
                    <td style='color:#f0f0f5;font-weight:600;text-align:right'>{row['Avg_Rating']:.2f} ⭐</td></tr>
                <tr><td style='color:#9495a7;padding:4px 0'>Avg Cost (2 people)</td>
                    <td style='color:#f0f0f5;font-weight:600;text-align:right'>{fmt(row['Avg_Cost'])}</td></tr>
                <tr><td style='color:#9495a7;padding:4px 0'>Total Votes</td>
                    <td style='color:#f0f0f5;font-weight:600;text-align:right'>{fmt(row['Total_Votes'])}</td></tr>
            </table>
        </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  SECTION 3: REVENUE & RATING ANALYSIS
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class='section-header'>
    <div class='section-icon'>💰</div>
    <div>
        <div class='section-title'>Revenue & Rating Analysis</div>
        <div class='section-sub'>Revenue potential by cuisine and rating distribution</div>
    </div>
</div>""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

# Chart 1: Revenue by Cuisine (top 12)
with col1:
    rev_data = (fdf_cuisine.groupby('Cuisine')['Revenue Index']
                .sum().reset_index()
                .query("Cuisine != 'Unknown'")
                .sort_values('Revenue Index', ascending=True)
                .tail(12))

    fig = px.bar(rev_data, x='Revenue Index', y='Cuisine',
                 orientation='h',
                 color='Revenue Index',
                 color_continuous_scale=['#312e81','#6366f1','#22d3ee'],
                 title='💰 Top 12 Cuisines by Revenue Potential')
    fig.update_coloraxes(showscale=False)
    fig.update_traces(hovertemplate="<b>%{y}</b><br>Revenue: %{x:,.0f}<extra></extra>")
    st.plotly_chart(make_chart(fig), use_container_width=True)

# Chart 2: Rating Distribution
with col2:
    cat_order = ['Not Rated','Poor (< 2)','Average (2-3)','Good (3-3.5)',
                 'Very Good (3.5-4)','Excellent (4-4.5)','Outstanding (4.5+)']
    cat_colors = ['#5e5f72','#ef4444','#f97316','#fbbf24','#34d399','#22d3ee','#6366f1']
    rating_counts = fdf['Rating Category'].value_counts().reindex(cat_order, fill_value=0)

    fig = px.bar(x=rating_counts.index, y=rating_counts.values,
                 color=rating_counts.index,
                 color_discrete_sequence=cat_colors,
                 title='⭐ Rating Distribution')
    fig.update_traces(hovertemplate="<b>%{x}</b><br>Count: %{y:,}<extra></extra>")
    fig.update_layout(showlegend=False, xaxis_tickangle=-30)
    st.plotly_chart(make_chart(fig), use_container_width=True)


# ═══════════════════════════════════════════════════════════════
#  SECTION 4: CUISINE & PRICING INTELLIGENCE
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class='section-header'>
    <div class='section-icon'>🍽️</div>
    <div>
        <div class='section-title'>Cuisine & Pricing Intelligence</div>
        <div class='section-sub'>Most popular cuisines and price segmentation</div>
    </div>
</div>""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

# Chart 3: Top 15 Cuisines
with col1:
    top15 = (fdf_cuisine['Cuisine'].value_counts()
             .head(15).reset_index()
             .rename(columns={'index':'Cuisine','Cuisine':'Count'}))
    # Handle pandas version differences
    top15.columns = ['Cuisine','Count']
    top15 = top15.sort_values('Count', ascending=True)

    fig = px.bar(top15, x='Count', y='Cuisine',
                 orientation='h',
                 color='Count',
                 color_continuous_scale=['#1e1b4b','#6366f1','#a855f7'],
                 title='🍽️ Top 15 Most Popular Cuisines')
    fig.update_coloraxes(showscale=False)
    fig.update_traces(hovertemplate="<b>%{y}</b><br>Restaurants: %{x:,}<extra></extra>")
    st.plotly_chart(make_chart(fig), use_container_width=True)

# Chart 4: Price Range Pie
with col2:
    price_dist = fdf['Price Label'].value_counts().reset_index()
    price_dist.columns = ['Price Range','Count']

    fig = px.pie(price_dist, names='Price Range', values='Count',
                 color_discrete_sequence=['#34d399','#3b82f6','#fbbf24','#f43f5e'],
                 title='💰 Price Range Segmentation',
                 hole=0.45)
    fig.update_traces(
        textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>"
    )
    fig.update_layout(legend=dict(orientation='v', x=1, y=0.5))
    st.plotly_chart(make_chart(fig), use_container_width=True)


# ═══════════════════════════════════════════════════════════════
#  SECTION 5: GEOGRAPHIC ANALYSIS
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class='section-header'>
    <div class='section-icon'>🌍</div>
    <div>
        <div class='section-title'>Geographic Analysis</div>
        <div class='section-sub'>Market distribution across countries and cities</div>
    </div>
</div>""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

# Chart 5: Country Distribution
with col1:
    country_data = (fdf['Country'].value_counts()
                    .reset_index()
                    .rename(columns={'index':'Country','Country':'Count'}))
    country_data.columns = ['Country','Count']
    country_data = country_data.sort_values('Count', ascending=True)

    fig = px.bar(country_data, x='Count', y='Country',
                 orientation='h',
                 color='Count',
                 color_continuous_scale=['#0c4a6e','#22d3ee','#a5f3fc'],
                 title='🌍 Restaurants by Country')
    fig.update_coloraxes(showscale=False)
    fig.update_traces(hovertemplate="<b>%{y}</b><br>Restaurants: %{x:,}<extra></extra>")
    st.plotly_chart(make_chart(fig), use_container_width=True)

# Chart 6: Top 10 Cities
with col2:
    city_data = (fdf['City'].value_counts()
                 .head(10).reset_index()
                 .rename(columns={'index':'City','City':'Count'}))
    city_data.columns = ['City','Count']

    fig = px.bar(city_data, x='City', y='Count',
                 color='Count',
                 color_continuous_scale=['#14532d','#34d399','#a7f3d0'],
                 title='🏙️ Top 10 Cities by Restaurant Count')
    fig.update_coloraxes(showscale=False)
    fig.update_layout(xaxis_tickangle=-35)
    fig.update_traces(hovertemplate="<b>%{x}</b><br>Count: %{y:,}<extra></extra>")
    st.plotly_chart(make_chart(fig), use_container_width=True)


# ═══════════════════════════════════════════════════════════════
#  SECTION 6: SERVICE ADOPTION & COST-QUALITY
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class='section-header'>
    <div class='section-icon'>📈</div>
    <div>
        <div class='section-title'>Service Adoption & Cost-Quality Correlation</div>
        <div class='section-sub'>Digital services uptake and pricing vs. customer satisfaction</div>
    </div>
</div>""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

# Chart 7: Service Adoption
with col1:
    svc_labels = ['Online Delivery', 'Table Booking']
    svc_yes  = [fdf['Has Online delivery'].sum(), fdf['Has Table booking'].sum()]
    svc_no   = [len(fdf) - v for v in svc_yes]

    fig = go.Figure(data=[
        go.Bar(name='Available ✅', x=svc_labels, y=svc_yes,
               marker_color='#34d399',
               hovertemplate="<b>%{x}</b><br>Available: %{y:,}<extra></extra>"),
        go.Bar(name='Not Available ❌', x=svc_labels, y=svc_no,
               marker_color='rgba(244,63,94,0.45)',
               hovertemplate="<b>%{x}</b><br>Not Available: %{y:,}<extra></extra>")
    ])
    fig.update_layout(barmode='stack', title='📱 Digital Service Adoption')
    st.plotly_chart(make_chart(fig), use_container_width=True)

# Chart 8: Avg Rating by Price Range
with col2:
    pr_stats = (fdf_rated.groupby('Price Label')
                .agg(Avg_Rating=('Aggregate rating','mean'),
                     Count=('Restaurant Name','count'),
                     Avg_Cost=('Average Cost for two','mean'))
                .reset_index()
                .sort_values('Price Label'))

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=pr_stats['Price Label'], y=pr_stats['Avg_Rating'],
        name='Avg Rating',
        marker_color=['#34d399','#3b82f6','#fbbf24','#f43f5e'],
        hovertemplate="<b>%{x}</b><br>Avg Rating: %{y:.2f}<extra></extra>"
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=pr_stats['Price Label'], y=pr_stats['Count'],
        name='Restaurant Count', mode='lines+markers',
        line=dict(color='#a855f7', width=2.5),
        marker=dict(size=8, color='#a855f7'),
        hovertemplate="<b>%{x}</b><br>Count: %{y:,}<extra></extra>"
    ), secondary_y=True)
    fig.update_yaxes(title_text='Avg Rating', secondary_y=False,
                     range=[0, 5], title_font=dict(color='#9495a7'))
    fig.update_yaxes(title_text='Count', secondary_y=True,
                     title_font=dict(color='#9495a7'))
    fig.update_layout(title='💰 Cost vs. Quality Correlation')
    st.plotly_chart(make_chart(fig), use_container_width=True)


# ═══════════════════════════════════════════════════════════════
#  SECTION 7: CUSTOMER ENGAGEMENT SCATTER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class='section-header'>
    <div class='section-icon'>🎯</div>
    <div>
        <div class='section-title'>Customer Engagement Patterns</div>
        <div class='section-sub'>Votes vs. Rating — identifying star performers</div>
    </div>
</div>""", unsafe_allow_html=True)

scatter_df = fdf_rated[fdf_rated['Votes'] > 0].copy()
if len(scatter_df) > 1500:
    scatter_df = scatter_df.sample(1500, random_state=42)

fig = px.scatter(
    scatter_df, x='Votes', y='Aggregate rating',
    color='Price Label',
    size='Average Cost for two',
    size_max=18,
    hover_name='Restaurant Name',
    hover_data={'City': True, 'Cuisines': True, 'Votes': ':,',
                'Aggregate rating': ':.2f', 'Price Label': False,
                'Average Cost for two': False},
    color_discrete_map={
        '💚 Budget':'#34d399', '💙 Mid-Range':'#3b82f6',
        '💛 Premium':'#fbbf24', '🔴 Luxury':'#f43f5e'
    },
    title='🎯 Customer Votes vs. Aggregate Rating (Sample of 1,500)',
    opacity=0.75
)
fig.update_layout(
    xaxis_title='Number of Customer Votes',
    yaxis_title='Aggregate Rating',
    legend_title='Price Range'
)
st.plotly_chart(make_chart(fig), use_container_width=True)


# ═══════════════════════════════════════════════════════════════
#  SECTION 8: CUISINE QUALITY RANKING
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class='section-header'>
    <div class='section-icon'>🌟</div>
    <div>
        <div class='section-title'>Cuisine Quality Ranking</div>
        <div class='section-sub'>Average rating by cuisine (min. 20 restaurants)</div>
    </div>
</div>""", unsafe_allow_html=True)

qual = (fdf_cuisine[fdf_cuisine['Rating'] > 0]
        .groupby('Cuisine')
        .agg(Avg_Rating=('Rating','mean'), Count=('Cuisine','count'))
        .reset_index()
        .query("Count >= 20")
        .sort_values('Avg_Rating', ascending=True)
        .tail(15))

qual['Color'] = qual['Avg_Rating'].apply(
    lambda r: '#6366f1' if r >= 4 else '#fbbf24' if r >= 3.5 else '#f97316'
)

fig = px.bar(qual, x='Avg_Rating', y='Cuisine',
             orientation='h',
             color='Avg_Rating',
             color_continuous_scale=['#7c3aed','#6366f1','#22d3ee'],
             title='🌟 Top 15 Cuisines by Average Rating',
             text='Avg_Rating')
fig.update_coloraxes(showscale=False)
fig.update_traces(
    texttemplate='%{text:.2f}',
    textposition='outside',
    hovertemplate="<b>%{y}</b><br>Avg Rating: %{x:.2f}<extra></extra>"
)
fig.update_layout(xaxis_range=[2.5, 5.2])
st.plotly_chart(make_chart(fig), use_container_width=True)


# ═══════════════════════════════════════════════════════════════
#  SECTION 9: DATA QUALITY REPORT
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class='section-header'>
    <div class='section-icon'>🧹</div>
    <div>
        <div class='section-title'>Data Quality Report</div>
        <div class='section-sub'>Cleaned dataset — column-level completeness analysis</div>
    </div>
</div>""", unsafe_allow_html=True)

cols_to_check = {
    'Restaurant ID': 'Integer',
    'Restaurant Name': 'String',
    'Country': 'Categorical',
    'City': 'String',
    'Cuisines': 'Multi-value',
    'Average Cost for two': 'Numeric',
    'Price range': 'Ordinal (1-4)',
    'Aggregate rating': 'Numeric (0-5)',
    'Votes': 'Integer',
    'Has Table booking': 'Boolean',
    'Has Online delivery': 'Boolean',
}

quality_rows = []
for col, dtype in cols_to_check.items():
    if col not in df.columns:
        continue
    total = len(df)
    if col == 'Aggregate rating' or col == 'Votes':
        non_null = (df[col] >= 0).sum()
    elif col == 'Cuisines':
        non_null = (df[col].str.strip() != '').sum()
    else:
        non_null = df[col].notna().sum()
    missing = total - non_null
    pct = non_null / total * 100
    quality_rows.append({
        'Column': col, 'Data Type': dtype,
        'Non-Null': f"{non_null:,}", 'Missing': f"{missing:,}",
        'Completeness': pct
    })

quality_df = pd.DataFrame(quality_rows)

def color_completeness(val):
    if val >= 95: return 'color: #34d399; font-weight: 600'
    elif val >= 80: return 'color: #fbbf24; font-weight: 600'
    else: return 'color: #f43f5e; font-weight: 600'

styled = (quality_df.style
          .map(color_completeness, subset=['Completeness'])
          .format({'Completeness': '{:.1f}%'})
          .set_properties(**{
              'background-color': '#16161f',
              'color': '#f0f0f5',
              'border': '1px solid rgba(148,149,167,0.1)',
              'font-size': '13px',
              'padding': '8px 12px'
          }))

st.dataframe(styled, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════
#  SECTION 10: RAW DATA EXPLORER
# ═══════════════════════════════════════════════════════════════
with st.expander("🔍 Explore Raw Data", expanded=False):
    show_cols = ['Restaurant Name','Country','City','Cuisines',
                 'Average Cost for two','Price Label','Aggregate rating',
                 'Rating Category','Votes','Has Online delivery','Has Table booking']
    st.dataframe(
        fdf[show_cols].head(100).reset_index(drop=True),
        use_container_width=True,
        height=350
    )
    st.caption(f"Showing top 100 of {len(fdf):,} filtered records")


# ── Footer ────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center;padding:1rem 0;color:#5e5f72;font-size:0.8rem'>
    🍽️ Restaurant Analytics Dashboard &nbsp;·&nbsp;
    Built with Python, Streamlit, Pandas & Plotly &nbsp;·&nbsp;
    Dataset: 9,557 Restaurants | 15 Countries
</div>
""", unsafe_allow_html=True)
