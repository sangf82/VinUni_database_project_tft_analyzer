import streamlit as st
import json
import pandas as pd
from collections import Counter
from st_on_hover_tabs import on_hover_tabs

st.set_page_config(layout="wide")

st.header("Custom tab component for on-hover navigation bar")
import os

css_path = './style.css'
if os.path.exists(css_path):
    with open(css_path, 'r') as f:
        st.markdown('<style>' + f.read() + '</style>', unsafe_allow_html=True)
else:
    st.warning(f"CSS file '{css_path}' not found. Skipping custom styles.")


with st.sidebar:
    with st.sidebar:
        tabs = on_hover_tabs(tabName=['Dashboard', 'Money', 'Economy'], 
                             iconName=['dashboard', 'money', 'economy'],
                             styles = {'navtab': {'background-color':'#111',
                                                  'color': '#818181',
                                                  'font-size': '18px',
                                                  'transition': '.3s',
                                                  'white-space': 'nowrap',
                                                  'text-transform': 'uppercase'},
                                       'tabStyle': {':hover :hover': {'color': 'red',
                                                                      'cursor': 'pointer'}},
                                       'tabStyle' : {'list-style-type': 'none',
                                                     'margin-bottom': '30px',
                                                     'padding-left': '30px'},
                                       'iconStyle':{'position':'fixed',
                                                    'left':'7.5px',
                                                    'text-align': 'left'},
                                       },
                             key="1")

if tabs =='Dashboard':
    st.title("Navigation Bar")
    st.write('Name of option is {}'.format(tabs))

elif tabs == 'Money':
    st.title("Paper")
    st.write('Name of option is {}'.format(tabs))

elif tabs == 'Economy':
    st.title("Tom")
    st.write('Name of option is {}'.format(tabs))

# Load JSON data
with open("stat.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Title and summoner info
st.title(f"TFT Player Overview - {data['summoner']['riot_id']}")

ranked = data.get("ranked", {})
st.subheader("Current Rank")
st.write(f"Rank: {ranked.get('rating_text', 'N/A')}")
st.write(f"Peak Rank: {ranked.get('peak_rating', 'N/A')}")
st.write(f"Number of Games: {ranked.get('num_games', 'N/A')}")

# Ranked rating history plot
rank_changes = data.get("ranked_rating_changes", [])
if rank_changes:
    df = pd.DataFrame(rank_changes)
    df['created_timestamp'] = pd.to_datetime(df['created_timestamp'])
    df = df.sort_values('created_timestamp')
    df['rating_numeric_inv'] = -df['rating_numeric']  # invert to show "rank up" visually

    st.subheader("Rank Rating Over Time")
    st.line_chart(df.set_index('created_timestamp')['rating_numeric_inv'])
else:
    st.write("No rank history available.")

# Calculate win rate and top champions from matches
matches = data.get("matches", [])
if matches:
    total_matches = len(matches)
    wins = sum(1 for m in matches if m.get("placement") == 1)
    win_rate = wins / total_matches * 100
    st.subheader(f"Win Rate (Last {total_matches} matches): {win_rate:.2f}%")

    champ_counter = Counter()
    for match in matches:
        units = match.get("summary", {}).get("units", [])
        for unit in units:
            champ_id = unit.get("character_id")
            if champ_id:
                champ_counter[champ_id] += 1

    top_champs = champ_counter.most_common(3)
    st.subheader("Top 3 Most Picked Champions")
    for champ, count in top_champs:
        st.write(f"{champ}: {count} times")
else:
    st.write("No match data available.")
    

