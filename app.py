"""All episodes as one app, for the hosted version.

Each episode also runs on its own: streamlit run episodes/NN-slug/app.py
"""

from pathlib import Path

import streamlit as st

EPISODES = Path(__file__).parent / "episodes"

pages = [
    st.Page(str(app), title=app.parent.name, url_path=app.parent.name)
    for app in sorted(EPISODES.glob("*/app.py"))
]

if pages:
    # Each episode is embedded on its own page at caspase.ai, so the app
    # shows no navigation of its own. Every episode is still reachable by URL.
    st.navigation(pages, position="hidden").run()
else:
    st.write("No episodes yet.")
