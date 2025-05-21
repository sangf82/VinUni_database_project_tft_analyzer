import os
import re
import bcrypt
import requests
import streamlit as st
import mysql.connector

# Set page config FIRST
st.set_page_config(page_title="TFT Stats Portal", page_icon="🎮")

DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "port":     int(os.getenv("DB_PORT", 3306)),
    "user":     os.getenv("DB_USER", "sanglt"),
    "password": os.getenv("DB_PASSWORD", "123456"),
    "database": os.getenv("DB_NAME", "tft_app"),
}

RIOT_KEY = os.getenv("RIOT_API_KEY")
HEADERS  = {"X-Riot-Token": RIOT_KEY}
REGION   = "vn2"

RIOTID_PATTERN = re.compile(r"^[A-Za-z0-9]{1,16}#[A-Za-z0-9]{4}$")

def get_conn():
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_CONFIG['database']}`;")
        conn.database = DB_CONFIG["database"]
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            name       VARCHAR(50) PRIMARY KEY,
            riotid     VARCHAR(21) NOT NULL,
            pw_hash    VARBINARY(60) NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        conn.commit()
    except mysql.connector.Error as e:
        st.error(f"❌ Database error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_user(name):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT riotid, pw_hash FROM users WHERE name=%s",
        (name,)
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return {"riotid": row[0], "pw_hash": row[1]}
    return None

def create_user(name, riotid, pw_plain):
    pw_hash = bcrypt.hashpw(pw_plain.encode(), bcrypt.gensalt())
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, riotid, pw_hash) VALUES (%s,%s,%s)",
        (name, riotid, pw_hash)
    )
    conn.commit()
    cursor.close()
    conn.close()

@st.cache_data(ttl=600)
def fetch_tft_stats(riotid):
    summoner_name = riotid.split("#")[0]
    url1 = f"https://{REGION}.api.riotgames.com/tft/summoner/v1/summoners/by-name/{summoner_name}"
    r1 = requests.get(url1, headers=HEADERS)
    if r1.status_code != 200:
        return None
    enc_id = r1.json()["id"]
    url2 = f"https://{REGION}.api.riotgames.com/tft/league/v1/entries/by-summoner/{enc_id}"
    r2 = requests.get(url2, headers=HEADERS)
    return r2.json()

init_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    choice = st.sidebar.radio("🔐", ["Sign Up", "Login"])
    with st.form(choice):
        name = st.text_input("Username (sign-in name)")
        if choice == "Sign Up":
            riotid = st.text_input("Your Riot ID (format: username#1234)")
            pw = st.text_input("Set a password", type="password")
            submitted = st.form_submit_button("Create Account")
            if submitted:
                if not name:
                    st.error("Please enter a username.")
                elif not riotid or not RIOTID_PATTERN.match(riotid):
                    st.error("Please enter a valid Riot ID in format username#1234 (tag must be exactly 4 letters/digits).")
                elif not pw:
                    st.error("Please enter a password.")
                elif get_user(name):
                    st.error("Username already taken.")
                else:
                    try:
                        create_user(name, riotid, pw)
                        st.success("Account created! Please switch to Login.")
                    except Exception as e:
                        st.error(f"Failed to create user: {e}")
        else:
            pw = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Log In")
            if submitted:
                try:
                    u = get_user(name)
                    if u and bcrypt.checkpw(pw.encode(), u["pw_hash"]):
                        st.session_state.logged_in = True
                        st.session_state.user = name
                        st.experimental_rerun()
                    else:
                        st.error("Invalid username or password.")
                except Exception as e:
                    st.error(f"Login error: {e}")

else:
    st.sidebar.success(f"Logged in as **{st.session_state.user}**")
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.experimental_rerun()

    user = get_user(st.session_state.user)
    st.title(f"TFT Stats for {user['riotid']}")
    stats = fetch_tft_stats(user["riotid"])
    if not stats:
        st.warning("Couldn’t fetch stats. Check your Riot ID or API key.")
    else:
        for e in stats:
            st.markdown(f"**{e['queueType']}** — Tier {e['tier']} {e['rank']} ({e['leaguePoints']} LP)")
            st.markdown(f"W: {e['wins']} • L: {e['losses']}")
            st.markdown("---")
