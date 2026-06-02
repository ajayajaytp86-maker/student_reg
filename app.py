import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import random

st.set_page_config(
    page_title="Game of Thrones 3D Throne",
    page_icon="🗡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

page_style = """
<style>
body {
    background: radial-gradient(circle at top left, #1f1b24 0%, #07050a 60%);
    color: #f2f2f2;
}
.main .block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
}
.card {
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    background: rgba(20, 18, 25, 0.88);
    box-shadow: 0 0 40px rgba(0,0,0,0.35);
    padding: 24px;
}
.glow-title {
    color: #ffdd66;
    text-shadow: 0 0 20px rgba(255, 221, 102, 0.45);
}
.throne-panel {
    background: linear-gradient(180deg, rgba(22,16,16,0.95), rgba(10,7,8,0.95));
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 24px;
    padding: 22px;
    margin-bottom: 1rem;
}
</style>
"""
st.markdown(page_style, unsafe_allow_html=True)

st.markdown("<h1 class='glow-title'>The Iron Throne 3D Command Center</h1>", unsafe_allow_html=True)
st.markdown(
    "Welcome to the most advanced Westeros dashboard. Explore Houses, inspect champions, and watch the throne's power grid in 3D."
)

houses = {
    "Stark": {"motto": "Winter Is Coming", "sigil": "🐺", "strength": 82, "wealth": 65, "loyalty": 90, "region": "The North", "members": ["Jon Snow", "Sansa Stark", "Arya Stark", "Bran Stark"], "dragons": 0},
    "Lannister": {"motto": "Hear Me Roar!", "sigil": "🦁", "strength": 78, "wealth": 95, "loyalty": 72, "region": "The Westerlands", "members": ["Cersei Lannister", "Jaime Lannister", "Tyrion Lannister"], "dragons": 0},
    "Targaryen": {"motto": "Fire and Blood", "sigil": "🐉", "strength": 88, "wealth": 80, "loyalty": 76, "region": "Dragonstone", "members": ["Daenerys Targaryen", "Jon Snow", "Viserys Targaryen"], "dragons": 3},
    "Baratheon": {"motto": "Ours is the Fury", "sigil": "🦌", "strength": 80, "wealth": 70, "loyalty": 68, "region": "Stormlands", "members": ["Stannis Baratheon", "Robert Baratheon", "Renly Baratheon"], "dragons": 0},
    "Greyjoy": {"motto": "We Do Not Sow", "sigil": "🦀", "strength": 70, "wealth": 55, "loyalty": 60, "region": "Iron Islands", "members": ["Yara Greyjoy", "Theon Greyjoy", "Euron Greyjoy"], "dragons": 0}
}

selected_house = st.sidebar.selectbox("Select your House", list(houses.keys()), index=0)
selected_mode = st.sidebar.radio("Dashboard mode", ["House Overview", "Throne 3D Map", "Dragon Lair", "Battle Simulator", "Champion Forge"])

st.sidebar.markdown("---")
st.sidebar.write("Theme: Stormy Night | Animation: Dragon Flame | Style: High Fantasy")

house = houses[selected_house]

if selected_mode == "House Overview":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader(f"House {selected_house} {house['sigil']}")
    st.markdown(f"**Motto:** {house['motto']}  |  **Region:** {house['region']}")
    st.markdown(f"**Key members:** {', '.join(house['members'])}")

    metrics = pd.DataFrame([
        {"Attribute": "Strength", "Value": house["strength"]},
        {"Attribute": "Wealth", "Value": house["wealth"]},
        {"Attribute": "Loyalty", "Value": house["loyalty"]}
    ])

    col1, col2 = st.columns([1, 1])
    with col1:
        st.metric(label="House Power", value=f"{house['strength']} pts")
        st.metric(label="Treasure", value=f"{house['wealth']}%")
        st.metric(label="Honor", value=f"{house['loyalty']}%")
        st.write("\n")
        st.write("This overview reveals where your House is strongest, and where your foes may strike.")
    with col2:
        fig = go.Figure(go.Bar(x=metrics.Attribute, y=metrics.Value, marker_color=['#ff8c00', '#c71585', '#1e90ff']))
        fig.update_layout(height=380, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=20,b=20))
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif selected_mode == "Throne 3D Map":
    st.subheader("Throne Power Grid")
    st.write("This 3D visualization represents the balance of power across the major Houses. Rotate, zoom, and inspect the throne's aura.")

    x = np.linspace(-2, 2, 45)
    y = np.linspace(-2, 2, 45)
    x, y = np.meshgrid(x, y)
    z = np.sin((x**2 + y**2) * 1.5) * np.exp(-0.3 * (x**2 + y**2)) * 12 + 16

    surface = go.Surface(
        x=x,
        y=y,
        z=z,
        colorscale='Inferno',
        lighting=dict(ambient=0.5, diffuse=0.9, roughness=0.9, specular=0.4),
        showscale=False,
        hoverinfo='skip'
    )

    crown = go.Scatter3d(
        x=[0, 0.7, -0.7, 0.7, -0.7],
        y=[0, 0.7, 0.7, -0.7, -0.7],
        z=[20, 18, 18, 18, 18],
        mode='markers+lines',
        marker=dict(size=6, color='gold'),
        line=dict(color='gold', width=3)
    )

    fig = go.Figure(data=[surface, crown])
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.1)),
            aspectmode='auto'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=20, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

