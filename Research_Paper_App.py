import streamlit as st

import google.generativeai as genai

genai.configure(api_key=st.secrets["Google_Gemini_Key"])
model = genai.GenerativeModel('gemini-2.5-flash')

# Initialize session state
if "papers" not in st.session_state:
    st.session_state.papers = {}

papers = st.session_state.papers

st.title("📚 AI Research Paper Tracker")

menu = st.sidebar.selectbox(
    "Select an option",
    [
        "Add Paper",
        "Search Paper",
        "Update Keywords",
        "Delete Paper",
        "Display All Papers",
        "Filter by Keyword",
        "Sort by Year"
    ]
)

# -----------------------------
# 1. Add Paper
# -----------------------------
if menu == "Add Paper":
    st.subheader("Add New Research Paper")

    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Year", min_value=1900, max_value=2100, step=1)
    keywords = st.text_input("Keywords (comma-separated)")

    if st.button("Add Paper"):
        if title in papers:
            st.warning("Paper already exists!")
        else:
            papers[title] = {
                "Author": author,
                "Year": year,
                "Keywords": [k.strip().lower() for k in keywords.split(",")]
            }
            st.success("Paper added successfully!")

# -----------------------------
# 2. Search Paper
# -----------------------------
elif menu == "Search Paper":
    st.subheader("Search Paper")

    title = st.text_input("Enter Title")

    if st.button("Search"):
        if title in papers:
            p = papers[title]
            st.write(f"**Author:** {p['Author']}")
            st.write(f"**Year:** {p['Year']}")
            st.write(f"**Keywords:** {', '.join(p['Keywords'])}")
        else:
            st.error("Paper not found")

# -----------------------------
# 3. Update Keywords
# -----------------------------
elif menu == "Update Keywords":
    st.subheader("Update Keywords")

    title = st.text_input("Enter Title")
    new_keywords = st.text_input("New Keywords (comma-separated)")

    if st.button("Update"):
        if title in papers:
            papers[title]["Keywords"] = [k.strip().lower() for k in new_keywords.split(",")]
            st.success("Keywords updated!")
        else:
            st.error("Paper not found")

# -----------------------------
# 4. Delete Paper
# -----------------------------
elif menu == "Delete Paper":
    st.subheader("Delete Paper")

    title = st.text_input("Enter Title")

    if st.button("Delete"):
        if title in papers:
            del papers[title]
            st.success("Paper deleted!")
        else:
            st.error("Paper not found")

# -----------------------------
# 5. Display All Papers
# -----------------------------
elif menu == "Display All Papers":
    st.subheader("All Research Papers")

    if papers:
        for title, details in papers.items():
            st.write(f"**{title}**")
            st.write(f"Author: {details['Author']}")
            st.write(f"Year: {details['Year']}")
            st.write(f"Keywords: {', '.join(details['Keywords'])}")
            st.write("---")
    else:
        st.info("No papers available")

# -----------------------------
# 6. Filter by Keyword
# -----------------------------
elif menu == "Filter by Keyword":
    st.subheader("Filter Papers")

    keyword = st.text_input("Enter keyword")

    if st.button("Filter"):
        found = False
        for title, details in papers.items():
            if keyword.lower() in details["Keywords"]:
                st.write(f"**{title}** - {details['Author']} ({details['Year']})")
                found = True
        
        if not found:
            st.warning("No papers found")

# -----------------------------
# 7. Sort by Year
# -----------------------------
elif menu == "Sort by Year":
    st.subheader("Sorted Papers")

    if papers:
        sorted_papers = sorted(papers.items(), key=lambda x: x[1]["Year"])
        
        for title, details in sorted_papers:
            st.write(f"**{title}** - {details['Author']} ({details['Year']})")
    else:
        st.info("No papers available")