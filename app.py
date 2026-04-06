# ---------- IMPORTS ---------- #
import streamlit as st
import pandas as pd
from supabase import create_client

# ---------- CONFIG ---------- #
st.set_page_config(page_title="Finance Advisor", layout="centered")

st.title("💰 Personal Finance Planner")
st.info("Efficiently manage your finances for a better future")

# ---------- SUPABASE ---------- #
SUPABASE_URL = "https://rwubgrllaaatrwqydqdg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ3dWJncmxsYWFhdHJ3cXlkcWRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM2OTAxMzYsImV4cCI6MjA4OTI2NjEzNn0.95AmKL8w6s78eTFdo2YYBFz6bTzNaljxEPGyFmwfrcA"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ------- APP View ----------- #

st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
    max-width: 420px;
}
div[data-testid="stMetric"] {
    background: #ffffff;
    padding: 10px;
    border-radius: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

# ---------- LOGIN ---------- #

st.subheader("🔐 Login")

login_mode = st.radio("Choose", ["Login", "Sign Up"], key="auth_mode")

email = st.text_input("Email", key="auth_email")
password = st.text_input("Password", type="password", key="auth_password")

remember_me = st.checkbox("Remember me", key="auth_remember")

# Initialize session
if "user" not in st.session_state:
    st.session_state.user = None

# ---------- SIGN UP ---------- #
if login_mode == "Sign Up":

    if st.button("Create account", key="auth_signup"):

        if email == "" or password == "":
            st.warning("Please enter email and password")

        else:
            try:
                supabase.auth.sign_up({
                    "email": email,
                    "password": password
                })
                st.success("Account created! Please log in.")

            except Exception as e:
                st.error(e)

# ---------- LOGIN ---------- #
elif login_mode == "Login":

    if st.button("Login", key="auth_login"):

        if email == "" or password == "":
            st.warning("Please enter email and password")

        else:
            try:
                user = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })

                st.session_state.user = user

                if remember_me:
                    st.session_state["remember"] = True

                st.success("Logged in!")

            except Exception as e:
                st.error(e)

# ---------- REQUIRE LOGIN ---------- #
if not st.session_state.user:
    st.warning("Please log in to continue")
    st.stop()

# ---------- USER INFO ---------- #
user_email = st.session_state.user.user.email
st.success(f"Logged in as: {user_email}")

# --------- Autologin if remembered ----------- #

if "user" in st.session_state and st.session_state.user:
    user_email = st.session_state.user.user.email
    st.success(f"Welcome back {user_email}")
else:
    # show login form

    st.divider()

# -------------- Householf profile -------- #

st.subheader("👨‍👩‍👧 Household Profile")

household_type = st.radio("Household type", ["Single", "Family"])

if household_type == "Single":
    members = 1
    ages = [st.number_input("Your age", 0, 100, 30)]
else:
    members = st.number_input("Number of family members", 1, 10, 3)
    ages = []

    for i in range(members):
        age = st.number_input(f"Age of member {i+1}", 0, 100, 30)
        ages.append(age)

#--------- Frequency Converter -------- #

def monthly_value(amount, frequency):
    if frequency == "Monthly":
        return amount
    elif frequency == "Annual":
        return amount / 12
    else:
        return amount / 12


def input_with_frequency(label, key, default=0):
    amount = st.number_input(label, 0, 999999999, default, key=f"{key}_amount")

    freq = st.selectbox(
        f"{label} frequency",
        ["Monthly", "Annual", "Occasional"],
        key=f"{key}_freq"
    )

    monthly = monthly_value(amount, freq)

    return monthly, freq

#--------- Konsumentverket -------- #

def get_reference_cost(ages):
    total = 0

    for age in ages:
        if age < 6:
            total += 3000
        elif age < 18:
            total += 4000
        else:
            total += 5000

    return total
        