elif selected_mode == "Dragon Lair":
    st.subheader("Dragon Lair")
    st.write("Welcome to the dragon vault. Summon the beasts, inspect their power, and watch the flight path of dragon fire.")

    dragon_count = house.get("dragons", 0)
    st.markdown(f"**Dragons under your command:** {dragon_count}")
    if dragon_count > 0:
        st.success(f"House {selected_house} commands {dragon_count} dragons. Your skies burn bright.")
    else:
        st.warning("No dragons are assigned to this House. Only House Targaryen commands dragons by default.")

    t = np.linspace(0, 6 * np.pi, 200)
    x = np.sin(t) * np.linspace(0.6, 2.1, 200)
    y = np.cos(t) * np.linspace(0.6, 2.1, 200)
    z = np.linspace(0, 12, 200)

    dragon_path = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='lines',
        line=dict(color='crimson', width=10),
        hoverinfo='none'
    )

    flame1 = go.Scatter3d(
        x=[0.6, -0.6, 0],
        y=[0.6, 0.6, -0.6],
        z=[6, 6, 6],
        mode='markers',
        marker=dict(size=15, color='orange', opacity=0.8)
    )

    fig = go.Figure(data=[dragon_path, flame1])
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)),
            aspectmode='auto'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=20, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

    if st.button("Unleash dragon fire"):
        st.balloons()
        st.success("The dragon roars and flames paint the sky! 🔥🐉")

elif selected_mode == "Battle Simulator":
    st.subheader("Battle Simulator: Claim the Iron Throne")
    opponent_house = st.selectbox("Choose your opponent", [h for h in houses if h != selected_house])
    opponent = houses[opponent_house]

    battle_power = house["strength"] * 1.0 + house["loyalty"] * 0.8 + house["wealth"] * 0.3
    enemy_power = opponent["strength"] * 1.0 + opponent["loyalty"] * 0.8 + opponent["wealth"] * 0.3
    weather = st.select_slider("Battle conditions", options=["Fog", "Rain", "Clear", "Dragonfire"])

    modifier = {
        "Fog": 0.9,
        "Rain": 0.95,
        "Clear": 1.0,
        "Dragonfire": 1.15
    }[weather]

    if st.button("Engage the battle"):
        score = battle_power * random.uniform(0.85, 1.15) * modifier
        enemy_score = enemy_power * random.uniform(0.85, 1.15) * (modifier if weather != "Dragonfire" else 0.95)
        if score > enemy_score:
            st.success(f"House {selected_house} conquers the field and moves closer to the Iron Throne! 🏆")
        else:
            st.error(f"House {opponent_house} overpowers you. Retreat, regroup, and strike again. ⚔️")
        st.write(f"Your final battle score: {score:.1f} — Opponent score: {enemy_score:.1f}")
        st.progress(min(100, int(abs(score - enemy_score))))
    else:
        st.info("Choose your enemy, set the battle conditions, and clash for the throne.")

else:
    st.subheader("Champion Forge")
    name = st.text_input("Forge a champion name", value="Aegon Stormborn")
    role = st.selectbox("Champion role", ["Dragon Rider", "King's Hand", "Warden of the North", "Master of Whisperers"])
    armor = st.color_picker("Armor glow", "#b87333")
    dragon = st.checkbox("Bind a dragon to this hero")

    if st.button("Create Champion"):
        st.markdown(f"<div class='throne-panel'><h2>{name}</h2><p><strong>Role:</strong> {role}</p><p><strong>Armor aura:</strong> <span style='color:{armor};'>■■■■■</span></p><p><strong>Dragon bound:</strong> {'Yes' if dragon else 'No'}</p></div>", unsafe_allow_html=True)
        st.success("Your champion has been forged in fire and steel.")
    else:
        st.write("Customize the soul of your warrior and summon them to the Iron Throne.")

st.markdown("<div class='throne-panel'><h3>Iron Throne Realism</h3><p>While true 3D throne models require a WebGL component, this app simulates realistic energy on the throne via interactive visuals, animated power surfaces, and dramatic styling. Use the 3D map above to feel the throne's aura.</p></div>", unsafe_allow_html=True)

st.caption("Streamlit 3D GOT experience: use Streamlit, Plotly, and custom CSS for immersive fantasy visuals.")
