import streamlit as st
import pandas as pd

st.set_page_config(page_title="PWCS GPA Calculator", page_icon="🎓", layout="centered")

# Custom styling for a sleek, compact student portal look
st.markdown("""
    <style>
    .main-header {
        font-size: 1.8rem;
        color: #0A2540;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-header {
        color: #4A5568;
        font-size: 0.95rem;
        margin-bottom: 15px;
    }
    .disclaimer-box {
        margin-top: 40px;
        padding: 12px;
        background-color: #F1F5F9;
        border-radius: 6px;
        text-align: center;
        color: #64748B;
        font-size: 0.85rem;
        border: 1px solid #E2E8F0;
    }
    .stButton>button {
        width: 100%;
        border-radius: 6px;
        font-weight: bold;
        background-color: #0A2540;
        color: #FFFFFF;
        border: none;
        padding: 8px;
    }
    .stButton>button:hover {
        background-color: #1E3A8A;
        color: #FFD700;
    }
    </style>
""", unsafe_allow_html=True)

# Compact Header
st.markdown('<p class="main-header">🎓 PWCS GPA Calculator</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Prince William County Public Schools grade and GPA tracker.</p>', unsafe_allow_html=True)

# Reference chart expander
with st.expander("📖 View Grading Scale Reference"):
    scale_data = {
        "Percentage": ["92–100", "90–91.99", "87–89.99", "82–86.99", "80–81.99", "77–79.99", "72–76.99", "70–71.99", "67–69.99", "62–66.99", "60–61.99", "<60"],
        "Letter": ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F"],
        "Standard": [4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.3, 1.0, 0.7, 0.0],
        "Honors (+.5)": [4.5, 4.2, 3.8, 3.5, 3.2, 2.8, 2.5, 2.2, "N/A", "N/A", "N/A", "N/A"],
        "AP/DE (+1.0)": [5.0, 4.7, 4.3, 4.0, 3.7, 3.3, 3.0, 2.7, "N/A", "N/A", "N/A", "N/A"]
    }
    st.table(pd.DataFrame(scale_data))

# Input type toggle
input_mode = st.radio(
    "Choose input type:",
    ["Letter Grades", "Percentages (0-100)"],
    horizontal=True
)

st.divider()

# Initialize default 7 classes in session state
if "compact_classes" not in st.session_state or st.session_state.get("last_mode") != input_mode:
    st.session_state.last_mode = input_mode
    default_val = "A" if "Letter" in input_mode else 95.0
    st.session_state.compact_classes = [
        {"name": f"Period {i+1}", "level": "Standard", "q1": default_val, "q2": default_val, "q3": default_val, "q4": default_val}
        for i in range(7)
    ]

grade_options = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F", "None"]
level_options = ["Standard", "Honors (.5)", "AP/DE (1.0)"]

st.markdown("### 📝 Enter Your Classes")

# Compact list layout using neat columns for each class row
updated_classes = []
for i, c in enumerate(st.session_state.compact_classes):
    cols = st.columns([2.2, 1.8, 1, 1, 1, 1])
    
    c_name = cols[0].text_input(f"Name {i}", value=c["name"], key=f"c_name_{i}", label_visibility="collapsed")
    c_level = cols[1].selectbox(f"Level {i}", level_options, index=level_options.index(c["level"]) if c["level"] in level_options else 0, key=f"c_level_{i}", label_visibility="collapsed")
    
    if "Letter" in input_mode:
        c_q1 = cols[2].selectbox(f"Q1 {i}", grade_options, index=grade_options.index(c["q1"]) if c["q1"] in grade_options else 0, key=f"c_q1_{i}", label_visibility="collapsed")
        c_q2 = cols[3].selectbox(f"Q2 {i}", grade_options, index=grade_options.index(c["q2"]) if c["q2"] in grade_options else 0, key=f"c_q2_{i}", label_visibility="collapsed")
        c_q3 = cols[4].selectbox(f"Q3 {i}", grade_options, index=grade_options.index(c["q3"]) if c["q3"] in grade_options else 0, key=f"c_q3_{i}", label_visibility="collapsed")
        c_q4 = cols[5].selectbox(f"Q4 {i}", grade_options, index=grade_options.index(c["q4"]) if c["q4"] in grade_options else 0, key=f"c_q4_{i}", label_visibility="collapsed")
    else:
        c_q1 = cols[2].number_input(f"Q1 {i}", min_value=0.0, max_value=100.0, value=float(c["q1"]), key=f"c_q1_{i}", label_visibility="collapsed")
        c_q2 = cols[3].number_input(f"Q2 {i}", min_value=0.0, max_value=100.0, value=float(c["q2"]), key=f"c_q2_{i}", label_visibility="collapsed")
        c_q3 = cols[4].number_input(f"Q3 {i}", min_value=0.0, max_value=100.0, value=float(c["q3"]), key=f"c_q3_{i}", label_visibility="collapsed")
        c_q4 = cols[5].number_input(f"Q4 {i}", min_value=0.0, max_value=100.0, value=float(c["q4"]), key=f"c_q4_{i}", label_visibility="collapsed")
    
    updated_classes.append({"name": c_name, "level": c_level, "q1": c_q1, "q2": c_q2, "q3": c_q3, "q4": c_q4})