# ---------- INCOME ---------- #
with st.expander("💵 Income", expanded=True):

    job, job_freq = input_with_frequency("Net Salary", "income_job", 0)
    bonus, bonus_freq = input_with_frequency("Bonus / commission", "income_bonus", 0)
    child_support, child_support_freq = input_with_frequency("Child support", "income_child_support", 0)
    other_support, other_support_freq = input_with_frequency("Other support", "income_other_support", 0)
    tax_return, tax_return_freq = input_with_frequency("Tax return", "income_tax_return", 0)
    other_income, other_income_freq = input_with_frequency("Other income", "income_other_income", 0)

income = (
    job +
    bonus +
    child_support +
    other_support +
    tax_return +
    other_income
)

st.success(f"Total Income: {income:,.0f} SEK")

income_items =[
    (job, job_freq),
    (bonus,    bonus_freq),
    (child_support, child_support_freq),
    (other_support, other_support_freq),
    (tax_return, tax_return_freq),
    (other_income, other_income_freq),
    ]

st.divider()


# ---------- LOANS ---------- #
with st.expander("💳 Loans"):

    mortgage_loan, mortgage_freq = input_with_frequency("Mortgage loan", "loans_mortgage", 8000)
    car_loan, car_freq = input_with_frequency("Car loan", "loans_car", 0)
    personal_loan, personal_freq = input_with_frequency("Personal loan", "loans_personal", 0)
    credit_cards, credit_freq = input_with_frequency("Credit cards", "loans_credit", 0)
    other_loans, other_loans_freq = input_with_frequency("Other loans", "loans_other_loans", 0)


loans = mortgage_loan + car_loan + personal_loan + credit_cards + other_loans

st.success(f"Total Loans: {loans:,.0f} SEK")

loans_items =[
    (mortgage_loan, mortgage_freq),
    (car_loan, car_freq),
    (personal_loan, personal_freq),
    (credit_cards, credit_freq),
    (other_loans, other_loans_freq),
    ]


st.divider()

# ---------- HOUSING ---------- #
with st.expander("🏠 Housing"):

    association, association_freq = input_with_frequency("Association fee", "housing_association", 0)
    rent, rent_freq = input_with_frequency("Rent", "housing_rent", 0)
    electricity, electricity_freq = input_with_frequency("Electricity", "housing_electricity", 500)
    heating, heating_freq = input_with_frequency("Heating", "housing_heating", 0)
    maintenance, maintenance_freq = input_with_frequency("Maintenance", "housing_maintenance", 0)
    renovation, renovation_freq = input_with_frequency("Renovation", "housing_renovation", 0)
    housing_other, housing_other_freq = input_with_frequency("Other housing", "housing_other", 0)


housing = (
    association +
    rent +
    electricity +
    heating +
    maintenance +
    renovation +
    housing_other
    )

st.success(f"Total Housing: {housing:,.0f} SEK")

housing_items =[
    (rent, rent_freq),
    (electricity, electricity_freq),
    (heating, heating_freq),
    (maintenance, maintenance_freq),
    (association, association_freq),
    (renovation, renovation_freq),
    (housing_other, housing_other_freq),
    ]


st.divider()

# ---------- TRANSPORT ---------- #
with st.expander("🚗 Transport"):

    transportation, transportation_freq = input_with_frequency("Public transportation", "transport_transportation", 0 )
    fuel, fuel_freq = input_with_frequency ("Fuel","transport_fuel", 0 )
    parking, parking_freq = input_with_frequency ("Parking", "transport_parking", 0 )
    insurance, insurance_freq = input_with_frequency ("Insurance", "transport_insurance", 0 )
    vehicle_tax, vehicle_tax_freq = input_with_frequency("Vehicle tax", "transport_vehicle_tax", 0 )
    other_transport, other_transport_freq= input_with_frequency("Other transport","transport_other_transport", 0 )

transport = transportation + fuel + parking + insurance + vehicle_tax + other_transport

st.success(f"Total Transport: {transport:,.0f} SEK")

