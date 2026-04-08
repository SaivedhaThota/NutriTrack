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

# ─── CSS ──────────────────────────────────────────────────────────────────────
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
    --warn:       #ff8a65;
    --warn-soft:  #fbe9e7;
    --warn-text:  #bf360c;
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
[data-testid="stAppViewContainer"] {
    background: linear-gradient(160deg,#fdf6fb 0%,#f5eafb 40%,#eee6f8 100%) !important;
}
[data-testid="stHeader"]       { background: transparent !important; }
[data-testid="stToolbar"]      { display: none !important; }
[data-testid="stStatusWidget"] { display: none !important; }
[data-testid="stDecoration"]   { display: none !important; }

/* ── Nav tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    background: var(--card) !important;
    border-radius: 50px !important;
    padding: 0.25rem !important;
    border: 1.5px solid var(--border2) !important;
    box-shadow: 0 4px 20px var(--shadow) !important;
    gap: 0.2rem !important;
}
[data-testid="stTabs"] [role="tab"] {
    border-radius: 50px !important;
    font-family: 'Quicksand', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    color: var(--muted) !important;
    padding: 0.45rem 1.4rem !important;
    transition: all 0.2s !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg,#ce93d8,#9b72cf) !important;
    color: white !important;
    box-shadow: 0 4px 14px rgba(155,114,207,0.35) !important;
}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] { display:none !important; }
[data-testid="stTabs"] [data-baseweb="tab-border"]    { display:none !important; }

/* ── Hero ── */
.hero { text-align:center; padding:2.2rem 0 1.4rem; }
.hero-icon {
    font-size:2.4rem; display:block; margin-bottom:0.3rem;
    animation: float 3.5s ease-in-out infinite;
}
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-7px)} }
.hero h1 {
    font-family:'Italiana',serif; font-size:3.6rem; font-weight:400;
    background:linear-gradient(135deg,#c77dbd,#9b72cf,#7986cb);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text; margin:0; line-height:1; letter-spacing:0.02em;
}
.hero p { color:var(--muted); font-size:0.88rem; margin-top:0.4rem; letter-spacing:0.12em; text-transform:uppercase; }
.hero-dots { margin-top:0.8rem; display:flex; justify-content:center; gap:0.4rem; }
.dot { width:6px; height:6px; border-radius:50%; display:inline-block; }

/* ── Cards ── */
.nutri-card {
    background:var(--card); border:1px solid var(--border);
    border-radius:24px; padding:1.6rem 1.9rem; margin-bottom:1rem;
    box-shadow:0 4px 28px var(--shadow);
}
.nutri-card h3 {
    font-family:'Italiana',serif; font-size:1.4rem; font-weight:400;
    margin:0 0 1.2rem; color:var(--lav-text); letter-spacing:0.03em;
}

/* ── Profile card ── */
.profile-banner {
    background: linear-gradient(135deg,#f3e5f5,#ede7f6,#e8eaf6);
    border:1.5px solid var(--border2); border-radius:24px;
    padding:1.5rem 1.9rem; margin-bottom:1rem;
    display:flex; align-items:center; gap:1.2rem;
    box-shadow:0 4px 20px var(--shadow);
}
.profile-avatar {
    width:62px; height:62px; border-radius:50%;
    background:linear-gradient(135deg,#ce93d8,#9b72cf);
    display:flex; align-items:center; justify-content:center;
    font-size:1.8rem; flex-shrink:0;
    box-shadow:0 4px 14px rgba(155,114,207,0.3);
}
.profile-name { font-family:'Italiana',serif; font-size:1.5rem; color:var(--text); line-height:1.1; }
.profile-meta { font-size:0.78rem; color:var(--muted); margin-top:0.15rem; font-weight:500; }
.condition-tags { display:flex; flex-wrap:wrap; gap:0.4rem; margin-top:0.55rem; }
.condition-tag {
    display:inline-block; padding:0.2rem 0.75rem; border-radius:999px;
    font-size:0.72rem; font-weight:600; letter-spacing:0.06em;
}
.tag-diabetes  { background:#fce4ec; color:#c2185b; border:1.5px solid #f48fb1; }
.tag-hypertension { background:#e8eaf6; color:#3949ab; border:1.5px solid #9fa8da; }
.tag-obesity   { background:#fff3e0; color:#e65100; border:1.5px solid #ffb74d; }
.tag-cholesterol { background:#e8f5e9; color:#2e7d32; border:1.5px solid #81c784; }
.tag-kidney    { background:#fce4ec; color:#ad1457; border:1.5px solid #f06292; }
.tag-none      { background:#f3e5f5; color:#7b5ea7; border:1.5px solid #ce93d8; }

/* ── Food name ── */
.food-name { font-family:'Italiana',serif; font-size:1.8rem; font-weight:400; color:var(--text); letter-spacing:0.02em; }
.section-pill {
    display:inline-block; background:var(--lav-soft); border:1px solid var(--border);
    border-radius:999px; padding:0.15rem 0.75rem; font-size:0.68rem;
    letter-spacing:0.12em; text-transform:uppercase; color:var(--lav-text);
    font-weight:600; margin-bottom:0.4rem;
}

/* ── Alert banners ── */
.alert-banner {
    border-radius:16px; padding:1rem 1.3rem; margin-bottom:1rem;
    display:flex; align-items:flex-start; gap:0.8rem;
    border:1.5px solid;
}
.alert-banner.danger  { background:#ffeef2; border-color:#f48fb1; }
.alert-banner.warning { background:#fff8e1; border-color:#ffd54f; }
.alert-banner.safe    { background:#f1f8e9; border-color:#aed581; }
.alert-icon  { font-size:1.4rem; flex-shrink:0; margin-top:0.05rem; }
.alert-title { font-weight:700; font-size:0.9rem; margin-bottom:0.15rem; }
.alert-danger-title  { color:#c62828; }
.alert-warning-title { color:#f57f17; }
.alert-safe-title    { color:#2e7d32; }
.alert-body  { font-size:0.82rem; color:var(--text2); line-height:1.5; }

/* ── Macro grid ── */
.macro-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:0.85rem; margin-bottom:0.4rem; }
.macro-tile {
    border-radius:20px; padding:1.2rem 0.7rem; text-align:center;
    border:1.5px solid transparent; transition:transform 0.18s,box-shadow 0.18s;
}
.macro-tile:hover { transform:translateY(-3px); box-shadow:0 8px 24px var(--shadow); }
.macro-tile.cal  { background:var(--rose-soft);  border-color:#f8bbd0; }
.macro-tile.prot { background:var(--mint-soft);  border-color:#c8e6c9; }
.macro-tile.carb { background:var(--lav-soft);   border-color:#d1c4e9; }
.macro-tile.fat  { background:var(--pink-soft);  border-color:#f8bbd0; }
.macro-tile.fib  { background:var(--peri-soft);  border-color:#c5cae9; }
.macro-tile.sug  { background:var(--lilac-soft); border-color:#e1bee7; }
.macro-val { font-family:'Italiana',serif; font-size:2.2rem; font-weight:400; line-height:1; margin-bottom:0.1rem; }
.macro-tile.cal  .macro-val { color:var(--rose-text); }
.macro-tile.prot .macro-val { color:var(--mint-text); }
.macro-tile.carb .macro-val { color:var(--lav-text);  }
.macro-tile.fat  .macro-val { color:var(--pink-text); }
.macro-tile.fib  .macro-val { color:var(--peri-text); }
.macro-tile.sug  .macro-val { color:var(--lilac-text);}
.macro-unit  { font-size:0.7rem; font-weight:600; letter-spacing:0.08em; opacity:0.7; }
.macro-label { font-size:0.76rem; margin-top:0.3rem; font-weight:600; opacity:0.75; }

/* ── Flagged nutrient highlight ── */
.flagged { outline:2.5px solid #f48fb1 !important; background:#ffeef2 !important; }
.flagged .macro-val { color:#c62828 !important; }

/* ── Cal badge ── */
.cal-badge {
    display:inline-block; padding:0.28rem 1rem; border-radius:999px;
    font-size:0.72rem; font-weight:600; letter-spacing:0.08em; text-transform:uppercase;
}
.cal-badge.low    { background:var(--mint-soft);  color:var(--mint-text);  border:1.5px solid #a5d6a7; }
.cal-badge.medium { background:var(--lav-soft);   color:var(--lav-text);   border:1.5px solid var(--lavender); }
.cal-badge.high   { background:var(--rose-soft);  color:var(--rose-text);  border:1.5px solid var(--rose); }

/* ── Bars ── */
.bar-wrap { margin-bottom:1rem; }
.bar-meta { display:flex; justify-content:space-between; font-size:0.8rem; color:var(--text2); margin-bottom:0.3rem; font-weight:600; }
.bar-bg   { background:var(--bg3); border-radius:999px; height:9px; overflow:hidden; border:1px solid var(--border); }
.bar-fill { height:9px; border-radius:999px; }

/* ── Micro table ── */
.micro-table { width:100%; border-collapse:collapse; }
.micro-table tr { border-bottom:1px solid var(--border); }
.micro-table tr:last-child { border:none; }
.micro-table td { padding:0.6rem 0.2rem; font-size:0.87rem; color:var(--text); }
.micro-table td:first-child { color:var(--muted); font-weight:500; }
.micro-table td:last-child  { text-align:right; font-weight:600; color:var(--lav-text); }

/* ── Chips ── */
.chip-row { display:flex; flex-wrap:wrap; gap:0.5rem; margin-top:0.8rem; }
.chip {
    background:var(--card); border:1.5px solid var(--border2); border-radius:999px;
    padding:0.3rem 0.9rem; font-size:0.78rem; color:var(--text2);
    font-family:'Quicksand',sans-serif; font-weight:600; box-shadow:0 2px 8px var(--shadow);
}

/* ── Rec card ── */
.rec-food-card {
    background:var(--card); border:1px solid var(--border); border-radius:18px;
    padding:1rem 1.2rem; margin-bottom:0.7rem; box-shadow:0 2px 14px var(--shadow);
    display:flex; align-items:center; justify-content:space-between; gap:1rem; flex-wrap:wrap;
}
.rec-food-name { font-family:'Italiana',serif; font-size:1.1rem; color:var(--text); }
.rec-food-meta { font-size:0.78rem; color:var(--muted); margin-top:0.1rem; }
.rec-badge {
    display:inline-block; padding:0.22rem 0.8rem; border-radius:999px;
    font-size:0.7rem; font-weight:700; letter-spacing:0.06em; white-space:nowrap;
}
.rec-badge.great  { background:#e8f5e9; color:#2e7d32; border:1.5px solid #81c784; }
.rec-badge.ok     { background:#fff8e1; color:#f57f17; border:1.5px solid #ffd54f; }
.rec-badge.avoid  { background:#fce4ec; color:#c62828; border:1.5px solid #ef9a9a; }

/* ── Not found ── */
.not-found {
    text-align:center; padding:3rem 1rem;
    background:var(--card); border-radius:24px; border:1px solid var(--border);
    box-shadow:0 4px 28px var(--shadow);
}
.not-found .icon { font-size:2.8rem; margin-bottom:0.6rem; }
.not-found h3 { font-family:'Italiana',serif; color:var(--text); font-size:1.5rem; font-weight:400; margin:0.2rem 0 0.4rem; }
.not-found p { color:var(--muted); font-size:0.88rem; }

/* ── Input & button ── */
[data-testid="stTextInput"] > div > div {
    background:var(--card) !important; border:1.5px solid var(--border2) !important;
    border-radius:50px !important; padding:0.25rem 1rem !important;
    font-size:0.95rem !important; color:var(--text) !important;
    box-shadow:0 4px 20px var(--shadow) !important;
}
[data-testid="stTextInput"] > div > div input { color:var(--text) !important; font-family:'Quicksand',sans-serif !important; font-weight:500 !important; }
[data-testid="stTextInput"] > div > div input::placeholder { color:var(--muted) !important; }
[data-testid="stTextInput"] > div > div:focus-within { border-color:var(--lavender) !important; box-shadow:0 0 0 4px rgba(179,157,219,0.18),0 4px 20px var(--shadow) !important; }

[data-testid="baseButton-primary"] {
    background:linear-gradient(135deg,#ce93d8,#9b72cf) !important; border:none !important;
    border-radius:50px !important; font-family:'Quicksand',sans-serif !important;
    font-weight:600 !important; font-size:0.92rem !important; color:#fff !important;
    box-shadow:0 6px 20px rgba(155,114,207,0.35) !important;
}
[data-testid="baseButton-primary"]:hover { background:linear-gradient(135deg,#ba68c8,#7e57c2) !important; transform:translateY(-2px) !important; }

[data-testid="baseButton-secondary"] {
    background:var(--card) !important; border:1.5px solid var(--border2) !important;
    border-radius:50px !important; font-family:'Quicksand',sans-serif !important;
    font-weight:600 !important; font-size:0.88rem !important; color:var(--lav-text) !important;
}

/* ── Form elements ── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div {
    background:var(--card) !important; border:1.5px solid var(--border2) !important;
    border-radius:14px !important; color:var(--text) !important;
}
[data-testid="stNumberInput"] > div > div {
    background:var(--card) !important; border:1.5px solid var(--border2) !important;
    border-radius:14px !important;
}
label { color:var(--text2) !important; font-weight:600 !important; font-size:0.85rem !important; }

/* ── Footer ── */
.footer { text-align:center; color:var(--muted); font-size:0.75rem; margin-top:3rem; padding-bottom:2rem; letter-spacing:0.06em; }
.footer span { color:var(--pink); }
</style>
""", unsafe_allow_html=True)


# ─── Health condition rules ────────────────────────────────────────────────────
CONDITION_RULES = {
    "Diabetes": {
        "icon": "",
        "color": "tag-diabetes",
        "avoid_nutrients": {
            "sugar":         ("high",  50,  "Sugar should be minimal — spikes blood glucose"),
            "carbohydrates": ("high", 150,  "High carbs raise blood sugar significantly"),
            "calories":      ("high", 400,  "High-calorie foods contribute to weight gain & insulin resistance"),
        },
        "prefer_nutrients": ["fiber", "protein"],
        "avoid_keywords": ["sugar","syrup","candy","cake","cookie","juice","soda","honey","jam","sweet"],
        "prefer_keywords": ["vegetable","leafy","egg","fish","chicken","lentil","oat","quinoa"],
        "tip": "Choose low glycaemic foods. Prioritise fibre & lean protein. Limit refined carbs & added sugars."
    },
    "Hypertension": {
        "icon": "",
        "color": "tag-hypertension",
        "avoid_nutrients": {
            "sodium": ("high", 400, "Excess sodium raises blood pressure"),
        },
        "prefer_nutrients": ["potassium", "magnesium"],
        "avoid_keywords": ["salt","pickle","chips","processed","canned","sausage","bacon"],
        "prefer_keywords": ["banana","spinach","avocado","oat","fish","potato","yogurt"],
        "tip": "Follow a low-sodium diet (DASH). Boost potassium & magnesium through whole foods."
    },
    "Obesity": {
        "icon": "⚖️",
        "color": "tag-obesity",
        "avoid_nutrients": {
            "calories": ("high", 300, "High-calorie foods make a caloric deficit harder"),
            "fat":      ("high",  20, "High fat is calorie-dense (9 kcal/g)"),
            "sugar":    ("high",  15, "Added sugar contributes empty calories"),
        },
        "prefer_nutrients": ["fiber", "protein"],
        "avoid_keywords": ["fried","burger","pizza","cake","chips","fries","cream","chocolate"],
        "prefer_keywords": ["vegetable","fruit","salad","chicken","fish","egg","lentil","oat"],
        "tip": "Prioritise fibre and protein for satiety. Reduce calorie-dense, processed and high-fat foods."
    },
    "High Cholesterol": {
        "icon": "",
        "color": "tag-cholesterol",
        "avoid_nutrients": {
            "fat":   ("high", 15, "Saturated/trans fats raise LDL cholesterol"),
            "sugar": ("high", 20, "Excess sugar converts to triglycerides"),
        },
        "prefer_nutrients": ["fiber"],
        "avoid_keywords": ["butter","cream","cheese","fried","lard","bacon","sausage","red meat"],
        "prefer_keywords": ["oat","fish","avocado","olive","walnut","bean","lentil","spinach"],
        "tip": "Increase soluble fibre. Choose unsaturated fats. Limit saturated fats and added sugar."
    },
    "Kidney Disease": {
        "icon": "",
        "color": "tag-kidney",
        "avoid_nutrients": {
            "potassium":   ("high", 300, "Damaged kidneys can't filter excess potassium"),
            "phosphorus":  ("high", 150, "High phosphorus harms kidney function"),
            "sodium":      ("high", 300, "Sodium causes fluid retention, straining kidneys"),
            "protein":     ("high",  20, "High protein increases kidney filtration load"),
        },
        "prefer_nutrients": [],
        "avoid_keywords": ["banana","potato","tomato","avocado","dairy","nut","whole grain"],
        "prefer_keywords": ["apple","cabbage","cauliflower","blueberry","egg white","white rice"],
        "tip": "Limit potassium, phosphorus, sodium and protein. Work with a dietitian for a personalised plan."
    },
}

def assess_food(food, conditions):
    """
    Returns (status, reasons, safe_notes)
    status: 'danger' | 'warning' | 'safe'
    """
    if not conditions or conditions == ["None"]:
        return "safe", [], []

    danger_reasons  = []
    warning_reasons = []
    safe_notes      = []

    name_lower = food['name'].lower()

    for cond in conditions:
        if cond not in CONDITION_RULES:
            continue
        rules = CONDITION_RULES[cond]

        # keyword check
        for kw in rules["avoid_keywords"]:
            if kw in name_lower:
                danger_reasons.append(f"**{cond}** — '{food['name'].title()}' is typically high-risk for this condition.")
                break

        # nutrient threshold check
        for nutrient, (severity, threshold, reason) in rules["avoid_nutrients"].items():
            val = food.get(nutrient, 0) or 0
            if val > threshold:
                msg = f"**{cond}** — {reason} ({nutrient.title()}: {val:.1f})"
                if severity == "high":
                    danger_reasons.append(msg)
                else:
                    warning_reasons.append(msg)

        # preferred nutrients
        for nutrient in rules["prefer_nutrients"]:
            val = food.get(nutrient, 0) or 0
            if val > 3:
                safe_notes.append(f"Good source of {nutrient} — beneficial for **{cond}**")

    if danger_reasons:
        return "danger", danger_reasons, safe_notes
    elif warning_reasons:
        return "warning", warning_reasons, safe_notes
    else:
        return "safe", [], safe_notes


def get_recommendations(df, conditions, n=8):
    """Return top recommended foods for given conditions."""
    if not conditions or conditions == ["None"]:
        return df.sample(min(n, len(df)))

    scored = []
    for _, row in df.iterrows():
        score = 0
        status, _, _ = assess_food(row, conditions)
        if status == "danger":
            continue  # skip bad foods
        if status == "safe":
            score += 5
        for cond in conditions:
            if cond not in CONDITION_RULES:
                continue
            rules = CONDITION_RULES[cond]
            for kw in rules.get("prefer_keywords", []):
                if kw in row['name'].lower():
                    score += 3
            for nutrient in rules.get("prefer_nutrients", []):
                val = row.get(nutrient, 0) or 0
                if val > 2:
                    score += 2
        scored.append((score, row))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = [row for _, row in scored[:n]]
    return pd.DataFrame(top) if top else df.head(n)


# ─── Data ─────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    for path in ["datset.xlsx","dataset.xlsx","/Users/saivedhathota/Desktop/batch 8 iomp/datset.xlsx"]:
        if os.path.exists(path):
            return pd.read_excel(path)
    demo = [
        {"name":"apple","calories":95,"protein":0.5,"carbohydrates":25,"fat":0.3,"fiber":4.4,"sugar":19,"sodium":2,"potassium":195,"calcium":11,"iron":0.2,"magnesium":9,"vitamin_c":8.4},
        {"name":"banana","calories":105,"protein":1.3,"carbohydrates":27,"fat":0.4,"fiber":3.1,"sugar":14,"sodium":1,"potassium":422,"calcium":6,"iron":0.3,"magnesium":32,"vitamin_c":10.3},
        {"name":"chicken breast","calories":165,"protein":31,"carbohydrates":0,"fat":3.6,"fiber":0,"sugar":0,"sodium":74,"potassium":256,"calcium":15,"iron":0.9,"magnesium":29,"vitamin_c":0},
        {"name":"brown rice","calories":216,"protein":5,"carbohydrates":45,"fat":1.8,"fiber":3.5,"sugar":0,"sodium":10,"potassium":84,"calcium":20,"iron":1,"magnesium":84,"vitamin_c":0},
        {"name":"egg","calories":78,"protein":6,"carbohydrates":0.6,"fat":5,"fiber":0,"sugar":0.6,"sodium":62,"potassium":63,"calcium":28,"iron":0.9,"magnesium":6,"vitamin_c":0},
        {"name":"broccoli","calories":55,"protein":3.7,"carbohydrates":11,"fat":0.6,"fiber":5.1,"sugar":2.6,"sodium":64,"potassium":457,"calcium":62,"iron":0.7,"magnesium":25,"vitamin_c":89.2},
        {"name":"salmon","calories":208,"protein":20,"carbohydrates":0,"fat":13,"fiber":0,"sugar":0,"sodium":59,"potassium":363,"calcium":13,"iron":0.3,"magnesium":27,"vitamin_c":0},
        {"name":"oats","calories":307,"protein":11,"carbohydrates":55,"fat":5,"fiber":8,"sugar":1,"sodium":5,"potassium":335,"calcium":54,"iron":4,"magnesium":138,"vitamin_c":0},
        {"name":"avocado","calories":160,"protein":2,"carbohydrates":9,"fat":15,"fiber":7,"sugar":0.7,"sodium":7,"potassium":485,"calcium":12,"iron":0.6,"magnesium":29,"vitamin_c":10},
        {"name":"sweet potato","calories":103,"protein":2.3,"carbohydrates":24,"fat":0.1,"fiber":3.8,"sugar":7.4,"sodium":41,"potassium":438,"calcium":39,"iron":0.8,"magnesium":27,"vitamin_c":22.3},
        {"name":"almonds","calories":579,"protein":21,"carbohydrates":22,"fat":50,"fiber":12.5,"sugar":4.4,"sodium":1,"potassium":705,"calcium":264,"iron":3.7,"magnesium":270,"vitamin_c":0},
        {"name":"greek yogurt","calories":59,"protein":10,"carbohydrates":3.6,"fat":0.4,"fiber":0,"sugar":3.2,"sodium":36,"potassium":141,"calcium":110,"iron":0.1,"magnesium":11,"vitamin_c":0},
        {"name":"spinach","calories":23,"protein":2.9,"carbohydrates":3.6,"fat":0.4,"fiber":2.2,"sugar":0.4,"sodium":79,"potassium":558,"calcium":99,"iron":2.7,"magnesium":79,"vitamin_c":28.1},
        {"name":"whole milk","calories":149,"protein":8,"carbohydrates":12,"fat":8,"fiber":0,"sugar":12,"sodium":105,"potassium":349,"calcium":276,"iron":0.1,"magnesium":24,"vitamin_c":0},
        {"name":"orange","calories":62,"protein":1.2,"carbohydrates":15,"fat":0.2,"fiber":3.1,"sugar":12,"sodium":0,"potassium":237,"calcium":52,"iron":0.1,"magnesium":13,"vitamin_c":69.7},
        {"name":"lentils","calories":230,"protein":18,"carbohydrates":40,"fat":0.8,"fiber":15.6,"sugar":3.6,"sodium":4,"potassium":731,"calcium":37,"iron":6.6,"magnesium":71,"vitamin_c":4.4},
        {"name":"tuna","calories":128,"protein":28,"carbohydrates":0,"fat":1.2,"fiber":0,"sugar":0,"sodium":339,"potassium":229,"calcium":10,"iron":1.3,"magnesium":35,"vitamin_c":0},
        {"name":"quinoa","calories":222,"protein":8,"carbohydrates":39,"fat":3.5,"fiber":5,"sugar":1.6,"sodium":13,"potassium":318,"calcium":31,"iron":2.8,"magnesium":118,"vitamin_c":0},
        {"name":"pizza","calories":285,"protein":12,"carbohydrates":36,"fat":10,"fiber":2.3,"sugar":3.6,"sodium":640,"potassium":184,"calcium":188,"iron":2.6,"magnesium":23,"vitamin_c":2},
        {"name":"burger","calories":354,"protein":20,"carbohydrates":29,"fat":17,"fiber":1,"sugar":6,"sodium":497,"potassium":320,"calcium":96,"iron":2.8,"magnesium":28,"vitamin_c":1},
        {"name":"pasta","calories":220,"protein":8,"carbohydrates":43,"fat":1.3,"fiber":2.5,"sugar":0.6,"sodium":1,"potassium":58,"calcium":10,"iron":1.8,"magnesium":30,"vitamin_c":0},
        {"name":"carrot","calories":41,"protein":0.9,"carbohydrates":10,"fat":0.2,"fiber":2.8,"sugar":4.7,"sodium":69,"potassium":320,"calcium":33,"iron":0.3,"magnesium":12,"vitamin_c":5.9},
        {"name":"tomato","calories":18,"protein":0.9,"carbohydrates":3.9,"fat":0.2,"fiber":1.2,"sugar":2.6,"sodium":5,"potassium":237,"calcium":10,"iron":0.3,"magnesium":11,"vitamin_c":13.7},
        {"name":"white rice","calories":206,"protein":4.3,"carbohydrates":45,"fat":0.4,"fiber":0.6,"sugar":0,"sodium":2,"potassium":55,"calcium":16,"iron":1.9,"magnesium":19,"vitamin_c":0},
        {"name":"bread","calories":265,"protein":9,"carbohydrates":49,"fat":3.2,"fiber":2.7,"sugar":5,"sodium":491,"potassium":115,"calcium":151,"iron":3.6,"magnesium":25,"vitamin_c":0},
        {"name":"cake","calories":395,"protein":4,"carbohydrates":59,"fat":17,"fiber":0.9,"sugar":38,"sodium":290,"potassium":77,"calcium":40,"iron":1.2,"magnesium":12,"vitamin_c":0},
        {"name":"chocolate","calories":546,"protein":5,"carbohydrates":60,"fat":31,"fiber":3.4,"sugar":48,"sodium":24,"potassium":365,"calcium":56,"iron":3.1,"magnesium":58,"vitamin_c":0},
        {"name":"honey","calories":304,"protein":0.3,"carbohydrates":82,"fat":0,"fiber":0.2,"sugar":82,"sodium":4,"potassium":52,"calcium":6,"iron":0.4,"magnesium":2,"vitamin_c":0.5},
        {"name":"cabbage","calories":25,"protein":1.3,"carbohydrates":6,"fat":0.1,"fiber":2.5,"sugar":3.2,"sodium":18,"potassium":170,"calcium":40,"iron":0.5,"magnesium":12,"vitamin_c":36.6},
        {"name":"cauliflower","calories":25,"protein":1.9,"carbohydrates":5,"fat":0.3,"fiber":2,"sugar":1.9,"sodium":30,"potassium":299,"calcium":22,"iron":0.4,"magnesium":15,"vitamin_c":48.2},
    ]
    return pd.DataFrame(demo)


@st.cache_data(show_spinner=False)
def preprocess_data(df):
    df = df.copy()
    df.columns = (df.columns.str.strip().str.lower()
                  .str.replace(r'[^a-z0-9_]','_',regex=True)
                  .str.replace(r'__+','_',regex=True))
    for src,dst in [('carbs','carbohydrates'),('carbohydrate','carbohydrates'),
                    ('sugars','sugar'),('vitamin c','vitamin_c'),('calorie','calories')]:
        if src in df.columns and dst not in df.columns:
            df[dst] = df[src]
    for drop_col in ['unnamed_0','saturated_fat']:
        if drop_col in df.columns:
            df.drop(drop_col, axis=1, inplace=True)
    for col in df.columns:
        if col != 'name':
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(r'[^0-9.]','',regex=True), errors='coerce')
    df['name'] = df['name'].apply(lambda t: re.sub(r'[^a-zA-Z ]','',str(t).lower()).strip())
    df.dropna(subset=['name'], inplace=True)
    return df


def fuzzy_search(query, df, top_k=5):
    q = re.sub(r'[^a-zA-Z ]','',query.lower()).strip()
    names = df['name'].str.lower()
    exact = df[names == q]
    if not exact.empty: return exact.iloc[0], df[names != q].head(top_k-1)
    sw = df[names.str.startswith(q)]
    if not sw.empty: return sw.iloc[0], df[(names != sw.iloc[0]['name']) & names.str.contains(q,na=False)].head(top_k-1)
    ct = df[names.str.contains(q,na=False)]
    if not ct.empty: return ct.iloc[0], ct.iloc[1:top_k]
    q_tokens = set(q.split())
    scores = names.apply(lambda n: len(q_tokens & set(n.split())))
    best_idx = scores.idxmax()
    if scores[best_idx] > 0: return df.loc[best_idx], df[scores > 0].drop(best_idx).head(top_k-1)
    return None, pd.DataFrame()


def calorie_category(cal):
    if cal < 100: return "low","Low Calorie"
    elif cal < 300: return "medium","Moderate"
    else: return "high","High Calorie"


def progress_bar(label, value, max_val, grad):
    pct = min(100,(value/max_val)*100) if max_val > 0 else 0
    return f"""<div class="bar-wrap">
        <div class="bar-meta"><span>{label}</span><span>{value:.1f} g</span></div>
        <div class="bar-bg"><div class="bar-fill" style="width:{pct:.1f}%;background:{grad};"></div></div>
    </div>"""


def bmi_category(bmi):
    if bmi < 18.5: return "Underweight "
    elif bmi < 25: return "Normal "
    elif bmi < 30: return "Overweight "
    else: return "Obese "


# ─── Session state defaults ────────────────────────────────────────────────────
if "profile_saved" not in st.session_state:
    st.session_state.profile_saved = False
if "profile" not in st.session_state:
    st.session_state.profile = {}

# ─── Load data ─────────────────────────────────────────────────────────────────
with st.spinner("Loading…"):
    df_raw = load_data()
    df     = preprocess_data(df_raw)

# ─── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <span class="hero-icon">🍲</span>
    <h1>NutriTrack</h1>
    <p>your personalised nutritional companion</p>
    <div class="hero-dots">
        <span class="dot" style="background:#f2a7c3;"></span>
        <span class="dot" style="background:#ce93d8;"></span>
        <span class="dot" style="background:#b39ddb;"></span>
        <span class="dot" style="background:#9fa8da;"></span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([" My Profile", "Search Food", " Recommendations"])

# ══════════════════════════════════════════════════════════════════════
# TAB 1 — PROFILE
# ══════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)

    p = st.session_state.profile

    # Show saved profile banner
    if st.session_state.profile_saved and p:
        bmi = p.get("bmi", 0)
        conds = p.get("conditions", ["None"])
        cond_tags = "".join(
            f'<span class="condition-tag {CONDITION_RULES[c]["color"]}">{CONDITION_RULES[c]["icon"]} {c}</span>'
            if c in CONDITION_RULES else
            f'<span class="condition-tag tag-none"> No conditions</span>'
            for c in conds
        )
        st.markdown(f"""
        <div class="profile-banner">
            <div class="profile-avatar"></div>
            <div>
                <div class="profile-name">{p.get('name','User')}</div>
                <div class="profile-meta">
                    {p.get('age','')} yrs &nbsp;·&nbsp;
                    {p.get('weight','')} kg &nbsp;·&nbsp;
                    {p.get('height','')} cm &nbsp;·&nbsp;
                    BMI {bmi:.1f} — {bmi_category(bmi)}
                </div>
                <div class="condition-tags">{cond_tags}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Profile form
    with st.container():
        st.markdown('<div class="nutri-card">', unsafe_allow_html=True)
        st.markdown("###  Your Profile")

        c1, c2 = st.columns(2)
        with c1:
            name   = st.text_input("Full Name", value=p.get("name",""), placeholder="")
            age    = st.number_input("Age", min_value=1, max_value=120, value=int(p.get("age",22)))
            weight = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, value=float(p.get("weight",60.0)), step=0.5)
        with c2:
            gender = st.selectbox("Gender", ["Female","Male","Other"], index=["Female","Male","Other"].index(p.get("gender","Female")))
            height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=float(p.get("height",165.0)), step=0.5)
            goal   = st.selectbox("Health Goal", ["Stay Healthy","Lose Weight","Gain Muscle","Manage Condition"],
                                  index=["Stay Healthy","Lose Weight","Gain Muscle","Manage Condition"].index(p.get("goal","Stay Healthy")))

        all_conditions = list(CONDITION_RULES.keys())
        conditions = st.multiselect(
            "Health Conditions (select all that apply)",
            options=all_conditions,
            default=[c for c in p.get("conditions",[]) if c in all_conditions],
            placeholder="Select conditions…"
        )
        if not conditions:
            conditions = ["None"]

        notes = st.text_area("Additional notes (optional)", value=p.get("notes",""), placeholder="e.g. lactose intolerant, vegetarian…", height=80)

        st.markdown('</div>', unsafe_allow_html=True)

        if st.button(" Save Profile", type="primary", use_container_width=True):
            bmi = weight / ((height/100)**2) if height > 0 else 0
            st.session_state.profile = {
                "name": name, "age": age, "weight": weight,
                "height": height, "gender": gender, "goal": goal,
                "conditions": conditions, "notes": notes, "bmi": bmi
            }
            st.session_state.profile_saved = True
            st.success(f"✨ Profile saved! Welcome, {name}!")
            st.rerun()

    # Tips per condition
    if st.session_state.profile_saved and p.get("conditions"):
        for cond in p["conditions"]:
            if cond in CONDITION_RULES:
                r = CONDITION_RULES[cond]
                st.markdown(f"""
                <div class="nutri-card" style="border-left:4px solid var(--lavender);">
                    <h3>{r['icon']} {cond} — Dietary Guidance</h3>
                    <p style="color:var(--text2);font-size:0.88rem;line-height:1.7;margin:0;">{r['tip']}</p>
                </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# TAB 2 — SEARCH
# ══════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)

    conditions = st.session_state.profile.get("conditions", ["None"]) if st.session_state.profile_saved else ["None"]

    col1, col2 = st.columns([4,1])
    with col1:
        query = st.text_input("", placeholder="  Search — apple, oats, salmon…", label_visibility="collapsed", key="search_input")
    with col2:
        search_btn = st.button("Track", type="primary", use_container_width=True)

    suggestions = ["🍎 Apple","🥚 Egg","🍌 Banana","🐟 Salmon","🥑 Avocado","🥦 Broccoli"]
    st.markdown('<div class="chip-row">'+''.join(f'<span class="chip">{s}</span>' for s in suggestions)+'</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if not st.session_state.profile_saved:
        st.markdown("""
        <div class="alert-banner warning">
            <div class="alert-icon"></div>
            <div>
                <div class="alert-title alert-warning-title">Set up your profile first!</div>
                <div class="alert-body">Go to <b>My Profile</b> tab and save your health conditions for personalised food assessments.</div>
            </div>
        </div>""", unsafe_allow_html=True)

    if query or search_btn:
        food, similar = fuzzy_search(query, df)

        if food is None:
            st.markdown(f"""
            <div class="not-found">
                <div class="icon"></div>
                <h3>No results for "{query}"</h3>
                <p>Try a different spelling or pick a suggestion above!</p>
            </div>""", unsafe_allow_html=True)
        else:
            name_display = food['name'].title()
            cal   = food.get('calories',0) or 0
            prot  = food.get('protein',0) or 0
            carb  = food.get('carbohydrates',0) or 0
            fat   = food.get('fat',0) or 0
            fiber = food.get('fiber',0) or 0
            sugar = food.get('sugar',0) or 0
            cat_cls, cat_label = calorie_category(cal)

            # ── Health assessment alert ──
            status, reasons, safe_notes = assess_food(food, conditions)

            if status == "danger" and conditions != ["None"]:
                reason_list = "".join(f"<li>{r}</li>" for r in reasons)
                st.markdown(f"""
                <div class="alert-banner danger">
                    <div class="alert-icon">⚠️</div>
                    <div>
                        <div class="alert-title alert-danger-title">Not recommended for your health profile</div>
                        <div class="alert-body"><ul style="margin:0.3rem 0 0;padding-left:1.2rem;">{reason_list}</ul></div>
                    </div>
                </div>""", unsafe_allow_html=True)
            elif status == "warning" and conditions != ["None"]:
                reason_list = "".join(f"<li>{r}</li>" for r in reasons)
                st.markdown(f"""
                <div class="alert-banner warning">
                    <div class="alert-icon"></div>
                    <div>
                        <div class="alert-title alert-warning-title">Consume with caution</div>
                        <div class="alert-body"><ul style="margin:0.3rem 0 0;padding-left:1.2rem;">{reason_list}</ul></div>
                    </div>
                </div>""", unsafe_allow_html=True)
            elif status == "safe" and conditions != ["None"]:
                notes_list = "".join(f"<li>{n}</li>" for n in safe_notes) if safe_notes else "<li>No red flags detected for your conditions.</li>"
                st.markdown(f"""
                <div class="alert-banner safe">
                    <div class="alert-icon">✅</div>
                    <div>
                        <div class="alert-title alert-safe-title">Safe for your health profile</div>
                        <div class="alert-body"><ul style="margin:0.3rem 0 0;padding-left:1.2rem;">{notes_list}</ul></div>
                    </div>
                </div>""", unsafe_allow_html=True)

            # ── Determine flagged tiles ──
            flagged = set()
            for cond in conditions:
                if cond in CONDITION_RULES:
                    for nutrient, (_, threshold, _) in CONDITION_RULES[cond]["avoid_nutrients"].items():
                        val = food.get(nutrient, 0) or 0
                        if val > threshold:
                            flagged.add(nutrient)

            def tile_class(base, nutrient):
                return f"{base} flagged" if nutrient in flagged else base

            # ── Macro card ──
            st.markdown(f"""
            <div class="nutri-card">
                <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:1.3rem;flex-wrap:wrap;gap:0.5rem;">
                    <div>
                        <div class="section-pill">per 100 g serving</div>
                        <div class="food-name">{name_display}</div>
                    </div>
                    <span class="cal-badge {cat_cls}">{cat_label}</span>
                </div>
                <div class="macro-grid">
                    <div class="macro-tile {tile_class('cal','calories')}">
                        <div class="macro-val">{cal:.0f}</div><div class="macro-unit">KCAL</div><div class="macro-label">Calories</div>
                    </div>
                    <div class="macro-tile {tile_class('prot','protein')}">
                        <div class="macro-val">{prot:.1f}</div><div class="macro-unit">G</div><div class="macro-label">Protein</div>
                    </div>
                    <div class="macro-tile {tile_class('carb','carbohydrates')}">
                        <div class="macro-val">{carb:.1f}</div><div class="macro-unit">G</div><div class="macro-label">Carbs</div>
                    </div>
                    <div class="macro-tile {tile_class('fat','fat')}">
                        <div class="macro-val">{fat:.1f}</div><div class="macro-unit">G</div><div class="macro-label">Fat</div>
                    </div>
                    <div class="macro-tile {tile_class('fib','fiber')}">
                        <div class="macro-val">{fiber:.1f}</div><div class="macro-unit">G</div><div class="macro-label">Fiber</div>
                    </div>
                    <div class="macro-tile {tile_class('sug','sugar')}">
                        <div class="macro-val">{sugar:.1f}</div><div class="macro-unit">G</div><div class="macro-label">Sugar</div>
                    </div>
                </div>
                {"<p style='font-size:0.75rem;color:#c62828;margin:0.4rem 0 0;'>⚠️ Highlighted tiles exceed recommended thresholds for your conditions.</p>" if flagged and conditions != ['None'] else ""}
            </div>""", unsafe_allow_html=True)

            # ── Bars ──
            if prot*4 + carb*4 + fat*9 > 0:
                st.markdown('<div class="nutri-card"><h3>Macro Breakdown</h3>', unsafe_allow_html=True)
                st.markdown(progress_bar("Protein",       prot,  50,  "linear-gradient(90deg,#f48fb1,#ce93d8)"), unsafe_allow_html=True)
                st.markdown(progress_bar("Carbohydrates", carb,  100, "linear-gradient(90deg,#b39ddb,#9fa8da)"), unsafe_allow_html=True)
                st.markdown(progress_bar("Fat",           fat,   80,  "linear-gradient(90deg,#f2a7c3,#f48fb1)"), unsafe_allow_html=True)
                st.markdown(progress_bar("Fiber",         fiber, 30,  "linear-gradient(90deg,#a5d6a7,#80cbc4)"), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # ── Micros ──
            micro_cols = {
                'sodium':('Sodium','mg'),'potassium':('Potassium','mg'),
                'calcium':('Calcium','mg'),'iron':('Iron','mg'),
                'magnesium':('Magnesium','mg'),'vitamin_c':('Vitamin C','mg'),
                'vitamin_a':('Vitamin A','IU'),'zinc':('Zinc','mg'),
            }
            available = {k:v for k,v in micro_cols.items() if k in food.index and pd.notna(food[k]) and food[k]!=0}
            if available:
                rows = "".join(f"<tr><td>{lbl}</td><td>{food[k]:.1f} {unit}</td></tr>" for k,(lbl,unit) in available.items())
                st.markdown(f'<div class="nutri-card"><h3> Micronutrients</h3><table class="micro-table"><tbody>{rows}</tbody></table></div>', unsafe_allow_html=True)

            # ── Daily values ──
            st.markdown(f"""
            <div class="nutri-card">
                <h3>Daily Value Reference <span style="font-size:0.7rem;color:var(--muted);font-weight:400;">based on 2000 kcal</span></h3>
                <table class="micro-table"><tbody>
                    <tr><td>Calories</td><td>{round((cal/2000)*100)}%</td></tr>
                    <tr><td>Protein</td><td>{round((prot/50)*100)}%</td></tr>
                    <tr><td>Carbohydrates</td><td>{round((carb/275)*100)}%</td></tr>
                    <tr><td>Fat</td><td>{round((fat/78)*100)}%</td></tr>
                </tbody></table>
            </div>""", unsafe_allow_html=True)

            if not similar.empty:
                chips = "".join(f'<span class="chip"> {r["name"].title()}</span>' for _,r in similar.iterrows())
                st.markdown(f'<div class="nutri-card"><h3> You might also like</h3><div class="chip-row">{chips}</div></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# TAB 3 — RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)

    if not st.session_state.profile_saved:
        st.markdown("""
        <div class="alert-banner warning">
            <div class="alert-icon"></div>
            <div>
                <div class="alert-title alert-warning-title">Profile needed!</div>
                <div class="alert-body">Please complete your profile in the <b>My Profile</b> tab to get personalised recommendations.</div>
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        p = st.session_state.profile
        conditions = p.get("conditions", ["None"])
        user_name  = p.get("name","there")

        st.markdown(f"""
        <div class="nutri-card" style="background:linear-gradient(135deg,#f3e5f5,#ede7f6);border-color:var(--border2);">
            <h3 style="margin-bottom:0.5rem;">Hi, {user_name}!</h3>
            <p style="color:var(--text2);font-size:0.88rem;margin:0;line-height:1.6;">
                Here are foods <b>recommended for you</b> based on your health profile.
                {"Your conditions: <b>" + ", ".join([c for c in conditions if c != 'None']) + "</b>" if conditions != ["None"] else "No specific conditions — showing generally healthy options."}
            </p>
        </div>""", unsafe_allow_html=True)

        recs = get_recommendations(df, conditions, n=10)

        if recs.empty:
            st.markdown('<div class="not-found"><div class="icon">🌷</div><h3>No recommendations found</h3><p>Try adjusting your health conditions.</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="nutri-card"><h3>🌿 Best Foods For You</h3>', unsafe_allow_html=True)
            for _, row in recs.iterrows():
                food_status, _, food_safe = assess_food(row, conditions)
                badge_cls  = "great" if food_status == "safe"    else ("ok" if food_status == "warning" else "avoid")
                badge_text = "✅ Great pick" if food_status == "safe" else ("⚠️ In moderation" if food_status == "warning" else "❌ Avoid")
                cal   = row.get('calories',0) or 0
                prot  = row.get('protein',0) or 0
                fiber = row.get('fiber',0) or 0
                sugar = row.get('sugar',0) or 0
                st.markdown(f"""
                <div class="rec-food-card">
                    <div>
                        <div class="rec-food-name">🌱 {row['name'].title()}</div>
                        <div class="rec-food-meta">{cal:.0f} kcal &nbsp;·&nbsp; {prot:.1f}g protein &nbsp;·&nbsp; {fiber:.1f}g fiber &nbsp;·&nbsp; {sugar:.1f}g sugar</div>
                    </div>
                    <span class="rec-badge {badge_cls}">{badge_text}</span>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── What to avoid ──
        if conditions != ["None"]:
            st.markdown('<div class="nutri-card"><h3>🚫 Foods to Limit or Avoid</h3>', unsafe_allow_html=True)
            avoid_count = 0
            for _, row in df.iterrows():
                status, reasons, _ = assess_food(row, conditions)
                if status == "danger":
                    reason_text = reasons[0] if reasons else ""
                    st.markdown(f"""
                    <div class="rec-food-card">
                        <div>
                            <div class="rec-food-name">⛔ {row['name'].title()}</div>
                            <div class="rec-food-meta">{reason_text}</div>
                        </div>
                        <span class="rec-badge avoid">❌ Avoid</span>
                    </div>""", unsafe_allow_html=True)
                    avoid_count += 1
                    if avoid_count >= 6:
                        break
            if avoid_count == 0:
                st.markdown('<p style="color:var(--muted);font-size:0.88rem;">No specific foods to flag — great!</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ──
st.markdown("""
<div class="footer">
    made with <span>♥</span> · NutriTrack · not a substitute for medical advice · values per 100 g
</div>""", unsafe_allow_html=True)
