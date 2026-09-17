import requests
import pandas as pd

url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"

params = {
    "vs_currency": "usd",
    "days": "30"
}

response = requests.get(url, params=params)

data = response.json()

prices = data["prices"]

df = pd.DataFrame(prices, columns=["timestamp", "price"])

df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

df["price_change"] = df["price"].pct_change() * 100

df["moving_average"] = df["price"].rolling(24).mean()

df["above_average"] = df["price"] > df["moving_average"]

df["crossover"] = (
    df["above_average"] != df["above_average"].shift(1)
)

df.loc[df.index[0], "crossover"] = False

df["previous_above"] = df["above_average"].shift(1).fillna(False)

df["crossed_up"] = (~df["previous_above"]) & df["above_average"]

df["crossed_down"] = df["previous_above"] & (~df["above_average"])

df["price_6h_later"] = df["price"].shift(-6)

df["return_6h"] = (
    (df["price_6h_later"] - df["price"])
    / df["price"]
) * 100

df["future_price"] = df["price"].shift(-6)

df["target"] = (df["future_price"] > df["price"]).astype(float)

df.loc[df["future_price"].isna(), "target"] = float("nan")

cross_up_results = df[df["crossed_up"]]

print(df[["price", "price_6h_later", "target"]].head(10))

print(cross_up_results[[
    "timestamp",
    "price",
    "price_6h_later",
    "return_6h"
]])

print()
print("Average 6-hour return after crossed up:",
      cross_up_results["return_6h"].mean(), "%")

print(df[["timestamp", "price", "moving_average", "above_average", "crossover"]].tail(20))

print(df[["price", "moving_average"]].tail())

print(df[["price", "moving_average", "above_average"]].tail(10))

print(df[df["crossed_up"]][["timestamp", "price", "moving_average"]])
print()
print(df[df["crossed_down"]][["timestamp", "price", "moving_average"]])

print("Crossed up:", df["crossed_up"].sum())
print("Crossed down:", df["crossed_down"].sum())

volatility = df["price_change"].std()

print()
print("Hourly volatility:", volatility, "%")

highest = df["price"].max()
lowest = df["price"].min()
average = df["price"].mean()

start_price = df["price"].iloc[0]
end_price = df["price"].iloc[-1]

change = ((end_price - start_price) / start_price) * 100

df["return_6h_past"] = df["price"].pct_change(6)

df["volatility_24h"] = df["price_change"].rolling(24).std()

df["ma_distance"] = (
    (df["price"] - df["moving_average"])
    / df["moving_average"]
)

features = [
    "price_change",
    "return_6h_past",
    "volatility_24h",
    "ma_distance",
    "crossed_up",
    "crossed_down"
]

model_data = df.dropna(subset=features + ["target"]).copy()

print()
print("Highest price:", highest)
print("Lowest price:", lowest)
print("Average price:", average)
print("30-day change:", change, "%")

print(df.head())
print()
print(df.tail())

print()
print("Average hourly change:", df["price_change"].mean(), "%")
print("Largest hourly increase:", df["price_change"].max(), "%")
print("Largest hourly decrease:", df["price_change"].min(), "%")

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

model_data = df.dropna(subset=features + ["target"]).copy()

X = model_data[features]
y = model_data["target"]

print()
print("FEATURES ACTUALLY USED:")
print(features)


split = int(len(model_data) * 0.8)

X_train = X.iloc[:split]
X_test = X.iloc[split:]

y_train = y.iloc[:split]
y_test = y.iloc[split:]

model = make_pipeline(
    StandardScaler(),
    LogisticRegression(max_iter=1000)
)

model.fit(X_train, y_train)

probabilities = model.predict_proba(X_test)

probabilities = model.predict_proba(X_test)

threshold = 0.65

predictions = (probabilities[:, 1] >= threshold).astype(float)

print()
print("EXAMPLE PREDICTION PROBABILITIES")

for i in range(10):
    print(
        "Actual:", y_test.iloc[i],
        "| Down probability:", round(probabilities[i][0], 3),
        "| Up probability:", round(probabilities[i][1], 3)
    )

print()
print("PREDICTION BREAKDOWN")
print("Predicted down:", (predictions == 0).sum())
print("Predicted up:", (predictions == 1).sum())

print()
print("Actual down:", (y_test == 0).sum())
print("Actual up:", (y_test == 1).sum())

from sklearn.metrics import confusion_matrix

matrix = confusion_matrix(y_test, predictions)

print()
print("CONFUSION MATRIX")
print(matrix)

from sklearn.metrics import classification_report

print()
print("CLASSIFICATION REPORT")
print(classification_report(y_test, predictions))

accuracy = accuracy_score(y_test, predictions)

baseline = int(y_train.mean() >= 0.5)

baseline_predictions = [baseline] * len(y_test)

baseline_accuracy = accuracy_score(
    y_test,
    baseline_predictions
)

print("Baseline accuracy:", baseline_accuracy)
print("Baseline accuracy %:", baseline_accuracy * 100)

print()
print("==============================")
print("FIRST PREDICTION MODEL")
print("==============================")
print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))
print("Accuracy:", accuracy)
print("Accuracy %:", accuracy * 100)

import matplotlib.pyplot as plt

plt.plot(df["timestamp"], df["price"])
plt.plot(df["timestamp"], df["moving_average"])

plt.title("Bitcoin Price vs 24-Hour Moving Average")
plt.xlabel("Date")
plt.ylabel("Price ($)")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()