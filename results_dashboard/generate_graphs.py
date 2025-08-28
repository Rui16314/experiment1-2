import pandas as pd
import matplotlib.pyplot as plt
import os

# Create output folder for graphs
os.makedirs("results_dashboard/graphs", exist_ok=True)

# List of session CSVs (replace with actual filenames)
session_files = {
    "Session1": "first_price_auction.csv",
    "Session2": "repeated_first_price_fixed.csv",
    "Session3": "first_price_with_chat.csv",
    "Session4": "second_price_auction.csv",
    "Session5": "repeated_second_price_fixed.csv",
    "Session6": "second_price_with_chat.csv"
}

# Store average revenues for Graph 7
average_revenues = {}

for session, file in session_files.items():
    df = pd.read_csv(file)

    # Graph 1-a: Average bid vs valuation
    avg_bids = df.groupby("valuation")["bid"].mean()
    plt.figure()
    avg_bids.plot(kind="line", title=f"{session} – Avg Bid vs Valuation")
    plt.xlabel("Valuation")
    plt.ylabel("Average Bid")
    plt.savefig(f"results_dashboard/graphs/{session}_graph1a.png")
    plt.close()

    # Graph 1-b: Average bid for valuation range 30–39
    range_df = df[(df["valuation"] >= 30) & (df["valuation"] <= 39)]
    avg_range = range_df.groupby("valuation")["bid"].mean()
    plt.figure()
    avg_range.plot(kind="bar", title=f"{session} – Avg Bid (Valuation 30–39)")
    plt.xlabel("Valuation")
    plt.ylabel("Average Bid")
    plt.savefig(f"results_dashboard/graphs/{session}_graph1b.png")
    plt.close()

    # Graph 2: Individual student’s bid when valuation = 50
    student_df = df[(df["participant_code"] == "P001") & (df["valuation"] == 50)]
    if not student_df.empty:
        avg_bid_50 = student_df["bid"].mean()
        plt.figure()
        plt.bar([50], [avg_bid_50])
        plt.title(f"{session} – Student P001 Avg Bid at Valuation 50")
        plt.xlabel("Valuation")
        plt.ylabel("Bid")
        plt.savefig(f"results_dashboard/graphs/{session}_graph2.png")
        plt.close()

    # Graph 3: Revenue per round
    revenue = df.groupby("round_number")["opponent_bid"].mean()
    plt.figure()
    revenue.plot(title=f"{session} – Revenue per Round")
    plt.xlabel("Round")
    plt.ylabel("Average Revenue")
    plt.savefig(f"results_dashboard/graphs/{session}_graph3.png")
    plt.close()

    # Graph 4: Overall average revenue
    avg_rev = df["opponent_bid"].mean()
    average_revenues[session] = avg_rev

# Graph 5: All Graph 1-a on one page
plt.figure()
for session in session_files:
    df = pd.read_csv(session_files[session])
    avg_bids = df.groupby("valuation")["bid"].mean()
    plt.plot(avg_bids, label=session)
plt.title("Graph 5 – Avg Bid vs Valuation Across Sessions")
plt.xlabel("Valuation")
plt.ylabel("Average Bid")
plt.legend()
plt.savefig("results_dashboard/graphs/graph5_all_sessions.png")
plt.close()

# Graph 6: All Graph 3 on one page
plt.figure()
for session in session_files:
    df = pd.read_csv(session_files[session])
    revenue = df.groupby("round_number")["opponent_bid"].mean()
    plt.plot(revenue, label=session)
plt.title("Graph 6 – Revenue per Round Across Sessions")
plt.xlabel("Round")
plt.ylabel("Average Revenue")
plt.legend()
plt.savefig("results_dashboard/graphs/graph6_all_sessions.png")
plt.close()

# Graph 7: Overall average revenue comparison
plt.figure()
plt.bar(average_revenues.keys(), average_revenues.values())
plt.title("Graph 7 – Overall Avg Revenue Across Sessions")
plt.xlabel("Session")
plt.ylabel("Average Revenue")
plt.savefig("results_dashboard/graphs/graph7_avg_revenue.png")
plt.close()

print("✅ All graphs generated and saved in results_dashboard/graphs/")

