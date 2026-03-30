import streamlit as st
import pandas as pd
import numpy as np
import re
import os

st.set_page_config(
    page_title="NutriTrack",
    page_icon="🥑",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Italiana&family=Quicksand:wght@300;400;500;600&display=swap');

:root {
    --bg:         #fdf6fb;
    --bg2:        #f9eef7;
    --bg3:        #f3e6f5;
    --card:       #ffffff;
    --border:     #ead6f0;
    --border2:    #ddc4e8;

    --pink:       #f2a7c3;
    --pink-soft:  #fce4ef;
    --pink-text:  #c4607e;

    --lavender:   #b39ddb;
    --lav-soft:   #ede7f6;
    --lav-text:   #7b5ea7;

    --lilac:      #ce93d8;
    --lilac-soft: #f3e5f5;
    --lilac-text: #8e44ad;

    --periwinkle: #9fa8da;
    --peri-soft:  #e8eaf6;
    --peri-text:  #5c6bc0;

    --rose:       #f48fb1;
    --rose-soft:  #fce4ec;
    --rose-text:  #c2185b;

    --mint:       #a5d6a7;
    --mint-soft:  #e8f5e9;
    --mint-text:  #388e3c;

    --text:       #4a3558;
    --text2:      #7a5f8a;
    --muted:      #b09abf;
    --shadow:     rgba(160,120,190,0.12);
}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main .block-container {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Quicksand', sans-serif !important;
}

[data-testid="stHeader"]       { background: transparent !important; }
[data-testid="stToolbar"]      { display: none !important; }
[data-testid="stStatusWidget"] { display: none !important; }
[data-testid="stDecoration"]   { display: none !important; }

/* ── Soft gradient background ── */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(160deg, #fdf6fb 0%, #f5eafb 40%, #eee6f8 100%) !important;
}

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 2.5rem 0 1.6rem;
}
.hero-icon {
    font-size: 2.6rem;
    display: block;
    margin-bottom: 0.3rem;
    animation: float 3.5s ease-in-out infinite;
}
@keyframes float {
    0%,100% { transform: translateY(0px); }
    50%      { transform: translateY(-7px); }
}
.hero h1 {
    font-family: 'Italiana', serif;
    font-size: 3.8rem;
    font-weight: 400;
    background: linear-gradient(135deg, #c77dbd, #9b72cf, #7986cb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    line-height: 1;
    letter-spacing: 0.02em;
}
.hero p {
    color: var(--muted);
    font-size: 0.9rem;
    margin-top: 0.5rem;
    font-weight: 400;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
.hero-dots {
    margin-top: 0.9rem;
    display: flex;
    justify-content: center;
    gap: 0.4rem;
}
.dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    display: inline-block;
}

/* ── Input ── */
[data-testid="stTextInput"] > div > div {
    background: var(--card) !important;
    border: 1.5px solid var(--border2) !important;
    border-radius: 50px !important;
    padding: 0.25rem 1rem !important;
    font-size: 0.95rem !important;
    color: var(--text) !important;
    box-shadow: 0 4px 20px var(--shadow) !important;
    transition: all 0.25s;
}
[data-testid="stTextInput"] > div > div input {
    color: var(--text) !important;
    font-family: 'Quicksand', sans-serif !important;
    font-weight: 500 !important;
}
[data-testid="stTextInput"] > div > div input::placeholder {
    color: var(--muted) !important;
}
[data-testid="stTextInput"] > div > div:focus-within {
    border-color: var(--lavender) !important;
    box-shadow: 0 0 0 4px rgba(179,157,219,0.18), 0 4px 20px var(--shadow) !important;
}

/* ── Button ── */
[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #ce93d8, #9b72cf) !important;
    border: none !important;
    border-radius: 50px !important;
    font-family: 'Quicksand', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    color: #fff !important;
    letter-spacing: 0.05em;
    box-shadow: 0 6px 20px rgba(155,114,207,0.35) !important;
    transition: all 0.22s !important;
}
[data-testid="baseButton-primary"]:hover {
    background: linear-gradient(135deg, #ba68c8, #7e57c2) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 26px rgba(155,114,207,0.45) !important;
}

/* ── Cards ── */
.nutri-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 1.6rem 1.9rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 28px var(--shadow);
}
.nutri-card h3 {
    font-family: 'Italiana', serif;
    font-size: 1.4rem;
    font-weight: 400;
    margin: 0 0 1.2rem;
    color: var(--lav-text);
    letter-spacing: 0.03em;
}

/* ── Food header ── */
.food-name {
    font-family: 'Italiana', serif;
    font-size: 1.8rem;
    font-weight: 400;
    color: var(--text);
    letter-spacing: 0.02em;
}
.section-pill {
    display: inline-block;
    background: var(--lav-soft);
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 0.15rem 0.75rem;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--lav-text);
    font-weight: 600;
    margin-bottom: 0.4rem;
}