transport_items = [
    (transportation, transportation_freq),
    (fuel, fuel_freq),
    (parking, parking_freq),
    (insurance, insurance_freq),
    (vehicle_tax, vehicle_tax_freq),
    (other_transport, other_transport_freq),
    ]
st.divider()

# ---------- LIFESTYLE ---------- #

with st.expander("🛍 Lifestyle"):

    food, food_freq = input_with_frequency ("Groceries", "lifestyle_food", 0 )
    restaurants, restaurants_freq = input_with_frequency ( "Restaurants", "lifestyle_restaurants", 0 )
    entertainment, entertainment_freq = input_with_frequency ( "Entertainment", "lifestyle_entertainment", 0 )
    clothes, clothes_freq = input_with_frequency ( "Clothes", "lifestyle_clothes", 0 )
    selfcare, selfcare_freq = input_with_frequency ( "Self-care", "lifestyle_selfcare", 0 )


lifestyle = food + restaurants + entertainment + clothes + selfcare

st.success(f"Total Lifestyle: {lifestyle:,.0f} SEK")

lifestyle_items =[
    (food, food_freq),
    (restaurants, restaurants_freq),
    (entertainment, entertainment_freq),
    (clothes, clothes_freq),
    (selfcare, selfcare_freq),
    ]


st.divider()

# ---------- SUBSCRIPTIONS ---------- #
with st.expander("📱 Subscriptions"):

    phone, phone_freq =  input_with_frequency ( "Phone", "subscriptions_phone", 0 )
    internet, internet_freq =  input_with_frequency ( "Internet", "subscriptions_internet", 0 )
    gym, gym_freq =  input_with_frequency ( "Gym", "subscriptions_gym", 0 )
    union, union_freq =  input_with_frequency ( "Trade Union", "subscriptions_union", 0 )
    unemployment_fund, unemployment_fund_freq =  input_with_frequency ( "Unemployment fund", "subscriptions_unemployment_fund", 0 )
    apps, apps_freq =  input_with_frequency ( "Mobile apps", "subscriptions_apps", 0 )
    streaming, streaming_freq =  input_with_frequency ( "Streaming services", "subscriptions_streaming", 0 )
    music, music_freq =  input_with_frequency ( "Music", "subscriptions_music", 0 )
    games, games_freq =  input_with_frequency ( "Games", "subscriptions_games", 0 )
    subs_other, subs_other_freq =  input_with_frequency ( "Other subscriptions", "subscriptions_subs_other", 0 )


subscriptions = phone + internet + gym + union + unemployment_fund + apps + streaming + music + games + subs_other

st.success(f"Total Subscriptions: {subscriptions:,.0f} SEK")

subscriptions_items =[
    (phone, phone_freq),
    (internet, internet_freq),
    (gym, gym_freq),
    (union, union_freq),
    (unemployment_fund, unemployment_fund_freq),
    (apps, apps_freq),
    (streaming, streaming_freq),
    (music, music_freq),
    (games, games_freq),
    (subs_other, subs_other_freq),
    ]


st.divider()

# ---------- SAVINGS ---------- #

with st.expander("💰 Savings & Investments"):

    buffer, buffer_freq = input_with_frequency("Emergency buffer", "saving_buffer", 0)

    future, future_freq = input_with_frequency("Future goals", "saving_future", 0)

    investments, investments_freq = input_with_frequency("Investments", "saving_investments", 0)

    crypto, crypto_freq = input_with_frequency("Crypto", "saving_crypto", 0)

    children, children_freq = input_with_frequency("Children savings", "saving_children", 0)

    other_savings, other_savings_freq = input_with_frequency("Other savings", "saving_other", 0)


savings_total = (
    buffer + future + investments + crypto + children + other_savings
)

st.success(f"Total Savings: {savings_total:,.0f} SEK")

savings_items = [
    (buffer, buffer_freq),
    (future, future_freq),
    (investments, investments_freq),
    (crypto, crypto_freq),
    (children, children_freq),
    (other_savings, other_savings_freq),
]

