rates = {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.78,
    "JPY": 146.0,
}

def convert_usd(amount_usd: float):
    return {cur: amount_usd * rate for cur, rate in rates.items()}

if __name__ == "__main__":
    amount = float(input("Amount in USD: "))
    for currency, value in convert_usd(amount).items():
        print(f"{currency}: {value:.2f}")
