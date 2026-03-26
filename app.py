import streamlit as st
import pandas as pd

st.set_page_config(page_title="Finance Advisor", layout="centered")

st.title("💰 Personal Finance Advisor")

st.info("This tool provides financial insights for educational purposes and is not financial advice.")

# ---------- INCOME ---------- #

with st.expander("💵 Income", expanded=True):

    job = st.number_input("Job", 0, 200000, 25000)
    bonus = st.number_input("Bonus / commission", 0, 200000, 0)
    child_support = st.number_input("Child support", 0, 200000, 0)
    other_support = st.number_input("Other support", 0, 200000, 0)
    tax_return = st.number_input("Tax return", 0, 200000, 0)
    other_income = st.number_input("Other income", 0, 200000, 0)

income = job + bonus + child_support + other_support + tax_return + other_income

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

# ---------- TRANSPORT ---------- #

with st.expander("🚗 Transport"):

    transport_loan = st.number_input("Vehicle loan", 0, 200000, 0)
    fuel = st.number_input("Fuel", 0, 200000, 1500)
    parking = st.number_input("Parking", 0, 200000, 500)
    insurance = st.number_input("Insurance", 0, 200000, 800)
    tax = st.number_input("Vehicle tax", 0, 200000, 300)
    transport_other = st.number_input("Other transport", 0, 200000, 200)

transport = transport_loan + fuel + parking + insurance + tax + transport_other

# ---------- LOANS ---------- #

with st.expander("💳 Loans"):

    personal = st.number_input("Personal loan", 0, 200000, 1000)
    credits = st.number_input("Credits", 0, 200000, 500)
    loans_other = st.number_input("Other loans", 0, 200000, 200)

loans = personal + credits + loans_other

# ---------- LIFESTYLE ---------- #

with st.expander("🛍 Lifestyle"):

    food = st.number_input("Food", 0, 200000, 3000)
    restaurants = st.number_input("Restaurants", 0, 200000, 800)
    entertainment = st.number_input("Entertainment", 0, 200000, 500)
    clothes = st.number_input("Clothes", 0, 200000, 500)
    selfcare = st.number_input("Self-care", 0, 200000, 300)

lifestyle = food + restaurants + entertainment + clothes + selfcare

# ---------- SUBSCRIPTIONS ---------- #

with st.expander("📱 Subscriptions"):

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

# ---------- OTHER ---------- #

with st.expander("✈️ Other"):

    travel = st.number_input("Travel", 0, 200000, 500)
    charity = st.number_input("Charity", 0, 200000, 0)
    other = st.number_input("Other", 0, 200000, 1000)

other_total = travel + charity + other

# ---------- TOTAL ---------- #

total_expenses = housing + transport + loans + lifestyle + subscriptions + other_total
remaining = income - total_expenses
savings_rate = (remaining / income * 100) if income > 0 else 0

st.subheader("📊 Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total expenses", f"{total_expenses:,.0f} SEK")
col2.metric("Remaining", f"{remaining:,.0f} SEK")
col3.metric("Savings rate", f"{savings_rate:.1f}%")
