import streamlit as st
import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("📈 Stock Correlation Matrix Web App")

tickers = st.text_input(
    "Enter ticker symbols separated by commas (e.g. AAPL, MSFT, GOOGL):",
    value="AAPL, MSFT, GOOGL, SPY"
)

start_date = st.date_input("Start Date", pd.to_datetime("2022-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("2023-01-01"))

if st.button("Show Correlation Matrix"):
    try:
        tickers_list = [t.strip().upper() for t in tickers.split(",")]
        data = yf.download(tickers_list, start=start_date, end=end_date)
        adj_close = data['Close']
        corr = adj_close.corr()
        clean_corr = corr.dropna(axis=0, how='all').dropna(axis=1, how='all')
        rounded_corr = clean_corr.round(2)
        st.write("### Correlation Matrix")
        st.dataframe(rounded_corr)
        fig, ax = plt.subplots(figsize=(12, 12))
        sns.heatmap(
            rounded_corr, annot=True, fmt=".2f", cmap="coolwarm",
            vmin=-1, vmax=1, linewidths=0, cbar=True, ax=ax
        )
        ax.set_title("Stock Correlation Matrix", fontsize=16, pad=20)
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error: {e}")
