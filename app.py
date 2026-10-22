import streamlit as st
import pandas as pd
import altair as alt
import scipy.stats as stats

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Chess Opening & Duration Explorer",
    page_icon="♟️",
    layout="wide"
)

# -----------------------------------------------------------------------------
# DATA LOADING & PREPROCESSING (Cached)
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv('chess_cleaned.csv')
    
    # columns 
    required_cols = ['id', 'opening_family', 'turns', 'opening_ply', 'rated', 'victory_status', 'white_rating', 'black_rating']
    for col in required_cols:
        if col not in df.columns:
            st.error(f"Missing required column: '{col}' in chess_cleaned.csv.")
            st.stop()
            
    # Calculate average rating and assign skill tiers
    df['avg_rating'] = (df['white_rating'] + df['black_rating']) / 2
    
    def get_skill_tier(rating):
        if rating < 1400:
            return 'Beginner (< 1400)'
        elif rating <= 1800:
            return 'Intermediate (1400 - 1800)'
        else:
            return 'Advanced (> 1800)'

    df['skill_tier'] = df['avg_rating'].apply(get_skill_tier)
    return df

try:
    chess = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# -----------------------------------------------------------------------------
# SIDEBAR CONTROLS (All 3 Filters Included)
# -----------------------------------------------------------------------------
st.sidebar.header("🎛️ Dashboard Filters")

# 1. Rated Status Filter
rated_options = chess['rated'].unique().tolist()
selected_rated = st.sidebar.multiselect(
    "Select Rated Status",
    options=rated_options,
    default=rated_options
)

# 2. Victory Status Filter
victory_options = chess['victory_status'].unique().tolist()
selected_victory = st.sidebar.multiselect(
    "Select Victory Status",
    options=victory_options,
    default=victory_options
)

# 3. Opening Families Multiselect Filter
top_families_list = chess['opening_family'].value_counts().head(8).index.tolist()
selected_families = st.sidebar.multiselect(
    "Select Opening Families:",
    options=top_families_list,
    default=top_families_list
)

# 4. Skill Tier Filter
rating_tier = st.sidebar.selectbox(
    "Select Skill Tier",
    options=["All Tiers", "Beginner (< 1400)", "Intermediate (1400 - 1800)", "Advanced (> 1800)"]
)

# Apply All Sidebar Filters
filtered_df = chess.copy()
if selected_rated:
    filtered_df = filtered_df[filtered_df['rated'].isin(selected_rated)]
if selected_victory:
    filtered_df = filtered_df[filtered_df['victory_status'].isin(selected_victory)]
if selected_families:
    filtered_df = filtered_df[filtered_df['opening_family'].isin(selected_families)]

if rating_tier == "Beginner (< 1400)":
    filtered_df = filtered_df[filtered_df['skill_tier'] == 'Beginner (< 1400)']
elif rating_tier == "Intermediate (1400 - 1800)":
    filtered_df = filtered_df[filtered_df['skill_tier'] == 'Intermediate (1400 - 1800)']
elif rating_tier == "Advanced (> 1800)":
    filtered_df = filtered_df[filtered_df['skill_tier'] == 'Advanced (> 1800)']

# -----------------------------------------------------------------------------
# MAIN DASHBOARD HEADER & METRICS
# -----------------------------------------------------------------------------
st.title("♟️ Chess Opening & Duration Explorer")
st.markdown("Explore the relationship between chess opening families, player skill tiers, opening theory depth, and game duration.")

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

total_games = len(filtered_df)
mean_turns = filtered_df['turns'].mean() if total_games > 0 else 0

if 'opening_ply' in filtered_df.columns and total_games > 1:
    r_val, p_val = stats.pearsonr(filtered_df['opening_ply'], filtered_df['turns'])
else:
    r_val, p_val = 0.0, 1.0

