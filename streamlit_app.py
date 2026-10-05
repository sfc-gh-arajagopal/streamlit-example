import streamlit as st
import streamlit.components.v1 as components

from therapy_maps import MAPS, to_markdown, to_mermaid, to_svg

st.set_page_config(page_title="Therapy mind maps", page_icon=":brain:", layout="wide")
st.markdown(
    """
    <style>
    .block-container {padding-top: 1.4rem; padding-bottom: 3rem; max-width: 1180px;}
    .map-kicker {letter-spacing: .08em; text-transform: uppercase; font-size: .78rem; color: #78716c;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Therapy mind maps")
st.write(
    "Original study maps of widely published therapy ideas: the process of care, "
    "CBT, thought traps, ACT, formulation, anxiety, low mood, emotion, the alliance, "
    "and a blank session map."
)
st.caption(
    "The page at recursospsicologia.online/therapy-mind-maps could not be opened from here, "
    "and that collection is a paid download. These maps are newly written for study and "
    "supervision discussion. They are not a treatment protocol and not a substitute for clinical training."
)

query = st.sidebar.text_input("Find a map", placeholder="anxiety, alliance, formulation")
matches = [
    mind_map
    for mind_map in MAPS
    if query.strip().lower() in f"{mind_map['title']} {mind_map['summary']} {mind_map['center']}".lower()
]
if not matches:
    st.sidebar.warning("No map matches that search.")
    matches = MAPS

titles = [mind_map["title"] for mind_map in matches]
if st.session_state.get("map_title") not in titles:
    st.session_state["map_title"] = titles[0]
selected_title = st.sidebar.radio("Maps", titles, key="map_title")
selected = next(mind_map for mind_map in matches if mind_map["title"] == selected_title)

st.markdown(f'<p class="map-kicker">{len(selected["branches"])} branches</p>', unsafe_allow_html=True)
st.subheader(selected["title"])
st.write(selected["summary"])

svg, width, height = to_svg(selected)
components.html(
    f'<div style="background:#fbf7f2;border-radius:28px;overflow:auto">{svg}</div>',
    height=height + 12,
    scrolling=True,
)

markdown = to_markdown(selected)
mermaid = to_mermaid(selected)
stem = selected["id"]
col1, col2, col3 = st.columns(3)
with col1:
    st.download_button("Download SVG", svg, file_name=f"{stem}-mind-map.svg", mime="image/svg+xml")
with col2:
    st.download_button("Download outline", markdown, file_name=f"{stem}-mind-map.md", mime="text/markdown")
with col3:
    st.download_button("Download Mermaid", mermaid, file_name=f"{stem}-mind-map.mmd", mime="text/plain")

with st.expander("Text outline"):
    st.markdown(markdown)
with st.expander("Mermaid source"):
    st.code(mermaid, language="mermaid")
