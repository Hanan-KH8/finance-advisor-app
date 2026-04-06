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
# SESSION INIT
# ================================
if "user" not in st.session_state:
    st.session_state.user = None

if "signup_clicked" not in st.session_state:
    st.session_state.signup_clicked = False

if "remember" not in st.session_state:
    st.session_state.remember = False


# ================================
# AUTO LOGIN (SOFT REMEMBER)
# ================================
if st.session_state.get("remember") and st.session_state.user:
    pass  # user stays logged in


# ================================
# AUTH
# ================================
if not st.session_state.user:

    st.subheader("🔐 Login")

    mode = st.radio("Choose", ["Login", "Sign Up"], key="auth_mode")

    email = st.text_input("Email", key="auth_email")
    password = st.text_input("Password", type="password", key="auth_password")

    remember = st.checkbox("Remember me")

    # ============================
    # SIGN UP
    # ============================
    if mode == "Sign Up":

        if st.session_state.signup_clicked:
            st.info("⏳ Processing... please wait")

        col1, col2 = st.columns(2)

        # Create account
        with col1:
            if st.button("Create account", key="signup"):

                if st.session_state.signup_clicked:
                    st.warning("⏳ Please wait before retrying")

                elif not email or not password:
                    st.warning("Enter email and password")

                else:
                    try:
                        st.session_state.signup_clicked = True

                        supabase.auth.sign_up({
                            "email": email,
                            "password": password
                        })

                        st.success("✅ Account created! Check your email to confirm.")

                    except Exception as e:
                        msg = str(e)

                        if "429" in msg:
                            st.warning("⏳ Too many attempts. Try again in ~60 seconds.")
                        else:
                            st.error(f"Signup failed: {msg}")

        # Resend confirmation email
        with col2:
            if st.button("Resend email", key="resend"):

                if not email:
                    st.warning("Enter your email first")

                else:
                    try:
                        supabase.auth.resend({
                            "type": "signup",
                            "email": email
                        })
                        st.success("📩 Confirmation email sent again")

                    except Exception as e:
                        st.error(f"Error: {e}")


    # ============================
    # LOGIN
    # ============================
    elif mode == "Login":

        if st.button("Login", key="login"):

            if not email or not password:
                st.warning("Enter email and password")

            else:
                try:
                    user = supabase.auth.sign_in_with_password({
                        "email": email,
                        "password": password
                    })

                    st.session_state.user = user
                    st.session_state.remember = remember

                    st.success("✅ Logged in!")
                    st.rerun()

                except Exception as e:
                    msg = str(e)

                    if "Email not confirmed" in msg:
                        st.warning("📩 Please confirm your email first")
                    else:
                        st.error(f"Login failed: {msg}")

    st.stop()


# ================================
# LOGGED-IN STATE
# ================================
user_email = st.session_state.user.user.email

col1, col2 = st.columns([3,1])

with col1:
    st.success(f"Welcome {user_email}")

with col2:
    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.remember = False
        st.rerun()
        
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

def financial_score_engine(
    income,
    savings,
    expenses,
    loans,
    freq_data,
):
    score = 100
    details = []

    # -------------------------
    # 1. Savings Score (30 pts)
    # -------------------------
    savings_rate = (savings / income * 100) if income > 0 else 0

    if savings_rate < 5:
        score -= 25
        details.append("❌ Very low savings")
    elif savings_rate < 10:
        score -= 15
        details.append("⚠️ Low savings")
    elif savings_rate >= 20:
        details.append("✅ Strong savings habit")

    # -------------------------
    # 2. Expense Ratio (25 pts)
    # -------------------------
    expense_ratio = expenses / income if income > 0 else 1

    if expense_ratio > 0.9:
        score -= 25
        details.append("❌ Spending almost all income")
    elif expense_ratio > 0.75:
        score -= 10
        details.append("⚠️ High spending level")

    # -------------------------
    # 3. Stability (20 pts)
    # -------------------------
    total = sum(freq_data.values())
    if total > 0:
        irregular = (freq_data["Annual"] + freq_data["Occasional"]) / total

        if irregular > 0.5:
            score -= 20
            details.append("❌ Unstable spending pattern")
        elif irregular > 0.3:
            score -= 10
            details.append("⚠️ Moderate irregular spending")

    # -------------------------
    # 4. Debt Load (15 pts)
    # -------------------------
    debt_ratio = loans / income if income > 0 else 0

    if debt_ratio > 0.4:
        score -= 15
        details.append("❌ High debt burden")
    elif debt_ratio > 0.2:
        score -= 8
        details.append("⚠️ Moderate debt level")

    # -------------------------
    # 5. Buffer (10 pts)
    # -------------------------
    if savings_rate < 5:
        score -= 10
        details.append("⚠️ No financial buffer")

    score = max(0, score)

    return score, details

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
# TOTALS
# ================================