col1.metric("Total Games in View", f"{total_games:,}")
col2.metric("Mean Turns", f"{mean_turns:.1f} turns")
col3.metric("Opening Depth Correlation (r)", f"{r_val:.3f}")
col4.metric("Pearson p-value", "p < 0.001" if p_val < 0.001 else f"p = {p_val:.3f}")

st.markdown("---")

# -----------------------------------------------------------------------------
# VISUALIZATION 1: ALTAIR BUBBLE CHART (Opening Depth vs Game Duration)
# -----------------------------------------------------------------------------
st.subheader("📊 Opening Depth vs. Game Duration & Popularity")
st.markdown("Examining how opening theory depth (`opening_ply`) relates to overall game duration (`turns`) across selected opening families.")

if not filtered_df.empty:
    family_rel = filtered_df.groupby('opening_family').agg(
        mean_ply=('opening_ply', 'mean'),
        mean_turns=('turns', 'mean'),
        game_count=('turns', 'count')
    ).reset_index()

    bubble_chart = alt.Chart(family_rel).mark_circle(opacity=0.85, stroke='DarkSlateGrey', strokeWidth=1).encode(
        x=alt.X('mean_ply:Q', title='Average Opening Depth (Ply)'),
        y=alt.Y('mean_turns:Q', title='Average Total Game Duration (Turns)', scale=alt.Scale(zero=False)),
        size=alt.Size('game_count:Q', title='Total Games Played', legend=None, scale=alt.Scale(range=[100, 1000])),
        color=alt.Color('opening_family:N', title='Opening Family', legend=None),
        tooltip=['opening_family', 'mean_ply', 'mean_turns', 'game_count']
    ).properties(
        width=900,
        height=500,
        title='Relating Opening Depth, Game Duration, and Popularity Across Selected Families'
    )

    text_labels = alt.Chart(family_rel).mark_text(align='center', baseline='bottom', dy=-12, fontSize=11).encode(
        x='mean_ply:Q',
        y='mean_turns:Q',
        text='opening_family:N'
    )

    st.altair_chart(bubble_chart + text_labels, use_container_width=True)
else:
    st.warning("No data available with the current filter selection.")

st.markdown("---")

# -----------------------------------------------------------------------------
# VISUALIZATION 2: FACETED BAR CHART BY SKILL TIER (All Names Displayed)
# -----------------------------------------------------------------------------
st.subheader("📈 Average Game Duration by Opening Family & Skill Tier")
st.markdown("Ranking opening families broken down across player skill tiers using faceted small multiples.")

if len(filtered_df) > 0:
    bar_stats = filtered_df.groupby(['opening_family', 'skill_tier']).agg(
        mean_turns=('turns', 'mean'),
        game_count=('turns', 'count')
    ).reset_index()

    bar_chart = alt.Chart(bar_stats).mark_bar().encode(
        x=alt.X(
            'opening_family:N', 
            title='Opening Family', 
            axis=alt.Axis(
                labelAngle=-90,         
                labelOverlap=False       
            )
        ),
        y=alt.Y('mean_turns:Q', title='Mean Turns'),
        color=alt.Color('skill_tier:N', title='Skill Tier'),
        column=alt.Column('skill_tier:N', title='skill_tier'),
        tooltip=['opening_family', 'skill_tier', alt.Tooltip('mean_turns:Q', format='.1f'), 'game_count']
    ).properties(
        width=200,
        height=400
    ).resolve_axis(
        x='independent'
    )
    
    st.altair_chart(bar_chart, use_container_width=True)
else:
    st.warning("Please select at least one opening family / skill tier combination to display the bar chart.")

st.markdown("---")

# -----------------------------------------------------------------------------
# DATASET PREVIEW
# -----------------------------------------------------------------------------
st.subheader("📋 Filtered Dataset Preview")
preview_cols = [col for col in ['id', 'rated', 'turns', 'victory_status', 'opening_family', 'skill_tier', 'opening_ply', 'avg_rating'] if col in filtered_df.columns]
st.dataframe(filtered_df[preview_cols].head(100), use_container_width=True)