import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt

# 📥 Load dataset
df = pd.read_csv("emails.csv")

# 🔧 Feature Engineering: detect URLs
def has_url(text):
    return 1 if re.search(r"http[s]?://", text) else 0

df["has_url"] = df["text"].apply(has_url)

# 🎯 Labels
df["label"] = df["label"].map({"safe": 0, "phishing": 1})

# ✂️ Split data
X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["label"], test_size=0.2, random_state=42
)

# 🧠 Text Vectorization (TF-IDF)
vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# ➕ Add URL feature
X_train_final = pd.concat(
    [pd.DataFrame(X_train_tfidf.toarray()), df.loc[X_train.index, ["has_url"]].reset_index(drop=True)],
    axis=1
)

X_test_final = pd.concat(
    [pd.DataFrame(X_test_tfidf.toarray()), df.loc[X_test.index, ["has_url"]].reset_index(drop=True)],
    axis=1
)

# 🤖 Model
model = LogisticRegression()
model.fit(X_train_final, y_train)

# 🔍 Predictions
y_pred = model.predict(X_test_final)

# 📊 Evaluation
accuracy = accuracy_score(y_test, y_pred)
print(f"\n✅ Accuracy: {accuracy:.2f}")

print("\n📋 Classification Report:")
print(classification_report(y_test, y_pred))

# 📉 Confusion Matrix
cm = confusion_matrix(y_test, y_pred)

sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Safe", "Phishing"],
            yticklabels=["Safe", "Phishing"])

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

# 🧪 Test with custom email
def predict_email(text):
    url_feature = has_url(text)

    text_tfidf = vectorizer.transform([text]).toarray()
    final_input = pd.concat(
        [pd.DataFrame(text_tfidf), pd.DataFrame([[url_feature]])],
        axis=1
    )

    prediction = model.predict(final_input)[0]

    return "Phishing ⚠️" if prediction == 1 else "Safe ✅"


# Example test
test_email = input("\nEnter email text to test: ")
print("Prediction:", predict_email(test_email))
