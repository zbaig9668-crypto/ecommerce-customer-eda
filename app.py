import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="E-commerce Customer Analysis", page_icon="🛍️", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("ecommerce_customers.csv")

df = load_data()
numeric_cols = df.select_dtypes(include="number").columns.tolist()

st.title("🛍️ E-commerce Customer Behavior & Purchase Patterns")
st.write("Explore customer engagement, membership length, and yearly spending in an online store.")

st.sidebar.header("Dashboard Filters")
min_membership = float(df["Length of Membership"].min())
max_membership = float(df["Length of Membership"].max())
membership_range = st.sidebar.slider(
    "Length of Membership (years)",
    min_value=min_membership,
    max_value=max_membership,
    value=(min_membership, max_membership)
)
min_spend = float(df["Yearly Amount Spent"].min())
max_spend = float(df["Yearly Amount Spent"].max())
spend_range = st.sidebar.slider(
    "Yearly Amount Spent",
    min_value=min_spend,
    max_value=max_spend,
    value=(min_spend, max_spend)
)

filtered = df[
    df["Length of Membership"].between(*membership_range)
    & df["Yearly Amount Spent"].between(*spend_range)
].copy()

st.caption(f"Showing {len(filtered):,} of {len(df):,} customers after applying filters.")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Customers", f"{len(filtered):,}")
c2.metric("Average yearly spend", f"${filtered['Yearly Amount Spent'].mean():,.2f}" if len(filtered) else "—")
c3.metric("Average membership", f"{filtered['Length of Membership'].mean():.2f} years" if len(filtered) else "—")
c4.metric("Highest yearly spend", f"${filtered['Yearly Amount Spent'].max():,.2f}" if len(filtered) else "—")

if filtered.empty:
    st.warning("No customers match these filters. Widen one or both ranges.")
    st.stop()

st.header("Customer Analysis")
col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots()
    ax.hist(filtered["Yearly Amount Spent"], bins=20, edgecolor="black")
    ax.set_title("Distribution of Yearly Amount Spent")
    ax.set_xlabel("Yearly Amount Spent ($)")
    ax.set_ylabel("Number of Customers")
    st.pyplot(fig)
    plt.close(fig)

with col2:
    fig, ax = plt.subplots()
    sns.scatterplot(data=filtered, x="Time on App", y="Yearly Amount Spent", ax=ax)
    ax.set_title("Time on App vs Yearly Amount Spent")
    ax.set_xlabel("Time on App")
    ax.set_ylabel("Yearly Amount Spent ($)")
    st.pyplot(fig)
    plt.close(fig)

col3, col4 = st.columns(2)
with col3:
    fig, ax = plt.subplots()
    sns.scatterplot(data=filtered, x="Time on Website", y="Yearly Amount Spent", ax=ax)
    ax.set_title("Time on Website vs Yearly Amount Spent")
    ax.set_xlabel("Time on Website")
    ax.set_ylabel("Yearly Amount Spent ($)")
    st.pyplot(fig)
    plt.close(fig)

with col4:
    fig, ax = plt.subplots()
    ax.hist(filtered["Length of Membership"], bins=20, edgecolor="black")
    ax.set_title("Distribution of Membership Length")
    ax.set_xlabel("Length of Membership (years)")
    ax.set_ylabel("Number of Customers")
    st.pyplot(fig)
    plt.close(fig)

st.subheader("Correlation Heatmap")
fig, ax = plt.subplots(figsize=(9, 6))
sns.heatmap(filtered[numeric_cols].corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
ax.set_title("Correlation Between Numeric Variables")
st.pyplot(fig)
plt.close(fig)

st.subheader("App vs Website Engagement")
comparison = pd.DataFrame({
    "Channel": ["App", "Website"],
    "Average time": [filtered["Time on App"].mean(), filtered["Time on Website"].mean()],
    "Correlation with yearly spend": [
        filtered["Time on App"].corr(filtered["Yearly Amount Spent"]),
        filtered["Time on Website"].corr(filtered["Yearly Amount Spent"])
    ]
})
st.dataframe(comparison, use_container_width=True)
st.write("Compare the correlation values to see which channel's time is more strongly associated with yearly spending. Correlation does not prove causation.")

st.header("Main Findings")
corr = filtered[numeric_cols].corr()["Yearly Amount Spent"].drop("Yearly Amount Spent")
strongest = corr.abs().idxmax()
st.markdown(
    f"""
    - The filtered dashboard currently contains **{len(filtered)} customers**.
    - The average yearly spend is **${filtered['Yearly Amount Spent'].mean():,.2f}**.
    - The strongest numeric relationship with yearly spending is **{strongest}** (correlation: **{corr[strongest]:.2f}**).
    - Use the app and website engagement charts to compare the two channels.
    - The company can prioritize improvements to the channel and customer experience most closely associated with spending.
    """
)

if st.checkbox("Show raw customer data"):
    st.dataframe(filtered, use_container_width=True)
