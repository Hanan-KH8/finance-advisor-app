import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Finance Advisor",
    layout="centered"
)

# ---------- STYLE ---------- #

st.markdown("""
<style>
.block-container {
padding-top:1rem;
padding-bottom:2rem;
}

.card {
background-color:white;
padding:20px;
border-radius:14px;
box-shadow:0px 3px 10px rgba(0,0,0,0.05);
margin-bottom:20px;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ---------- #

st.title("💰 Personal Finance Advisor")

st.write(
"Analyze your finances and receive suggestions to improve financial health."
)

# ---------- MODE SELECTOR ---------- #

analysis_mode = st.radio(
    "Select analysis mode",
    ["Individual", "Household"]
)

# =====================================================
# INDIVIDUAL MODE
# =====================================================

if analysis_mode == "Individual":

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("💵 Your Income")

        income = st.number_input(
            "Monthly income (SEK)",
            0,
            200000,
            25000
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("📊 Your Expenses")

        housing = st.number_input("Housing contribution",0,200000,5000)
        food = st.number_input("Food / groceries",0,200000,2500)
        transport = st.number_input("Transport",0,200000,800)

        healthcare = st.number_input("Healthcare",0,200000,300)
        clothes = st.number_input("Clothes",0,200000,500)

        entertainment = st.number_input("Entertainment",0,200000,500)
        restaurants = st.number_input("Restaurants",0,200000,600)

        subscriptions = st.number_input("Subscriptions",0,200000,200)

        travel = st.number_input("Travel",0,200000,500)

        other = st.number_input("Other",0,200000,800)

        st.markdown("</div>", unsafe_allow_html=True)

    expenses = {
        "Housing":housing,
        "Food":food,
        "Transport":transport,
        "Healthcare":healthcare,
        "Clothes":clothes,
        "Entertainment":entertainment,
        "Restaurants":restaurants,
        "Subscriptions":subscriptions,
        "Travel":travel,
        "Other":other
    }

    total_expenses = sum(expenses.values())
    remaining = income - total_expenses

    savings_rate = (remaining / income * 100) if income > 0 else 0
    housing_ratio = housing / income if income > 0 else 0

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("📈 Financial Overview")

        col1,col2,col3 = st.columns(3)

        col1.metric("Expenses",f"{total_expenses:,.0f} SEK")
        col2.metric("Remaining",f"{remaining:,.0f} SEK")
        col3.metric("Savings rate",f"{savings_rate:.1f}%")

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- CHART ---------- #

    with st.container():

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("Spending breakdown")

        df = pd.DataFrame({
            "Category":expenses.keys(),
            "Amount":expenses.values()
        })

        st.bar_chart(df.set_index("Category"))

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- FINANCIAL LIFE SCORE ---------- #

    score = 50

    if savings_rate >= 20:
        score += 30
    elif savings_rate >= 10:
        score += 20
    elif savings_rate >= 5:
        score += 10

    if housing_ratio < 0.3:
        score += 20
    elif housing_ratio < 0.4:
        score += 10

    score = min(score,100)

    with st.container():

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("⭐ Financial Life Score")

        st.progress(score/100)

        st.metric("Score",f"{score}/100")

        if score > 80:
            st.success("Your finances are strong.")
        elif score > 60:
            st.info("Your finances are stable but could improve.")
        else:
            st.warning("Your finances may need attention.")

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- SUGGESTIONS ---------- #

    with st.container():

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("💡 Suggestions")

        if restaurants > income*0.1:
            st.info("Restaurant spending is relatively high.")

        if subscriptions > 500:
            st.info("Consider reviewing subscriptions.")

        if savings_rate < 10:
            st.warning("Aim to save at least 10-20% of income.")

        if remaining > 0:
            yearly = remaining * 12
            st.success(f"Potential yearly savings: {yearly:,.0f} SEK")

        st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# HOUSEHOLD MODE
# =====================================================

elif analysis_mode == "Household":

    with st.container():

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("🏠 Household")

        members = st.number_input("Household members",1,10,2)

        ages = []

        for i in range(members):
            ages.append(
                st.number_input(f"Age member {i+1}",0,100,30)
            )

        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("💵 Partner Income")

        col1,col2 = st.columns(2)

        partner_a_income = col1.number_input("Partner A income",0,200000,20000)
        partner_b_income = col2.number_input("Partner B income",0,200000,15000)

        income = partner_a_income + partner_b_income

        st.metric("Total household income",f"{income:,.0f} SEK")

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- EXPENSE INPUT FUNCTION ---------- #

    def expense_input(name,default):

        amount = st.number_input(name,0,200000,default)

        col1,col2 = st.columns(2)

        share_a = col1.slider("Partner A %",0,100,50,key=name)
        share_b = 100-share_a

        col2.write(f"Partner B %: {share_b}")

        return amount,share_a,share_b

    with st.container():

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("📊 Expenses")

        housing,housing_a,housing_b = expense_input("Housing",9000)
        food,food_a,food_b = expense_input("Food",3500)
        transport,transport_a,transport_b = expense_input("Transport",1000)

        loans,loan_a,loan_b = expense_input("Loans",2000)

        healthcare = st.number_input("Healthcare",0,10000,300)
        clothes = st.number_input("Clothes",0,10000,500)

        entertainment = st.number_input("Entertainment",0,10000,500)
        restaurants = st.number_input("Restaurants",0,10000,800)

        travel = st.number_input("Travel",0,10000,500)

        subscriptions = st.number_input("Subscriptions",0,10000,300)

        other = st.number_input("Other",0,10000,1000)

        st.markdown("</div>", unsafe_allow_html=True)

    expenses = {
        "Housing":housing,
        "Food":food,
        "Transport":transport,
        "Healthcare":healthcare,
        "Clothes":clothes,
        "Entertainment":entertainment,
        "Restaurants":restaurants,
        "Travel":travel,
        "Subscriptions":subscriptions,
        "Loans":loans,
        "Other":other
    }

    total_expenses = sum(expenses.values())
    remaining = income - total_expenses

    savings_rate = (remaining/income*100) if income>0 else 0

    # ---------- CHART ---------- #

    with st.container():

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("Spending breakdown")

        df = pd.DataFrame({
            "Category":expenses.keys(),
            "Amount":expenses.values()
        })

        st.bar_chart(df.set_index("Category"))

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- PARTNER FAIRNESS ---------- #

    partner_a_total = (
        housing*(housing_a/100)
        + food*(food_a/100)
        + transport*(transport_a/100)
        + loans*(loan_a/100)
    )

    partner_b_total = (
        housing*(housing_b/100)
        + food*(food_b/100)
        + transport*(transport_b/100)
        + loans*(loan_b/100)
    )

    partner_a_income_share = partner_a_income/income if income>0 else 0
    partner_b_income_share = partner_b_income/income if income>0 else 0

    partner_a_expense_share = partner_a_total/total_expenses if total_expenses>0 else 0
    partner_b_expense_share = partner_b_total/total_expenses if total_expenses>0 else 0

    with st.container():

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("⚖ Partner contribution balance")

        st.write(f"Partner A income share: {partner_a_income_share*100:.1f}%")
        st.write(f"Partner A expense share: {partner_a_expense_share*100:.1f}%")

        st.write(f"Partner B income share: {partner_b_income_share*100:.1f}%")
        st.write(f"Partner B expense share: {partner_b_expense_share*100:.1f}%")

        if partner_a_expense_share > partner_a_income_share + 0.1:
            st.warning("Partner A contributes more than income proportion.")

        elif partner_b_expense_share > partner_b_income_share + 0.1:
            st.warning("Partner B contributes more than income proportion.")

        else:
            st.success("Household contributions appear balanced.")

        st.markdown("</div>", unsafe_allow_html=True)