/* ── Macro grid ── */
.macro-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.85rem;
    margin-bottom: 0.4rem;
}
.macro-tile {
    border-radius: 20px;
    padding: 1.2rem 0.7rem;
    text-align: center;
    border: 1.5px solid transparent;
    transition: transform 0.18s, box-shadow 0.18s;
    position: relative;
    overflow: hidden;
}
.macro-tile:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px var(--shadow);
}
.macro-tile.cal   { background: var(--rose-soft);  border-color: #f8bbd0; }
.macro-tile.prot  { background: var(--mint-soft);  border-color: #c8e6c9; }
.macro-tile.carb  { background: var(--lav-soft);   border-color: #d1c4e9; }
.macro-tile.fat   { background: var(--pink-soft);  border-color: #f8bbd0; }
.macro-tile.fib   { background: var(--peri-soft);  border-color: #c5cae9; }
.macro-tile.sug   { background: var(--lilac-soft); border-color: #e1bee7; }

.macro-val {
    font-family: 'Italiana', serif;
    font-size: 2.2rem;
    font-weight: 400;
    line-height: 1;
    margin-bottom: 0.1rem;
}
.macro-tile.cal  .macro-val { color: var(--rose-text); }
.macro-tile.prot .macro-val { color: var(--mint-text); }
.macro-tile.carb .macro-val { color: var(--lav-text);  }
.macro-tile.fat  .macro-val { color: var(--pink-text); }
.macro-tile.fib  .macro-val { color: var(--peri-text); }
.macro-tile.sug  .macro-val { color: var(--lilac-text);}

.macro-unit  { font-size: 0.7rem; font-weight: 600; letter-spacing: 0.08em; opacity: 0.7; }
.macro-label { font-size: 0.76rem; margin-top: 0.3rem; font-weight: 600; opacity: 0.75; }

/* ── Calorie badge ── */
.cal-badge {
    display: inline-block;
    padding: 0.28rem 1rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.cal-badge.low    { background: var(--mint-soft);  color: var(--mint-text);  border: 1.5px solid #a5d6a7; }
.cal-badge.medium { background: var(--lav-soft);   color: var(--lav-text);   border: 1.5px solid var(--lavender); }
.cal-badge.high   { background: var(--rose-soft);  color: var(--rose-text);  border: 1.5px solid var(--rose); }

/* ── Bar viz ── */
.bar-wrap { margin-bottom: 1rem; }
.bar-meta {
    display: flex;
    justify-content: space-between;
    font-size: 0.8rem;
    color: var(--text2);
    margin-bottom: 0.3rem;
    font-weight: 600;
}
.bar-bg {
    background: var(--bg3);
    border-radius: 999px;
    height: 9px;
    overflow: hidden;
    border: 1px solid var(--border);
}
.bar-fill { height: 9px; border-radius: 999px; }

/* ── Micro table ── */
.micro-table { width: 100%; border-collapse: collapse; }
.micro-table tr { border-bottom: 1px solid var(--border); }
.micro-table tr:last-child { border: none; }
.micro-table td {
    padding: 0.6rem 0.2rem;
    font-size: 0.87rem;
    color: var(--text);
}
.micro-table td:first-child { color: var(--muted); font-weight: 500; }
.micro-table td:last-child  { text-align: right; font-weight: 600; color: var(--lav-text); }

/* ── Chips ── */
.chip-row { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.8rem; }
.chip {
    background: var(--card);
    border: 1.5px solid var(--border2);
    border-radius: 999px;
    padding: 0.3rem 0.9rem;
    font-size: 0.78rem;
    color: var(--text2);
    font-family: 'Quicksand', sans-serif;
    font-weight: 600;
    box-shadow: 0 2px 8px var(--shadow);
}

/* ── Not found ── */
.not-found {
    text-align: center;
    padding: 3rem 1rem;
    background: var(--card);
    border-radius: 24px;
    border: 1px solid var(--border);
    box-shadow: 0 4px 28px var(--shadow);
}
.not-found .icon { font-size: 2.8rem; margin-bottom: 0.6rem; }
.not-found h3 {
    font-family: 'Italiana', serif;
    color: var(--text);
    font-size: 1.5rem;
    font-weight: 400;
    margin: 0.2rem 0 0.4rem;
}
.not-found p { color: var(--muted); font-size: 0.88rem; }

/* ── Footer ── */
.footer {
    text-align: center;
    color: var(--muted);
    font-size: 0.75rem;
    margin-top: 3rem;
    padding-bottom: 2rem;
    letter-spacing: 0.06em;
}
.footer span { color: var(--pink); }
</style>
""", unsafe_allow_html=True)


# ─── Data ─────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    possible_paths = [
        "datset.xlsx", "dataset.xlsx",
        "/Users/saivedhathota/Desktop/batch 8 iomp/datset.xlsx",
    ]
    df = None
    for path in possible_paths:
        if os.path.exists(path):
            df = pd.read_excel(path)
            break
    if df is None:
        demo_foods = [
            {"name": "apple", "calories": 95, "protein": 0.5, "carbohydrates": 25, "fat": 0.3,
             "fiber": 4.4, "sugar": 19, "sodium": 2, "potassium": 195, "calcium": 11, "iron": 0.2, "magnesium": 9, "vitamin_c": 8.4},
            {"name": "banana", "calories": 105, "protein": 1.3, "carbohydrates": 27, "fat": 0.4,
             "fiber": 3.1, "sugar": 14, "sodium": 1, "potassium": 422, "calcium": 6, "iron": 0.3, "magnesium": 32, "vitamin_c": 10.3},
            {"name": "chicken breast", "calories": 165, "protein": 31, "carbohydrates": 0, "fat": 3.6,
             "fiber": 0, "sugar": 0, "sodium": 74, "potassium": 256, "calcium": 15, "iron": 0.9, "magnesium": 29, "vitamin_c": 0},
            {"name": "brown rice", "calories": 216, "protein": 5, "carbohydrates": 45, "fat": 1.8,
             "fiber": 3.5, "sugar": 0, "sodium": 10, "potassium": 84, "calcium": 20, "iron": 1, "magnesium": 84, "vitamin_c": 0},
            {"name": "egg", "calories": 78, "protein": 6, "carbohydrates": 0.6, "fat": 5,
             "fiber": 0, "sugar": 0.6, "sodium": 62, "potassium": 63, "calcium": 28, "iron": 0.9, "magnesium": 6, "vitamin_c": 0},
            {"name": "broccoli", "calories": 55, "protein": 3.7, "carbohydrates": 11, "fat": 0.6,
             "fiber": 5.1, "sugar": 2.6, "sodium": 64, "potassium": 457, "calcium": 62, "iron": 0.7, "magnesium": 25, "vitamin_c": 89.2},
            {"name": "salmon", "calories": 208, "protein": 20, "carbohydrates": 0, "fat": 13,
             "fiber": 0, "sugar": 0, "sodium": 59, "potassium": 363, "calcium": 13, "iron": 0.3, "magnesium": 27, "vitamin_c": 0},
            {"name": "oats", "calories": 307, "protein": 11, "carbohydrates": 55, "fat": 5,
             "fiber": 8, "sugar": 1, "sodium": 5, "potassium": 335, "calcium": 54, "iron": 4, "magnesium": 138, "vitamin_c": 0},
            {"name": "avocado", "calories": 160, "protein": 2, "carbohydrates": 9, "fat": 15,
             "fiber": 7, "sugar": 0.7, "sodium": 7, "potassium": 485, "calcium": 12, "iron": 0.6, "magnesium": 29, "vitamin_c": 10},
            {"name": "sweet potato", "calories": 103, "protein": 2.3, "carbohydrates": 24, "fat": 0.1,
             "fiber": 3.8, "sugar": 7.4, "sodium": 41, "potassium": 438, "calcium": 39, "iron": 0.8, "magnesium": 27, "vitamin_c": 22.3},
            {"name": "almonds", "calories": 579, "protein": 21, "carbohydrates": 22, "fat": 50,
             "fiber": 12.5, "sugar": 4.4, "sodium": 1, "potassium": 705, "calcium": 264, "iron": 3.7, "magnesium": 270, "vitamin_c": 0},
            {"name": "greek yogurt", "calories": 59, "protein": 10, "carbohydrates": 3.6, "fat": 0.4,
             "fiber": 0, "sugar": 3.2, "sodium": 36, "potassium": 141, "calcium": 110, "iron": 0.1, "magnesium": 11, "vitamin_c": 0},
            {"name": "spinach", "calories": 23, "protein": 2.9, "carbohydrates": 3.6, "fat": 0.4,
             "fiber": 2.2, "sugar": 0.4, "sodium": 79, "potassium": 558, "calcium": 99, "iron": 2.7, "magnesium": 79, "vitamin_c": 28.1},
            {"name": "whole milk", "calories": 149, "protein": 8, "carbohydrates": 12, "fat": 8,
             "fiber": 0, "sugar": 12, "sodium": 105, "potassium": 349, "calcium": 276, "iron": 0.1, "magnesium": 24, "vitamin_c": 0},
            {"name": "orange", "calories": 62, "protein": 1.2, "carbohydrates": 15, "fat": 0.2,
             "fiber": 3.1, "sugar": 12, "sodium": 0, "potassium": 237, "calcium": 52, "iron": 0.1, "magnesium": 13, "vitamin_c": 69.7},
            {"name": "lentils", "calories": 230, "protein": 18, "carbohydrates": 40, "fat": 0.8,
             "fiber": 15.6, "sugar": 3.6, "sodium": 4, "potassium": 731, "calcium": 37, "iron": 6.6, "magnesium": 71, "vitamin_c": 4.4},
            {"name": "tuna", "calories": 128, "protein": 28, "carbohydrates": 0, "fat": 1.2,
             "fiber": 0, "sugar": 0, "sodium": 339, "potassium": 229, "calcium": 10, "iron": 1.3, "magnesium": 35, "vitamin_c": 0},
            {"name": "quinoa", "calories": 222, "protein": 8, "carbohydrates": 39, "fat": 3.5,
             "fiber": 5, "sugar": 1.6, "sodium": 13, "potassium": 318, "calcium": 31, "iron": 2.8, "magnesium": 118, "vitamin_c": 0},
            {"name": "pizza", "calories": 285, "protein": 12, "carbohydrates": 36, "fat": 10,
             "fiber": 2.3, "sugar": 3.6, "sodium": 640, "potassium": 184, "calcium": 188, "iron": 2.6, "magnesium": 23, "vitamin_c": 2},
            {"name": "burger", "calories": 354, "protein": 20, "carbohydrates": 29, "fat": 17,
             "fiber": 1, "sugar": 6, "sodium": 497, "potassium": 320, "calcium": 96, "iron": 2.8, "magnesium": 28, "vitamin_c": 1},
            {"name": "pasta", "calories": 220, "protein": 8, "carbohydrates": 43, "fat": 1.3,
             "fiber": 2.5, "sugar": 0.6, "sodium": 1, "potassium": 58, "calcium": 10, "iron": 1.8, "magnesium": 30, "vitamin_c": 0},
            {"name": "carrot", "calories": 41, "protein": 0.9, "carbohydrates": 10, "fat": 0.2,
             "fiber": 2.8, "sugar": 4.7, "sodium": 69, "potassium": 320, "calcium": 33, "iron": 0.3, "magnesium": 12, "vitamin_c": 5.9},
            {"name": "tomato", "calories": 18, "protein": 0.9, "carbohydrates": 3.9, "fat": 0.2,
             "fiber": 1.2, "sugar": 2.6, "sodium": 5, "potassium": 237, "calcium": 10, "iron": 0.3, "magnesium": 11, "vitamin_c": 13.7},
            {"name": "white rice", "calories": 206, "protein": 4.3, "carbohydrates": 45, "fat": 0.4,
             "fiber": 0.6, "sugar": 0, "sodium": 2, "potassium": 55, "calcium": 16, "iron": 1.9, "magnesium": 19, "vitamin_c": 0},
            {"name": "bread", "calories": 265, "protein": 9, "carbohydrates": 49, "fat": 3.2,
             "fiber": 2.7, "sugar": 5, "sodium": 491, "potassium": 115, "calcium": 151, "iron": 3.6, "magnesium": 25, "vitamin_c": 0},
        ]
        df = pd.DataFrame(demo_foods)
    return df


@st.cache_data(show_spinner=False)
def preprocess_data(df):
    df = df.copy()
    df.columns = (df.columns.str.strip().str.lower()
                  .str.replace(r'[^a-z0-9_]', '_', regex=True)
                  .str.replace(r'__+', '_', regex=True))
    aliases = [('carbs','carbohydrates'),('carbohydrate','carbohydrates'),
               ('sugars','sugar'),('vitamin c','vitamin_c'),('calorie','calories')]
    for src, dst in aliases:
        if src in df.columns and dst not in df.columns:
            df[dst] = df[src]
    for drop_col in ['unnamed_0', 'saturated_fat']:
        if drop_col in df.columns:
            df.drop(drop_col, axis=1, inplace=True)
    for col in df.columns:
        if col != 'name':
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(r'[^0-9.]','',regex=True), errors='coerce')
    df['name'] = df['name'].apply(lambda t: re.sub(r'[^a-zA-Z ]','',str(t).lower()).strip())
    df.dropna(subset=['name'], inplace=True)
    return df


def fuzzy_search(query, df, top_k=5):
    q = re.sub(r'[^a-zA-Z ]', '', query.lower()).strip()
    names = df['name'].str.lower()
    exact = df[names == q]
    if not exact.empty:
        return exact.iloc[0], df[names != q].head(top_k - 1)
    sw = df[names.str.startswith(q)]
    if not sw.empty:
        return sw.iloc[0], df[(names != sw.iloc[0]['name']) & names.str.contains(q, na=False)].head(top_k - 1)
    ct = df[names.str.contains(q, na=False)]
    if not ct.empty:
        return ct.iloc[0], ct.iloc[1:top_k]
    q_tokens = set(q.split())
    scores = names.apply(lambda n: len(q_tokens & set(n.split())))
    best_idx = scores.idxmax()
    if scores[best_idx] > 0:
        return df.loc[best_idx], df[scores > 0].drop(best_idx).head(top_k - 1)
    return None, pd.DataFrame()


def calorie_category(cal):
    if cal < 100:   return "low",    "Low Calorie"
    elif cal < 300: return "medium", "Moderate"
    else:           return "high",   "High Calorie"


def progress_bar(label, value, max_val, grad):
    pct = min(100, (value / max_val) * 100) if max_val > 0 else 0
    return f"""
    <div class="bar-wrap">
        <div class="bar-meta"><span>{label}</span><span>{value:.1f} g</span></div>
        <div class="bar-bg">
            <div class="bar-fill" style="width:{pct:.1f}%;background:{grad};border-radius:999px;"></div>
        </div>
    </div>"""


# ── Load ──
with st.spinner("Loading…"):
    df_raw = load_data()
    df     = preprocess_data(df_raw)

# ── Hero ──
st.markdown("""
<div class="hero">
    <span class="hero-icon">🍲</span>
    <h1>NutriTrack</h1>
    <p>your daily nutritional companion</p>
    <div class="hero-dots">
        <span class="dot" style="background:#f2a7c3;"></span>
        <span class="dot" style="background:#ce93d8;"></span>
        <span class="dot" style="background:#b39ddb;"></span>
        <span class="dot" style="background:#9fa8da;"></span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Search ──
col1, col2 = st.columns([4, 1])
with col1:
    query = st.text_input("", placeholder="🔍  Search a food — apple, oats, salmon…", label_visibility="collapsed")
with col2:
    search_btn = st.button("Track", type="primary", use_container_width=True)

# ── Chips ──
suggestions = ["🍎 Apple", "🥚 Egg", "🍌 Banana", "🐟 Salmon", "🥑 Avocado", "🥦 Broccoli"]
st.markdown(
    '<div class="chip-row">' + ''.join(f'<span class="chip">{s}</span>' for s in suggestions) + '</div>',
    unsafe_allow_html=True
)
st.markdown("<br>", unsafe_allow_html=True)

# ── Results ──
if query or search_btn:
    food, similar = fuzzy_search(query, df)

    if food is None:
        st.markdown(f"""
        <div class="not-found">
            <div class="icon"></div>
            <h3>No results for "{query}"</h3>
            <p>Try a different spelling, or pick one of the suggestions above!</p>
        </div>""", unsafe_allow_html=True)
    else:
        name_display = food['name'].title()
        cal   = food.get('calories',      0) or 0
        prot  = food.get('protein',       0) or 0
        carb  = food.get('carbohydrates', 0) or 0
        fat   = food.get('fat',           0) or 0
        fiber = food.get('fiber',         0) or 0
        sugar = food.get('sugar',         0) or 0
        cat_cls, cat_label = calorie_category(cal)

        # ── Macro tiles ──
        st.markdown(f"""
        <div class="nutri-card">
            <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:1.3rem;flex-wrap:wrap;gap:0.5rem;">
                <div>
                    <div class="section-pill"> per 100 g serving</div>
                    <div class="food-name">{name_display}</div>
                </div>
                <span class="cal-badge {cat_cls}">{cat_label}</span>
            </div>
            <div class="macro-grid">
                <div class="macro-tile cal">
                    <div class="macro-val">{cal:.0f}</div>
                    <div class="macro-unit">KCAL</div>
                    <div class="macro-label">Calories</div>
                </div>
                <div class="macro-tile prot">
                    <div class="macro-val">{prot:.1f}</div>
                    <div class="macro-unit">G</div>
                    <div class="macro-label">Protein</div>
                </div>
                <div class="macro-tile carb">
                    <div class="macro-val">{carb:.1f}</div>
                    <div class="macro-unit">G</div>
                    <div class="macro-label">Carbs</div>
                </div>
                <div class="macro-tile fat">
                    <div class="macro-val">{fat:.1f}</div>
                    <div class="macro-unit">G</div>
                    <div class="macro-label">Fat</div>
                </div>
                <div class="macro-tile fib">
                    <div class="macro-val">{fiber:.1f}</div>
                    <div class="macro-unit">G</div>
                    <div class="macro-label">Fiber</div>
                </div>
                <div class="macro-tile sug">
                    <div class="macro-val">{sugar:.1f}</div>
                    <div class="macro-unit">G</div>
                    <div class="macro-label">Sugar</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

        # ── Breakdown bars ──
        if prot * 4 + carb * 4 + fat * 9 > 0:
            st.markdown('<div class="nutri-card"><h3> Macro Breakdown</h3>', unsafe_allow_html=True)
            st.markdown(progress_bar("Protein",       prot,  50,  "linear-gradient(90deg,#f48fb1,#ce93d8)"), unsafe_allow_html=True)
            st.markdown(progress_bar("Carbohydrates", carb,  100, "linear-gradient(90deg,#b39ddb,#9fa8da)"), unsafe_allow_html=True)
            st.markdown(progress_bar("Fat",           fat,   80,  "linear-gradient(90deg,#f2a7c3,#f48fb1)"), unsafe_allow_html=True)
            st.markdown(progress_bar("Fiber",         fiber, 30,  "linear-gradient(90deg,#a5d6a7,#80cbc4)"), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Micronutrients ──
        micro_cols = {
            'sodium':('Sodium','mg'), 'potassium':('Potassium','mg'),
            'calcium':('Calcium','mg'), 'iron':('Iron','mg'),
            'magnesium':('Magnesium','mg'), 'vitamin_c':('Vitamin C','mg'),
            'vitamin_a':('Vitamin A','IU'), 'zinc':('Zinc','mg'),
            'phosphorus':('Phosphorus','mg'), 'folate':('Folate','mcg'),
        }
        available = {k:v for k,v in micro_cols.items()
                     if k in food.index and pd.notna(food[k]) and food[k] != 0}
        if available:
            rows = "".join(f"<tr><td>{lbl}</td><td>{food[k]:.1f} {unit}</td></tr>"
                           for k,(lbl,unit) in available.items())
            st.markdown(f"""
            <div class="nutri-card">
                <h3>Micronutrients</h3>
                <table class="micro-table"><tbody>{rows}</tbody></table>
            </div>""", unsafe_allow_html=True)

        # ── Daily Values ──
        st.markdown(f"""
        <div class="nutri-card">
            <h3>Daily Value Reference
                <span style="font-size:0.7rem;color:var(--muted);font-family:'Quicksand',sans-serif;font-weight:400;margin-left:0.4rem;">
                    based on 2000 kcal diet
                </span>
            </h3>
            <table class="micro-table">
                <tbody>
                    <tr><td>Calories</td><td>{round((cal/2000)*100)}%</td></tr>
                    <tr><td>Protein</td><td>{round((prot/50)*100)}%</td></tr>
                    <tr><td>Carbohydrates</td><td>{round((carb/275)*100)}%</td></tr>
                    <tr><td>Fat</td><td>{round((fat/78)*100)}%</td></tr>
                </tbody>
            </table>
        </div>""", unsafe_allow_html=True)

        # ── Similar ──
        if not similar.empty:
            chips = "".join(f'<span class="chip">{r["name"].title()}</span>' for _,r in similar.iterrows())
            st.markdown(f'<div class="nutri-card"><h3> You might also like</h3><div class="chip-row">{chips}</div></div>',
                        unsafe_allow_html=True)

# ── Footer ──
st.markdown("""
<div class="footer">
    made with <span>♥</span> · NutriTrack · values per 100 g · approximate reference data
</div>""", unsafe_allow_html=True)