st.divider()

# ---------- OTHER ---------- #
with st.expander("✈️ Other"):

    travel, travel_freq =  input_with_frequency ( "Travel", "other_travel", 0 )
    charity, charity_freq =  input_with_frequency ( "Charity", "other_charity", 0 )
    other, other_freq =  input_with_frequency ( "Other", "other_other", 0 )

other_total = travel + charity + other

st.success(f"Total Other: {other_total:,.0f} SEK")

other_items =[
    (travel, travel_freq),
    (charity, charity_freq),
    (other, other_freq),
    ]

st.divider()

# ---------- TOTAL ---------- #

total_expenses = housing + transport + lifestyle + subscriptions + loans + other_total

total_outflow = total_expenses + savings_total

unallocated = income - total_outflow

savings_rate = (remaining / income * 100) if income > 0 else 0

#-------- All Items ----- #
all_items = (
    income_items +
    housing_items +
    transport_items +
    loans_items +
    lifestyle_items +
    subscriptions_items +
    savings_items +
    other_items
)

st.divider()

# ------- Spending by Category --------- #

st.subheader("📊 Spending by Category")

category_data = {
    "Housing": housing,
    "Transport": transport,
    "Lifestyle": lifestyle,
    "Subscriptions": subscriptions,
    "Loans": loans,
    "Other": other_total
}

total = sum(category_data.values())

for category, value in category_data.items():
    if total > 0:
        percent = (value / total) * 100
        st.write(f"{category}: {percent:.1f}%")

top_category = max(category_data, key=category_data.get)

st.info(f"💡 Your biggest spending category is {top_category}")

st.divider()    

# --------- Financial Overview -------- #

st.subheader("🏦 Monthly Financial Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Income", f"{income:,.0f}")
col2.metric("Expenses", f"{total_expenses:,.0f}")
col3.metric("Savings", f"{savings_total:,.0f}")
col4.metric("Unallocated", f"{unallocated:,.0f}")

st.divider()

# -------- Frequency Insight ---------- #

st.subheader("🧠 Spending Insights")

total = sum(freq_data.values())

if total > 0:
    annual_ratio = freq_data["Annual"] / total
    occasional_ratio = freq_data["Occasional"] / total
    monthly_ratio = freq_data["Monthly"] / total

    if annual_ratio > 0.3:
        st.warning("⚠️ Large portion of spending is annual — plan cash flow")

    if occasional_ratio > 0.3:
        st.warning("⚠️ High irregular spending — build emergency buffer")

    if monthly_ratio > 0.6:
        st.success("✅ Stable monthly spending structure")

st.divider()

# ------------- Visual Breakdown ---------- #

st.subheader("📊 Money Allocation")

chart_data = pd.DataFrame({
    "Category": ["Expenses", "Savings", "Unallocated"],
    "Amount": [total_expenses, savings_total, max(unallocated, 0)]
})

st.bar_chart(chart_data.set_index("Category"))

st.divider()
# ------------ Overspend + Health Check ------------- # 

st.subheader("🚨 Financial Health")

if total_outflow > income:
    st.error("❌ You are overspending — expenses + savings exceed income")

elif unallocated < 0:
    st.warning("⚠️ Your plan is not sustainable")

elif savings_total < income * 0.1:
    st.warning("⚠️ Low savings rate — aim for at least 10–20%")

else:
    st.success("✅ Healthy financial structure")

st.divider()

# ---------- Financial Health Score ---------- #

st.subheader("🏆 Financial Health Score")

score = 100

# Savings impact
if savings_rate < 10:
    score -= 30
elif savings_rate < 20:
    score -= 10

# Housing impact
if housing / income > 0.4:
    score -= 20

# Frequency impact
if freq_data["Occasional"] > freq_data["Monthly"] * 0.5:
    score -= 15

score = max(0, score)

st.metric("Score", f"{score}/100")

