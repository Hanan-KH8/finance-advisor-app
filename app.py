# ---------- IMPORTS ---------- #
import streamlit as st
import pandas as pd
from supabase import create_client

# ---------- CONFIG ---------- #
st.set_page_config(page_title="Finance Advisor", layout="centered")

st.title("💰 Personal Finance Advisor")
st.info("This tool provides financial insights for educational purposes and is not financial advice.")

# ---------- SUPABASE ---------- #
SUPABASE_URL = "https://rwubgrllaaatrwqydqdg.supabase.co"
SUPABASE_KEY = "YOUR_KEY_HERE"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------- LOGIN ---------- #
st.subheader("🔐 Login")

login_mode = st.radio("Choose", ["Login", "Sign Up"])
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if "user" not in st.session_state:
    st.session_state.user = None

if login_mode == "Sign Up":
    if st.button("Create account"):
        try:
            supabase.auth.sign_up({"email": email, "password": password})
            st.success("Account created! Please log in.")
        except Exception as e:
            st.error(e)

elif login_mode == "Login":
    if st.button("Login"):
        try:
            user = supabase.auth.sign_in_with_password({"email": email, "password": password})
            st.session_state.user = user
            st.success("Logged in!")
        except Exception as e:
            st.error(e)

if not st.session_state.user:
    st.warning("Please log in to continue")
    st.stop()

user_email = st.session_state.user.user.email
st.success(f"Logged in as: {user_email}")

# ---------- INPUTS ---------- #

with st.expander("💵 Income", expanded=True):
    job = st.number_input("Job", 0, 200000, 25000)
    bonus = st.number_input("Bonus", 0, 200000, 0)
    income = job + bonus

with st.expander("🏠 Housing"):
    mortgage = st.number_input("Mortgage/Rent", 0, 200000, 9000)
    electricity = st.number_input("Electricity", 0, 200000, 500)
    housing = mortgage + electricity

with st.expander("🚗 Transport"):
    fuel = st.number_input("Fuel", 0, 200000, 1500)
    insurance = st.number_input("Insurance", 0, 200000, 800)
    transport = fuel + insurance

with st.expander("🛍 Lifestyle"):
    food = st.number_input("Food", 0, 200000, 3000)
    restaurants = st.number_input("Restaurants", 0, 200000, 800)
    entertainment = st.number_input("Entertainment", 0, 200000, 500)
    lifestyle = food + restaurants + entertainment

with st.expander("📱 Subscriptions"):
    phone = st.number_input("Phone", 0, 10000, 300)
    streaming = st.number_input("Streaming", 0, 10000, 200)
    subscriptions = phone + streaming

# ---------- CALCULATIONS ---------- #

total_expenses = housing + transport + lifestyle + subscriptions
remaining = income - total_expenses
savings_rate = (remaining / income * 100) if income > 0 else 0

# ---------- AI FUNCTIONS ---------- #

def generate_advice():
    advice = []
    if savings_rate < 10:
        advice.append("⚠️ Try increasing savings")
    if housing > income * 0.4:
        advice.append("🏠 Housing too high")
    return advice

def chat_response(q):
    if "save" in q:
        return "Reduce restaurants and subscriptions"
    return "Focus on saving more"

# ---------- TABS ---------- #

tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🎯 Goals", "💬 Advisor"])

# ---------- DASHBOARD ---------- #
with tab1:
    st.subheader("📊 Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Income", f"{income:,.0f}")
    col2.metric("Expenses", f"{total_expenses:,.0f}")
    col3.metric("Savings", f"{remaining:,.0f}")

# ---------- GOALS ---------- #
with tab2:
    st.subheader("🎯 Goal")

    goal = st.number_input("Goal (SEK)", 0, 1000000, 50000)
    months = st.number_input("Months", 1, 120, 12)

    needed = goal / months

    if remaining >= needed:
        st.success("On track")
    else:
        st.warning("Not on track")

# ---------- ADVISOR ---------- #
with tab3:
    st.subheader("🤖 AI Advice")

    for tip in generate_advice():
        st.write(tip)

    question = st.text_input("Ask AI")

    if question:
        st.write("🤖", chat_response(question.lower()))

# ---------- SAVE ---------- #
st.subheader("💾 Save")

month = st.selectbox("Month", ["Jan","Feb","Mar","Apr"])
year = st.number_input("Year", 2020, 2100, 2025)

if st.button("Save"):
    try:
        data = {
            "email": user_email,
            "month": f"{month}-{year}",
            "income": income,
            "housing": housing,
            "food": food,
            "transport": transport,
            "total_expenses": total_expenses
        }
        supabase.table("budgets").insert(data).execute()
        st.success("Saved")
    except Exception as e:
        st.error(e)

# ---------- LOAD ---------- #
st.subheader("📂 Load")

if st.button("Load"):
    result = supabase.table("budgets").select("*").eq("email", user_email).execute()
    df = pd.DataFrame(result.data)

    if not df.empty:
        st.dataframe(df)
        st.line_chart(df[["income", "total_expenses"]])