st.session_state.compact_classes = updated_classes

# Add class button below
if st.button("➕ Add Class"):
    default_val = "A" if "Letter" in input_mode else 95.0
    st.session_state.compact_classes.append({"name": f"Period {len(st.session_state.compact_classes)+1}", "level": "Standard", "q1": default_val, "q2": default_val, "q3": default_val, "q4": default_val})
    st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Calculation Logic helper
def get_pts(grade, level, is_letter):
    if is_letter:
        mapping = {"A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0, "B-": 2.7, "C+": 2.3, "C": 2.0, "C-": 1.7, "D+": 1.3, "D": 1.0, "D-": 0.7, "F": 0.0, "None": 0.0}
        base = mapping.get(grade, 0.0)
    else:
        score = float(grade)
        if score >= 92: base = 4.0
        elif score >= 90: base = 3.7
        elif score >= 87: base = 3.3
        elif score >= 82: base = 3.0
        elif score >= 80: base = 2.7
        elif score >= 77: base = 2.3
        elif score >= 72: base = 2.0
        elif score >= 70: base = 1.7
        elif score >= 67: base = 1.3
        elif score >= 62: base = 1.0
        elif score >= 60: base = 0.7
        else: base = 0.0

    if base >= 1.7:
        if level == "Honors (.5)": base += 0.5
        elif level == "AP/DE (1.0)": base += 1.0
    return base

# Calculate and display
if st.button("✨ Calculate GPAs", type="primary"):
    n = len(st.session_state.compact_classes)
    is_let = "Letter" in input_mode
    if n > 0:
        q1 = sum(get_pts(c["q1"], c["level"], is_let) for c in st.session_state.compact_classes if not (is_let and c["q1"] == "None")) / n
        q2 = sum(get_pts(c["q2"], c["level"], is_let) for c in st.session_state.compact_classes if not (is_let and c["q2"] == "None")) / n
        q3 = sum(get_pts(c["q3"], c["level"], is_let) for c in st.session_state.compact_classes if not (is_let and c["q3"] == "None")) / n
        q4 = sum(get_pts(c["q4"], c["level"], is_let) for c in st.session_state.compact_classes if not (is_let and c["q4"] == "None")) / n
        
        all_scores = [get_pts(c[q], c["level"], is_let) for c in st.session_state.compact_classes for q in ["q1", "q2", "q3", "q4"] if not (is_let and c[q] == "None")]
        year = sum(all_scores) / len(all_scores) if all_scores else 0.0

        st.success("Calculation Complete!")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Q1", f"{q1:.2f}")
        col2.metric("Q2", f"{q2:.2f}")
        col3.metric("Q3", f"{q3:.2f}")
        col4.metric("Q4", f"{q4:.2f}")
        col5.metric("Year", f"{year:.2f}")

# Student-made disclaimer at the bottom
st.markdown("""
    <div class="disclaimer-box">
        💡 <b>Disclaimer:</b> This app was independently created by a student as a personal project and is not affiliated with, endorsed by, or representative of Prince William County Public Schools.
    </div>
""", unsafe_allow_html=True)