from sklearn.ensemble import IsolationForest
import numpy as np


def extract_features(query: str):
    q = query.lower()
    length = len(query)
    word_count = len(q.split())

    suspicious_words = [
        "ignore",
        "bypass",
        "reveal",
        "admin",
        "dump",
        "show all data",
        "system prompt",
        "override",
        "disable security",
        "leak",
        "exploit",
        "sqlmap",
        "drop table"
    ]

    keyword_count = sum(word in q for word in suspicious_words)

    special_char_count = sum(1 for ch in query if not ch.isalnum() and not ch.isspace())

    return [length, word_count, keyword_count, special_char_count]


# Mixed normal training data:
# include both SOC/security queries and banking-support queries
X_train = np.array([
    extract_features("How do I investigate SSH failures?"),
    extract_features("What are common indicators of brute force attacks?"),
    extract_features("How do I review firewall logs?"),
    extract_features("How can I identify suspicious outbound traffic?"),
    extract_features("What steps should I take after repeated login failures?"),
    extract_features("I forgot my password"),
    extract_features("My transfer is pending"),
    extract_features("My card is missing"),
    extract_features("I saw a transaction I did not make"),
    extract_features("How do I download my bank statement?"),
    extract_features("OTP not received"),
    extract_features("How can I block my debit card?"),
    extract_features("Refund still not received"),
    extract_features("Login not working"),
])

model = IsolationForest(
    contamination=0.1,
    random_state=42
)
model.fit(X_train)


def is_anomalous(query: str) -> bool:
    features = np.array([extract_features(query)])
    prediction = model.predict(features)
    return prediction[0] == -1