if score > 80:
    st.success("Excellent financial health")
elif score > 60:
    st.info("Good, but room for improvement")
else:
    st.warning("Needs attention")

st.divider()

# ---------- Saving Opportunity ---------- #

st.subheader("💡 Opportunities")

if lifestyle > income * 0.25:
    st.write("👉 Reduce lifestyle spending to increase savings")

if subscriptions > 500:
    st.write("👉 Review subscriptions — potential savings")

if transport > income * 0.15:
    st.write("👉 Transport costs are high — optimize routes or usage")

st.divider()

# ---------- AI FUNCTIONS ---------- #

def generate_advice():
    advice = []

    total = sum(freq_data.values())

    if total > 0:
        monthly_ratio = freq_data["Monthly"] / total
        annual_ratio = freq_data["Annual"] / total
        occasional_ratio = freq_data["Occasional"] / total

        if annual_ratio > 0.3:
            advice.append("📆 A large part of your spending is annual — plan ahead")

        if occasional_ratio > 0.3:
            advice.append("🎯 Irregular spending is high — build an emergency buffer")

        if monthly_ratio > 0.6:
            advice.append("✅ Your spending is stable and predictable")

    if savings_rate < 10:
        advice.append("⚠️ Your savings rate is low")

    if housing > income * 0.4:
        advice.append("🏠 Housing costs are high")

    return advice
st.divider()

# ---------- TABS ---------- #

tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🎯 Goals", "💬 Advisor"])

# ---------- DASHBOARD ---------- #
with tab1:

    st.subheader("📈 Spending Breakdown")

    chart_data = pd.DataFrame({
    "Category": ["Monthly", "Annual", "Occasional"],
    "Amount": [
        freq_data["Monthly"],
        freq_data["Annual"],
        freq_data["Occasional"]
    ]
    })

    st.bar_chart(chart_data.set_index("Category"))

    st.subheader("📊 Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Income", f"{income:,.0f}")
    col2.metric("Expenses", f"{total_expenses:,.0f}")
    col3.metric("Savings", f"{remaining:,.0f}")

    # ---------- Card style UI ---------- #

    st.markdown("""
<style>
.metric-card {
    background: white;
    padding: 15px;
    border-radius: 16px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    margin-bottom: 10px;
}
</style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="metric-card">', unsafe_allow_html=True)

    st.subheader("🏦 Your Financial Snapshot")

    col1, col2 = st.columns(2)
    col1.metric("Income", f"{income:,.0f}")
    col2.metric("Unallocated", f"{unallocated:,.0f}")

    col3, col4 = st.columns(2)
    col3.metric("Expenses", f"{total_expenses:,.0f}")
    col4.metric("Savings", f"{savings_total:,.0f}")

    st.markdown('</div>', unsafe_allow_html=True)
    
    
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
        
st.divider()

# ---------- Comparison with Konsumentverket ---------- #
reference_cost = get_reference_cost(ages)

st.subheader("🇸🇪 Household Benchmark")

st.write(f"Estimated reference cost: {reference_cost:,.0f} SEK/month")
st.write(f"Your spending: {total_expenses:,.0f} SEK/month")

if total_expenses > reference_cost:
    st.warning("⚠️ Your spending is above recommended levels")
else:
    st.success("✅ Your spending is within recommended range")

st.divider()


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

st.divider()


# ---------- Progress ------------ #

if monthly_savings_needed > 0:
    progress = current_savings / monthly_savings_needed
else:
    progress = 0

progress = max(0.0, min(progress, 1.0))

st.progress(progress)

st.write(f"Progress: {progress*100:.1f}%")

st.divider()

# ---------- ADVISOR ---------- #
with tab3:
    st.subheader("🤖 AI Advice")

    for tip in generate_advice():
        st.write(tip)

    question = st.text_input("Ask AI")

    if question:
        st.write("🤖", chat_response(question.lower()))

st.divider()

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

st.divider()


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
