import pandas as pd
import matplotlib.pyplot as plt


def draw_chart(ticker, start_date, override_date):
    df = pd.read_csv("us_stock.csv")
    df["Date"] = pd.to_datetime(df["Date"])

    # 시나리오 기간 필터링
    mask = (df["Date"] >= pd.to_datetime(start_date)) & (df["Date"] <= pd.to_datetime(override_date))
    df_filtered = df.loc[mask]

    # 해당 기간 만큼 차트 그리기
    plt.figure(figsize=(10, 4))
    plt.plot(df_filtered["Date"], df_filtered[ticker], marker="o")
    plt.title(f"{ticker} ({start_date} ~ {override_date})")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
