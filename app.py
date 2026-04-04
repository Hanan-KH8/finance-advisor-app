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
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ3dWJncmxsYWFhdHJ3cXlkcWRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM2OTAxMzYsImV4cCI6MjA4OTI2NjEzNn0.95AmKL8w6s78eTFdo2YYBFz6bTzNaljxEPGyFmwfrcA"

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

# ---------- INCOME ---------- #

with st.expander("💵 Income", expanded=True):

    job = st.number_input("Job", 0, 200000, 25000)
    bonus = st.number_input("Bonus / commission", 0, 200000, 0)
    child_support = st.number_input("Child support", 0, 200000, 0)
    other_support = st.number_input("Other support", 0, 200000, 0)
    tax_return = st.number_input("Tax return", 0, 200000, 0)
    other_income = st.number_input("Other", 0, 200000, 0)

income = job + bonus + child_support + other_support + tax_return + other_income

st.success(f"Total Income: {income:,.0f} SEK")

# ---------- HOUSING ---------- #

with st.expander("🏠 Housing"):

    mortgage = st.number_input("Rent / Mortgage", 0, 200000, 9000)
    electricity = st.number_input("Electricity", 0, 200000, 500)
    heating = st.number_input("Heating", 0, 200000, 400)
    maintenance = st.number_input("Maintenance", 0, 200000, 300)
    association = st.number_input("Association fee", 0, 200000, 2000)
    renovation = st.number_input("Renovation", 0, 200000, 0)
    housing_other = st.number_input("Other housing", 0, 200000, 300)

housing = mortgage + electricity + heating + maintenance + association + renovation + housing_other

st.success(f"Total Housing: {housing:,.0f} SEK")


# ---------- TRANSPORT ---------- #

with st.expander("🚗 Transport"):

    transport_loan = st.number_input("Vehicle loan", 0, 200000, 0)
    fuel = st.number_input("Fuel", 0, 200000, 1500)
    parking = st.number_input("Parking", 0, 200000, 500)
    insurance = st.number_input("Insurance", 0, 200000, 800)
    tax = st.number_input("Vehicle tax", 0, 200000, 300)
    transport_other = st.number_input("Other transport", 0, 200000, 200)

transport = transport_loan + fuel + parking + insurance + tax + transport_other
st.write(f"Total Transport: {transport:,.0f} SEK")

st.success(f"Total Transport: {transport:,.0f} SEK")

# ---------- LIFESTYLE ---------- #

with st.expander("🛍 Lifestyle"):

    food = st.number_input("Food", 0, 200000, 3000)
    restaurants = st.number_input("Restaurants", 0, 200000, 800)
    entertainment = st.number_input("Entertainment", 0, 200000, 500)
    clothes = st.number_input("Clothes", 0, 200000, 500)
    selfcare = st.number_input("Self-care", 0, 200000, 300)

lifestyle = food + restaurants + entertainment + clothes + selfcare

st.success(f"Total Lifestyle: {lifestyle:,.0f} SEK")

# ---------- SUBSCRIPTIONS ---------- #

with st.expander("📱 subscriptions"):

    phone = st.number_input("Phone", 0, 10000, 300)
    internet = st.number_input("Internet", 0, 10000, 400)
    gym = st.number_input("Gym", 0, 10000, 400)
    union = st.number_input("Trade Union", 0, 10000, 300)
    unemployment = st.number_input("Unemployment fund", 0, 10000, 200)
    apps = st.number_input("Mobile apps", 0, 10000, 100)
    streaming = st.number_input("Streaming services", 0, 10000, 200)
    music = st.number_input("Music", 0, 10000, 100)
    games = st.number_input("Games", 0, 10000, 100)
    subs_other = st.number_input("Other subscriptions", 0, 10000, 100)

subscriptions = phone + internet + gym + union + unemployment + apps + streaming + music + games + subs_other

st.success(f"Total subscriptions: {subscriptions:,.0f} SEK")

# ---------- OTHER ---------- #

with st.expander("✈️ Other"):

    travel = st.number_input("Travel", 0, 200000, 500)
    charity = st.number_input("Charity", 0, 200000, 0)
    other = st.number_input("Other", 0, 200000, 1000)

