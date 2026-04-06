# ================================
# IMPORTS
# ================================
import streamlit as st
import pandas as pd
from supabase import create_client

# ================================
# CONFIG
# ================================
st.set_page_config(page_title="Finance Advisor", layout="centered")

st.title("💰 Personal Finance Planner")
st.info("Efficiently manage your finances for a better future")

# ================================
# SUPABASE
# ================================
SUPABASE_URL = "https://rwubgrllaaatrwqydqdg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ3dWJncmxsYWFhdHJ3cXlkcWRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM2OTAxMzYsImV4cCI6MjA4OTI2NjEzNn0.95AmKL8w6s78eTFdo2YYBFz6bTzNaljxEPGyFmwfrcA"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ================================
# STYLE
# ================================
st.markdown("""
<style>
.block-container {max-width:420px;}
div[data-testid="stMetric"] {
    background:white;
    padding:12px;
    border-radius:12px;
    box-shadow:0 2px 6px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

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

    mode = st.radio("Choose", ["Login", "Sign Up"], key="auth_mode")
    email = st.text_input("Email", key="auth_email")
    password = st.text_input("Password", type="password", key="auth_password")
    remember = st.checkbox("Remember me")

    if mode == "Sign Up":
        if st.button("Create account", key="signup"):
            if email and password:
                supabase.auth.sign_up({"email": email, "password": password})
                st.success("Account created")
            else:
                st.warning("Fill all fields")

    if mode == "Login":
        if st.button("Login", key="login"):
            if email and password:
                user = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
                st.session_state.user = user
                if remember:
                    st.session_state.remember = True
                st.rerun()
            else:
                st.warning("Fill all fields")

    st.stop()

user_email = st.session_state.user.user.email
st.success(f"Welcome {user_email}")

# ================================
# HELPERS
# ================================
def monthly_value(amount, freq):
    return amount if freq == "Monthly" else amount / 12

def input_freq(label, key, default=0):
    val = st.number_input(label, 0, 999999999, default, key=f"{key}_val")
    freq = st.selectbox("Frequency", ["Monthly","Annual","Occasional"], key=f"{key}_freq")
    return monthly_value(val, freq), freq

def get_reference_cost(ages):
    total = 0
    for age in ages:
        if age < 6: total += 3000
        elif age < 18: total += 4000
        else: total += 5000
    return total

def chat_response(q):
    if "save" in q: return "Reduce lifestyle or subscriptions"
    if "debt" in q: return "Pay high-interest loans first"
    return "Improve savings and reduce waste"

# ================================
# HOUSEHOLD
# ================================
st.subheader("👨‍👩‍👧 Household")

members = st.number_input("Members",1,10,1)
ages = [st.number_input(f"Age {i+1}",0,100,30,key=f"age{i}") for i in range(members)]

# ================================
# INPUT SECTIONS
# ================================
def section(title, items):
    with st.expander(title):
        data=[]
        for label,key,default in items:
            data.append(input_freq(label,key,default))
        return data

income_items = section("💵 Income",[
("Salary","inc_salary",0),
("Bonus","inc_bonus",0),
("Child support","inc_child",0),
("Tax return","inc_tax",0),
("Other income","inc_other",0)
])

loans_items = section("💳 Loans",[
("Mortgage","loan_mort",8000),
("Car loan","loan_car",0),
("Credit cards","loan_cc",0),
("Other loans","loan_other_loan",0)
])

housing_items = section("🏠 Housing",[
("Rent","house_rent",0),
("Association fees","house_association",0),
("Maintenance","house_maint",0),
("Renovations","house_renovation",0),
("Electricity","house_el",500),
("House Insurance","house_insurance",500)
])

transport_items = section("🚗 Transport",[
("Public transport","trans_pub",0),
("Fuel","trans_fuel",0),
("Car Insurance","trans_insurance",0),
("Vehicle Tax","trans_tax",0),
("Other fees and taxes","trans_t_other",0)
])

lifestyle_items = section("🛍 Lifestyle",[
("Groceries","life_food",0),
("Restaurants","life_rest",0),
("Entertainment","life_ent",0),
("Clothes","life_clothes",0),
("Grooming","life_groom",0),
("Self-care","life_selfcare",0)
])

subscriptions_items = section("📱 Subscriptions",[
("Phone","sub_phone",0),
("Internet","sub_inter",0),
("Gym","sub_gym",0),
("Trade Union","sub_union",0),
("Unemployment fund","sub_akassa",0),
("Streaming","sub_stream",0),
("Other","sub_other_suns",0)

])

savings_items = section("💰 Savings",[
("Buffer","sav_buf",0),
("Future","sav_fut",0),
("Children","sav_child",0),
("Investments","sav_inv",0),
("Other","sav_other_sav",0)

])

other_items = section("✈️ Other",[
("Travel","other_travel",0),
("Charity","other_charity",0),
("Other","other_other",0)
])

# ================================
# CALCULATIONS
# ================================
def total(items): return sum(v for v,_ in items)

income = total(income_items)
loans = total(loans_items)
housing = total(housing_items)
transport = total(transport_items)
lifestyle = total(lifestyle_items)
subscriptions = total(subscriptions_items)
savings = total(savings_items)
other = total(other_items)

total_expenses = housing + transport + lifestyle + subscriptions + loans + other
total_outflow = total_expenses + savings
net = income - total_outflow

savings_rate = (savings/income*100) if income>0 else 0

all_items = (
    income_items + loans_items + housing_items + transport_items +
    lifestyle_items + subscriptions_items + savings_items + other_items
)

# ================================
# FREQUENCY
# ================================
freq_data = {"Monthly":0,"Annual":0,"Occasional":0}

for v,f in all_items:
    freq_data[f]+=v

# ================================
# DASHBOARD
# ================================
tab1, tab2, tab3 = st.tabs(["📊 Dashboard","🎯 Goals","💬 Advisor"])

with tab1:

    st.subheader("🏦 Overview")

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Income",f"{income:,.0f}")
    c2.metric("Expenses",f"{total_expenses:,.0f}")
    c3.metric("Savings",f"{savings:,.0f}")
    c4.metric("Net",f"{net:,.0f}")

    # Health
    if total_outflow > income:
        st.error("Overspending")
    elif savings_rate < 10:
        st.warning("Low savings")
    else:
        st.success("Healthy")

    # Frequency chart
    st.subheader("📊 Spending Pattern")
    st.bar_chart(pd.DataFrame({
        "Type":["Monthly","Annual","Occasional"],
        "Amount":[freq_data["Monthly"],freq_data["Annual"],freq_data["Occasional"]]
    }).set_index("Type"))

    # Category %
    st.subheader("📊 Category Breakdown")

    categories = {
        "Housing":housing,
        "Transport":transport,
        "Lifestyle":lifestyle,
        "Subscriptions":subscriptions,
        "Loans":loans
    }

        total_cat = sum(categories.values())
        for k,v in categories.items():
        if total_cat>0:
        st.write(f"{k}: {(v/total_cat*100):.1f}%")

    # What-if
    
        st.subheader("🔮 What-if Simulator")
        reduction = st.slider("Reduce restaurants (%)", 0, 50, 10)
        rest_val = lifestyle_items["restaurants"][0]
        new_exp = total_expenses - rest_val + rest_val * (1 - reduction / 100)
        new_savings = income - new_exp
        st.write(f"New savings: {new_savings:,.0f} SEK/month")
        st.write(f"Improvement: {(new_savings - net):,.0f} SEK")


    # Needs vs Wants
    st.subheader("📊 Needs vs Wants")
    needs = housing + transport + food if 'food' in globals() else housing
    wants = lifestyle
    if income>0:
    st.write(f"Needs: {needs/income*100:.1f}%")
    st.write(f"Wants: {wants/income*100:.1f}%")

# ================================
# GOALS
# ================================
with tab2:

    goal = st.number_input("Goal",0,1_000_000,50000)
    months = st.number_input("Months",1,120,12)

    need = goal/months
    st.write(f"Need/month: {need:,.0f}")

    if savings>=need:
        st.success("On track")
    else:
        st.warning("Not enough saving")

    progress = min(savings/need if need>0 else 0,1)
    st.progress(progress)

# ================================
# AI
# ================================
with tab3:

    st.subheader("🤖 Advice")

    if savings_rate < 10:
        st.write("Increase savings")

    if housing/income > 0.4 if income>0 else False:
        st.write("Housing too high")

    q = st.text_input("Ask AI")
    if q:
        st.write(chat_response(q.lower()))

# ================================
# BENCHMARK
# ================================
ref = get_reference_cost(ages)

st.subheader("🇸🇪 Benchmark")
st.write(f"Reference: {ref:,.0f}")
st.write(f"Your spending: {total_expenses:,.0f}")

# ================================
# SAVE / LOAD
# ================================
st.subheader("💾 Save")

month = st.selectbox("Month",["Jan","Feb","Mar"])
year = st.number_input("Year",2020,2100,2025)

if st.button("Save"):
    supabase.table("budgets").insert({
        "email":user_email,
        "month":f"{month}-{year}",
        "income":income,
        "total_expenses":total_expenses
    }).execute()
    st.success("Saved")

if st.button("Load"):
    res = supabase.table("budgets").select("*").eq("email",user_email).execute()
    df = pd.DataFrame(res.data)
    if not df.empty:
        st.dataframe(df)
