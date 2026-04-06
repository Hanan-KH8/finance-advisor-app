# ================================
# IMPORTS & CONFIG
# ================================
import streamlit as st
import pandas as pd
from supabase import create_client

st.set_page_config(page_title="Finance Planner", layout="centered")

# ================================
# STYLING (Mobile Banking Feel)
# ================================
st.markdown("""
<style>
.block-container {max-width:420px;}
div[data-testid="stMetric"] {
    background:white;
    padding:12px;
    border-radius:14px;
    box-shadow:0 2px 8px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

st.title("💰 Finance Planner")

# ================================
# SUPABASE
# ================================
SUPABASE_URL = "YOUR_URL"
SUPABASE_KEY = "YOUR_KEY"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ================================
# SESSION
# ================================
if "user" not in st.session_state:
    st.session_state.user = None

# ================================
# AUTH
# ================================
if not st.session_state.user:

    st.subheader("🔐 Login")

    mode = st.radio("Mode", ["Login", "Sign Up"], key="auth_mode")
    email = st.text_input("Email", key="auth_email")
    password = st.text_input("Password", type="password", key="auth_pass")

    if mode == "Sign Up":
        if st.button("Create account", key="signup"):
            supabase.auth.sign_up({"email": email, "password": password})
            st.success("Account created")

    if mode == "Login":
        if st.button("Login", key="login"):
            user = supabase.auth.sign_in_with_password(
                {"email": email, "password": password}
            )
            st.session_state.user = user
            st.rerun()

    st.stop()

user_email = st.session_state.user.user.email
st.success(f"Logged in as {user_email}")

# ================================
# HELPERS
# ================================
def monthly_value(amount, freq):
    return amount if freq == "Monthly" else amount / 12

def input_freq(label, key, default=0):
    val = st.number_input(label, 0, 1_000_000, default, key=f"{key}_val")
    freq = st.selectbox("Freq", ["Monthly","Annual","Occasional"], key=f"{key}_freq")
    return monthly_value(val, freq), freq

def build_freq_data(all_items):
    freq_data = {"Monthly":0,"Annual":0,"Occasional":0}
    for v,f in all_items:
        freq_data[f] += v
    return freq_data

def chat_response(q):
    if "save" in q: return "Reduce lifestyle or subscriptions"
    if "debt" in q: return "Pay high-interest loans first"
    return "Focus on improving savings"

# ================================
# PROFILE
# ================================
st.subheader("👨‍👩‍👧 Household")

members = st.number_input("Members",1,10,1)
ages = [st.number_input(f"Age {i+1}",0,100,30,key=f"age{i}") for i in range(members)]

# ================================
# INPUTS
# ================================
def section(title, items):
    with st.expander(title):
        results=[]
        for label,key,default in items:
            results.append(input_freq(label,key,default))
        return results

income_items = section("💵 Income",[
("Salary","inc_salary",0),
("Bonus","inc_bonus",0),
("Other","inc_other",0)
])

housing_items = section("🏠 Housing",[
("Rent","house_rent",0),
("Electricity","house_elec",500)
])

transport_items = section("🚗 Transport",[
("Fuel","trans_fuel",0),
("Public Transport","trans_public",0)
])

lifestyle_items = section("🛍 Lifestyle",[
("Food","life_food",0),
("Restaurants","life_rest",0)
])

subscriptions_items = section("📱 Subscriptions",[
("Phone","sub_phone",0),
("Streaming","sub_stream",0)
])

savings_items = section("💰 Savings",[
("Investments","sav_inv",0),
("Buffer","sav_buf",0)
])

other_items = section("✈️ Other",[
("Travel","other_travel",0)
])

# ================================
# CALCULATIONS
# ================================
def total(items): return sum(v for v,_ in items)

income = total(income_items)
expenses = sum([
    total(housing_items),
    total(transport_items),
    total(lifestyle_items),
    total(subscriptions_items),
    total(other_items)
])
savings = total(savings_items)

net = income - (expenses + savings)

all_items = (
    income_items + housing_items + transport_items +
    lifestyle_items + subscriptions_items + savings_items + other_items
)

freq_data = build_freq_data(all_items)

# ================================
# DASHBOARD
# ================================
tab1, tab2, tab3 = st.tabs(["📊 Dashboard","🎯 Goals","💬 Advisor"])

with tab1:

    st.subheader("Overview")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Income",f"{income:,.0f}")
    c2.metric("Expenses",f"{expenses:,.0f}")
    c3.metric("Savings",f"{savings:,.0f}")
    c4.metric("Net",f"{net:,.0f}")

    st.subheader("Spending Pattern")
    st.bar_chart(pd.DataFrame({
        "Type":["Monthly","Annual","Occasional"],
        "Amount":[freq_data["Monthly"],freq_data["Annual"],freq_data["Occasional"]]
    }).set_index("Type"))

    if net < 0:
        st.error("Overspending")
    elif savings < income*0.1:
        st.warning("Low savings")
    else:
        st.success("Healthy")

# ================================
# GOALS
# ================================
with tab2:

    goal = st.number_input("Goal",0,1_000_000,50000)
    months = st.number_input("Months",1,120,12)

    need = goal/months
    current = savings

    st.write(f"Needed/month: {need:,.0f}")

    if current >= need:
        st.success("On track")
    else:
        st.warning("Not on track")

# ================================
# AI
# ================================
with tab3:

    st.subheader("Advice")

    if savings < income*0.1:
        st.write("Increase savings")

    q = st.text_input("Ask AI")
    if q:
        st.write(chat_response(q.lower()))

# ================================
# SAVE / LOAD
# ================================
st.subheader("💾 Save")

month = st.selectbox("Month",["Jan","Feb","Mar"])
year = st.number_input("Year",2020,2100,2025)

if st.button("Save",key="save"):
    supabase.table("budgets").insert({
        "email":user_email,
        "month":f"{month}-{year}",
        "income":income,
        "total_expenses":expenses
    }).execute()
    st.success("Saved")

if st.button("Load",key="load"):
    res = supabase.table("budgets").select("*").eq("email",user_email).execute()
    df = pd.DataFrame(res.data)
    if not df.empty:
        st.dataframe(df)