other_total = travel + charity + other

st.success(f"Total Other: {other_total:,.0f} SEK")

# ---------- TOTAL ---------- #

total_expenses = housing + transport + lifestyle + subscriptions + other_total
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

    # ---------- WHAT-IF SIMULATOR ---------- #
    st.subheader("🔮 What-if Simulator")

    reduction = st.slider("Reduce restaurants spending (%)", 0, 50, 10)

    new_restaurants = restaurants * (1 - reduction / 100)
    new_expenses = total_expenses - restaurants + new_restaurants
    new_savings = income - new_expenses

    st.write(f"New savings: {new_savings:,.0f} SEK/month")
    st.write(f"Improvement: {(new_savings - remaining):,.0f} SEK")

    # ---------- NEEDS VS WANTS ---------- #
    st.subheader("📊 Needs vs Wants")

    needs = housing + food + transport
    wants = restaurants + entertainment + subscriptions
    savings = remaining

    if income > 0:
        st.write(f"Needs: {needs/income*100:.1f}%")
        st.write(f"Wants: {wants/income*100:.1f}%")
        st.write(f"Savings: {savings/income*100:.1f}%")

# ---------- Goal ------------- #

st.subheader("🎯 Financial Goal")

goal_amount = st.number_input("Goal amount (SEK)", 0, 1000000, 50000)
goal_months = st.number_input("Timeframe (months)", 1, 120, 12)

monthly_savings_needed = goal_amount / goal_months

current_savings = income - total_expenses

st.write(f"💡 You need to save {monthly_savings_needed:,.0f} SEK/month")

if current_savings >= monthly_savings_needed:
    st.success("✅ You are on track to reach your goal!")
else:
    gap = monthly_savings_needed - current_savings
    st.warning(f"⚠️ You need an extra {gap:,.0f} SEK/month to reach your goal")

# ---------- Progress ------------ #

progress = min(current_savings / monthly_savings_needed, 1.0)

st.progress(progress)

st.write(f"Progress: {progress*100:.1f}%")

# ---------- ADVISOR ---------- #
with tab3:
    st.subheader("🤖 AI Advice")

    for tip in generate_advice():
        st.write(tip)

    question = st.text_input("Ask AI")

    if question:
        st.write("🤖", chat_response(question.lower()))

# ---------- SAVE DATA ---------- #

st.subheader("💾 Save Budget")

month = st.selectbox("Month", [
    "Jan","Feb","Mar","Apr","May","Jun",
    "Jul","Aug","Sep","Oct","Nov","Dec"
])

year = st.number_input("Year", 2020, 2100, 2025)

if st.button("Save my budget"):

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
        st.success("Budget saved!")

    except Exception as e:
        st.error(f"Error: {e}")

# ---------- LOAD DATA ---------- #
  
st.subheader("📂 Load Previous Budgets")

if st.button("Load my data"):

    result = supabase.table("budgets").select("*").eq("email", user_email).execute()

    df = pd.DataFrame(result.data)

    if not df.empty:

        # Sort data
        df_sorted = df.sort_values("month")

        # Show table
        st.dataframe(df_sorted)

        # Add savings column
        df_sorted["savings"] = df_sorted["income"] - df_sorted["total_expenses"]

        # 📈 Chart 1
        st.subheader("📈 Income vs Expenses")
        st.line_chart(
            df_sorted.set_index("month")[["income", "total_expenses"]]
        )

        # 📈 Chart 2
        st.subheader("💰 Savings Trend")
        st.line_chart(
            df_sorted.set_index("month")[["income", "total_expenses", "savings"]]
        )

        # 📊 Summary
        st.subheader("📊 Summary")

        st.write(f"Average income: {df_sorted['income'].mean():,.0f} SEK")
        st.write(f"Average expenses: {df_sorted['total_expenses'].mean():,.0f} SEK")
        st.write(f"Average savings: {df_sorted['savings'].mean():,.0f} SEK")

    else:
        st.warning("No data found for this user.")