def show_card(title, value, icon="💰"):
    color = "#16a34a" if value >= 0 else "#dc2626"

    st.markdown(f"""
    <div style="
        background: white;
        padding: 16px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 10px;
    ">
        <div style="font-size:14px; color:#666;">
            {icon} {title}
        </div>
        <div style="font-size:22px; font-weight:600; color:{color};">
            {value:,.0f} SEK
        </div>
    </div>
    """, unsafe_allow_html=True)

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
# FINANCIAL SCORE ENGINE
# ================================

score, insights = financial_score_engine(
    income,
    savings,
    total_expenses,
    loans,
    freq_data
)

st.subheader("🏆 Financial Health Score")
st.metric("Score", f"{score}/100")

for i in insights:
    st.write(i)

# ================================
# DASHBOARD
# ================================
page = st.radio(
    "",
    ["🏠 Home", "📊 Insights", "🎯 Goals", "💬 Advisor", "👤 Profile"],
    horizontal=True
)

if page == "🏠 Home":

    st.subheader("🏦 Available balance")

    # ---- BALANCE CARD ----
    show_card("Net Balance", net, "💳")

    # ---- GRID (KEY METRICS) ----
    col1, col2 = st.columns(2)
    col1.metric("Income", f"{income:,.0f}")
    col2.metric("Expenses", f"{total_expenses:,.0f}")

    col3, col4 = st.columns(2)
    col3.metric("Savings", f"{savings:,.0f}")
    col4.metric("Savings Rate", f"{savings_rate:.0f}%")

    st.divider()

elif page == "📊 Insights":

    st.subheader("📊 Spending Pattern")

    st.bar_chart(pd.DataFrame({
        "Type":["Monthly","Annual","Occasional"],
        "Amount":[freq_data["Monthly"],freq_data["Annual"],freq_data["Occasional"]]
    }).set_index("Type"))

    st.subheader("📊 Category Breakdown")

    categories = {
        "Housing": housing,
        "Transport": transport,
        "Lifestyle": lifestyle,
        "Subscriptions": subscriptions,
        "Loans": loans
    }

    total_cat = sum(categories.values())

    for k,v in categories.items():
        if total_cat > 0:
            st.write(f"{k}: {(v/total_cat*100):.1f}%")

    st.divider()

    # ---- WHAT IF ----
    st.subheader("🔮 Scenario Simulator")

    reduction = st.slider("Reduce restaurants (%)", 0, 50, 10)

    rest_val = lifestyle_items[1][0]

    new_exp = total_expenses - rest_val + rest_val * (1 - reduction / 100)
    new_net = income - new_exp

    st.write(f"New balance: {new_net:,.0f} SEK")
    st.write(f"Improvement: {(new_net - net):,.0f} SEK")


    # ---- HEALTH STATUS ----
    if total_outflow > income:
        st.error("❌ Overspending")
    elif savings_rate < 10:
        st.warning("⚠️ Low savings")
    else:
        st.success("✅ Healthy finances")

    st.divider()

    # ---- QUICK INSIGHTS ----
    st.subheader("💡 Quick Insights")

    if lifestyle > income * 0.25:
        st.write("👉 Lifestyle spending is high")

    if subscriptions > 500:
        st.write("👉 Review subscriptions")

    if loans > income * 0.3:
        st.write("👉 Debt level is high")
    

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
        "Housing": housing_items,
        "Transport": transport_items,
        "Lifestyle": lifestyle_items,
        "Subscriptions": subscriptions_items,
        "Loans": loans_items
    }

    category_totals = {k: sum(v for v,_ in items) for k,items in categories.items()}

    total_cat = sum(category_totals.values())

    for k, v in category_totals.items():
        if total_cat > 0:
            st.write(f"{k}: {(v/total_cat*100):.1f}%")
        

    # What-if
    
    st.subheader("🔮 What-if Simulator")

    reduction = st.slider("Reduce restaurants (%)", 0, 50, 10)

    rest_val = lifestyle_items[1][0]  # safer than dict

    new_exp = total_expenses - rest_val + rest_val * (1 - reduction / 100)
    new_savings = income - new_exp

    st.write(f"New savings: {new_savings:,.0f} SEK/month")
    st.write(f"Improvement: {(new_savings - net):,.0f} SEK")


    # Needs vs Wants
    st.subheader("📊 Needs vs Wants")
    needs = housing + transport + food if 'food' in globals() else housing
    wants = lifestyle
    
    if income > 0:
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
