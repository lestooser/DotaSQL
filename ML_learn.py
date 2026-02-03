
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report

import pandas as pd
from sqlconnecter import FETCH_ALL_MATCHES




def train_model(df):
    features = df[
        ['duration', 'kills', 'deaths', 'assists',
         'average_rank', 'leaver_status', 'party_size']
    ]
    target = df['radiant_win']

    scaler = MinMaxScaler()
    features_scaled = scaler.fit_transform(features)

    X_train, X_test, y_train, y_test = train_test_split(
        features_scaled, target, test_size=0.2, random_state=42
    )

    LogisticRegression_model(X_train, X_test, y_train, y_test)
    DecisionTree_model(X_train, X_test, y_train, y_test)


def LogisticRegression_model(X_train, X_test, y_train, y_test):
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    print("Logistic Regression Report:\n",
          classification_report(y_test, preds))

    print("Accuracy:", model.score(X_test, y_test))


def DecisionTree_model(X_train, X_test, y_train, y_test):
    tree = DecisionTreeClassifier(random_state=42)
    tree.fit(X_train, y_train)

    preds = tree.predict(X_test)
    print("Decision Tree Report:\n",
          classification_report(y_test, preds))

    print("Accuracy:", tree.score(X_test, y_test))


# Основной блок для обучения модели при запуске этого файла напрямую
    
if __name__ == "__main__":
    data = FETCH_ALL_MATCHES()
    df = pd.DataFrame(data, columns=[
        "match_id",
        "player_slot",
        "radiant_win",
        "duration",
        "game_mode",
        "lobby_type",
        "hero_id",
        "start_time",
        "version",
        "kills",
        "deaths",
        "assists",
        "average_rank",
        "leaver_status",
        "party_size",
        "hero_variant"
    ])
    train_model(df)
    