import os
import time
import datetime
import re
import bcrypt
import requests
import streamlit as st
import mysql.connector
import pandas as pd
import altair as alt
from dotenv import load_dotenv

# ─── Load environment variables ───────────────────────────────────────────────
load_dotenv()
DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "port":     int(os.getenv("DB_PORT", 3306)),
    "user":     os.getenv("DB_USER", ""),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "tft_app"),
}
RIOT_KEY = os.getenv("RIOT_API_KEY")
HEADERS   = {"X-Riot-Token": RIOT_KEY}
MATCH_REGION = "sea.api.riotgames.com"
SUMMONER_REGION = "vn2.api.riotgames.com"

# Regex for Riot ID format username#1234
RIOTID_REGEX = re.compile(r"^.+#[A-Za-z0-9]{1,10}$")

# ─── Database initialization ─────────────────────────────────────────────────
def get_conn():
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    conn = None
    cur = None
    try:
        # Connect without selecting DB to create it first
        temp_conf = DB_CONFIG.copy()
        temp_conf.pop("database")
        conn = mysql.connector.connect(**temp_conf)
        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_CONFIG['database']}`;")
        conn.database = DB_CONFIG["database"]
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
          name       VARCHAR(50) PRIMARY KEY,
          pw_hash    VARBINARY(60) NOT NULL,
          nameGame   VARCHAR(50) NOT NULL,
          tagLine    VARCHAR(10) NOT NULL,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        conn.commit()
    except mysql.connector.Error as e:
        st.error(f"Database error: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# ─── User management ─────────────────────────────────────────────────────────
def create_user(username, riotid, password_plain):
    # Split riotid into nameGame and tagLine
    nameGame, tagLine = riotid.split("#")
    pw_hash = bcrypt.hashpw(password_plain.encode(), bcrypt.gensalt())
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, pw_hash, nameGame, tagLine) VALUES (%s,%s,%s,%s)",
        (username, pw_hash, nameGame, tagLine)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_user(username):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT pw_hash, nameGame, tagLine FROM users WHERE name=%s", (username,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return {"pw_hash": row[0], "nameGame": row[1], "tagLine": row[2]}
    return None

# ─── Riot API calls ───────────────────────────────────────────────────────────
@st.cache_data(ttl=600)
def fetch_riotid(nameGame, tagLine):
    r = requests.get(
        f"https://{SUMMONER_REGION}/lol/summoner/v4/summoners/by-name/{nameGame}#{tagLine}",
        headers=HEADERS
    )
    if r.status_code == 200:
        return r.json()
    return None

def fetch_matches(puuid):
    now = int(time.time())
    month_ago = now - 30*24*3600
    url = (f"https://{MATCH_REGION}/lol/match/v5/matches/by-puuid/{puuid}" 
           f"?startTime={month_ago}&endTime={now}&count=50")
    return requests.get(url, headers=HEADERS).json()

@st.cache_data(ttl=600)
def fetch_match_detail(match_id):
    r = requests.get(f"https://{MATCH_REGION}/lol/match/v5/matches/{match_id}", headers=HEADERS)
    return r.json()

@st.cache_data(ttl=600)
def fetch_rank(summoner_id):
    url = f"https://{SUMMONER_REGION}/lol/league/v4/entries/by-summoner/{summoner_id}"
    return requests.get(url, headers=HEADERS).json()

# ─── Streamlit App UI ────────────────────────────────────────────────────────
st.set_page_config(page_title="Riot Dashboard", page_icon="🎮", layout="wide")
init_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Authentication screens
if not st.session_state.logged_in:
    choice = st.sidebar.selectbox("Action", ["Sign Up", "Login"])
    with st.form(key=choice):
        username = st.text_input("Username")
        if choice == "Sign Up":
            riotid = st.text_input("Riot ID (e.g. adamgreen#0776)")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Create Account")
            if submitted:
                if not username:
                    st.error("Username is required.")
                elif not RIOTID_REGEX.match(riotid):
                    st.error("Riot ID must be in format username#1234.")
                elif not password:
                    st.error("Password is required.")
                elif get_user(username):
                    st.error("Username already exists.")
                else:
                    create_user(username, riotid, password)
                    st.success("Account created! Please log in.")
        else:
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Log In")
            if submitted:
                user = get_user(username)
                if user and bcrypt.checkpw(password.encode(), user["pw_hash"]):
                    st.session_state.logged_in = True
                    st.session_state.user = username
                    st.experimental_rerun()
                else:
                    st.error("Invalid username or password.")

# Main dashboard
else:
    st.sidebar.success(f"Logged in as: {st.session_state.user}")
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.experimental_rerun()

    # Get stored nameGame and tagLine
    user = get_user(st.session_state.user)
    nameGame = user["nameGame"]
    tagLine = user["tagLine"]
    st.title(f"📊 Dashboard for {nameGame}#{tagLine}")

    # Fetch latest summoner info
    summ = requests.get(
        f"https://{SUMMONER_REGION}/lol/summoner/v4/summoners/by-name/{nameGame}",
        headers=HEADERS
    ).json()
    puuid     = summ["puuid"]
    summoner_id = summ["id"]

    # Fetch matches and stats
    match_ids = fetch_matches(puuid)
    details   = [fetch_match_detail(m) for m in match_ids]
    rank_data = fetch_rank(summoner_id)

    # Process stats
    rows = []
    champ_counts = {}
    wins = 0
    for m in details:
        part = next(p for p in m["info"]["participants"] if p["puuid"] == puuid)
        placement = part.get("placement", 1 if part.get("win") else 8)
        rows.append({
            "time": datetime.datetime.fromtimestamp(m["info"]["gameStartTimestamp"]/1000),
            "placement": placement
        })
        if part.get("win"): wins += 1
        champ = part.get("championName")
        champ_counts[champ] = champ_counts.get(champ, 0) + 1

    df = pd.DataFrame(rows).sort_values("time")
    total = len(rows)
    win_rate = (wins / total * 100) if total else 0
    top3 = dict(sorted(champ_counts.items(), key=lambda x: -x[1])[:3])

    # Layout metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Matches (30d)", total)
    c2.metric("Win Rate", f"{win_rate:.1f}%")
    c3.metric("Top Champ", list(top3.keys())[0] if top3 else "N/A")

    # Charts
    st.subheader("Match Placement Over Time")
    line = alt.Chart(df).mark_line(point=True).encode(
        x="time:T",
        y=alt.Y("placement:Q", sort="descending")
    ).properties(height=300)
    st.altair_chart(line, use_container_width=True)

    st.subheader("Win vs Loss")
    pie_data = pd.DataFrame({"Result": ["Win", "Loss"], "Count": [wins, total - wins]})
    st.altair_chart(alt.Chart(pie_data).mark_arc().encode(theta="Count:Q", color="Result:N"),
                     use_container_width=True)

    st.subheader("Top 3 Champions")
    bar_data = pd.DataFrame({"Champion": list(top3.keys()), "Picks": list(top3.values())})
    st.altair_chart(
        alt.Chart(bar_data).mark_bar().encode(x="Champion:N", y="Picks:Q", tooltip=["Champion","Picks"]),
        use_container_width=True
    )
