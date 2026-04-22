# ================================
# IMPORTS
# ================================
import streamlit as st
from supabase import create_client

st.set_page_config(
    page_title="Finwise",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================================
# STYLE
# ================================
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.block-container {
    max-width: 480px;
    margin: auto;
    padding-top: 1rem;
}

.stButton button {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ================================
# TITLE
# ================================
st.title("Finwise")
st.caption("Personal Finance Planner")

# ================================
# SUPABASE
# ================================
SUPABASE_URL = "https://rwubgrllaaatrwqydqdg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ3dWJncmxsYWFhdHJ3cXlkcWRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM2OTAxMzYsImV4cCI6MjA4OTI2NjEzNn0.95AmKL8w6s78eTFdo2YYBFz6bTzNaljxEPGyFmwfrcA"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ================================
# SESSION
# ================================
if "step" not in st.session_state:
    st.session_state.step = 1

# ================================
# HELPERS
# ================================
def input_block(items):
    for label, key, default in items:
        st.number_input(label, 0, 999999999, default, key=key)

def show_card(title, value, icon="💰"):
    st.markdown(f"### {icon} {title}")
    st.write(f"**{value:,.0f} SEK**")

# ================================
# NAVIGATION
# ================================
page = st.radio("", ["🏠 Home", "👤 Profile"], horizontal=True)

# ================================
# HOME FLOW (NEW UX)
# ================================
if page == "🏠 Home":

    st.markdown(f"### Step {st.session_state.step} of 4")

    # STEP 1 — INCOME
    if st.session_state.step == 1:
        st.subheader("💵 Income")

        input_block([
            ("Salary", "inc_salary", 0),
            ("Bonus", "inc_bonus", 0),
            ("Other income", "inc_other", 0),
        ])

        if st.button("Next"):
            st.session_state.step = 2
            st.rerun()

    # STEP 2 — EXPENSES
    elif st.session_state.step == 2:
        st.subheader("💸 Expenses")

        input_block([
            ("Rent", "exp_rent", 0),
            ("Food", "exp_food", 0),
            ("Transport", "exp_transport", 0),
        ])

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Back"):
                st.session_state.step = 1
                st.rerun()

        with col2:
            if st.button("Next"):
                st.session_state.step = 3
                st.rerun()

    # STEP 3 — SAVINGS
    elif st.session_state.step == 3:
        st.subheader("💰 Savings")

        input_block([
            ("Monthly savings", "sav_monthly", 0),
        ])

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Back"):
                st.session_state.step = 2
                st.rerun()

        with col2:
            if st.button("Calculate"):
                st.session_state.step = 4
                st.rerun()

    # STEP 4 — RESULTS
    elif st.session_state.step == 4:
        st.subheader("📊 Overview")

        income = (
            st.session_state.get("inc_salary", 0)
            + st.session_state.get("inc_bonus", 0)
            + st.session_state.get("inc_other", 0)
        )

        expenses = (
            st.session_state.get("exp_rent", 0)
            + st.session_state.get("exp_food", 0)
            + st.session_state.get("exp_transport", 0)
        )

        savings = st.session_state.get("sav_monthly", 0)

        balance = income - expenses - savings

        show_card("Balance", balance, "💳")
        show_card("Income", income, "💵")
        show_card("Expenses", expenses, "💸")
        show_card("Savings", savings, "💰")

        if st.button("Start Over"):
            st.session_state.step = 1
            st.rerun()

# ================================
# PROFILE
# ================================
elif page == "👤 Profile":
    st.write("User profile coming soon...")