

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report

import pandas as pd
from SQL_connect.sqlconnecter import get_matches_at_dataframe, FETCH_ALL_MATCHES


from main import fetch_match, matches_formating, del_column, get_match_inf, formating_for_sql, PLAYER_ID


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

def get_picks_bans(match_id, game) -> list:
    result = []
    # Picks and Bans for the first match: [{'hero_id': 14, 'team': 0}, {'hero_id': 31, 'team': 0}, {'hero_id': 105, 'team': 1}, 
    # {'hero_id': 155, 'team': 0}, {'hero_id': 5, 'team': 1}, {'hero_id': 34, 'team': 0}, {'hero_id': 40, 'team': 0}, 
    # {'hero_id': 67, 'team': 1}, {'hero_id': 48, 'team': 1}, {'hero_id': 95, 'team': 0}, {'hero_id': 39, 'team': 1}]
    if match_id is None:
        print("match_id is None, cannot fetch picks and bans.")
        return []
    if match_id != game.get('match_id'):
        print(f"match_id {match_id} does not match game match_id {game.get('match_id')}.")
        return []
    
    for key, value in game.items():
        if key == "picks_bans":
                for pb in value:
                    if pb.get('is_pick') and pb.get('hero_id') is not None and pb.get('team') is not None:
                        result.append({
                            'hero_id': pb['hero_id'],
                            'team': pb['team']
                        })
                        
                return result  # Вернуть список пиков и банов для данного матча
    
    return []  # Вернуть список пиков и банов
# Основной блок для обучения модели при запуске этого файла напрямую
    
if __name__ == "__main__":
    matches_df = fetch_match(PLAYER_ID)
    matches_formating(matches_df)
    del_column(matches_df)
    # 1 match: [{'match_id': 8679277835, 'player_slot': 0, 'radiant_win': True, 'duration': 58, 
    # 'game_mode': 22, 'lobby_type': 7, 'hero_id': 34, 'start_time': '2026-02-06 03:31:47', 
    # 'kills': 7, 'deaths': 7, 'assists': 23, 'average_rank': 61, 'leaver_status': 0, 'hero_variant': 2}]
    
    

    # print(matches_df[:1])
    games = get_match_inf(matches_df)
    # 1 game (player): [{'match_id': 8679277835, 'account_id': 327729645, 'hero_id': 34, 'picks_bans': [{'is_pick': True, 'hero_id': 14, 'team': 0, 
    # 'order': 0}, {'is_pick': True, 'hero_id': 31, 'team': 0, 'order': 1}, {'is_pick': True, 'hero_id': 105, 'team': 1, 'order': 2}, 
    # {'is_pick': True, 'hero_id': 155, 'team': 0, 'order': 3}, {'is_pick': True, 'hero_id': 5, 'team': 1, 'order': 4}, 
    # {'is_pick': True, 'hero_id': 34, 'team': 0, 'order': 5}, {'is_pick': True, 'hero_id': 40, 'team': 0, 'order': 6}, 
    # {'is_pick': True, 'hero_id': 67, 'team': 1, 'order': 7}, {'is_pick': True, 'hero_id': 48, 'team': 1, 'order': 8}, 
    # {'is_pick': True, 'hero_id': 95, 'team': 0, 'order': 9}, {'is_pick': True, 'hero_id': 39, 'team': 1, 'order': 10}, 
    # {'is_pick': False, 'hero_id': 113, 'team': 0, 'order': 11}, {'is_pick': False, 'hero_id': 12, 'team': 0, 'order': 12}, 
    # {'is_pick': False, 'hero_id': 102, 'team': 0, 'order': 13}, {'is_pick': False, 'hero_id': 59, 'team': 0, 'order': 14}, 
    # {'is_pick': False, 'hero_id': 49, 'team': 0, 'order': 15}, {'is_pick': False, 'hero_id': 60, 'team': 1, 'order': 16}, 
    # {'is_pick': False, 'hero_id': 61, 'team': 1, 'order': 17}, {'is_pick': False, 'hero_id': 36, 'team': 1, 'order': 18}], 
    # 'benchmarks': {'gold_per_min': {'raw': 792, 'pct': 0.8324175824175825}, 'xp_per_min': {'raw': 1115, 'pct': 0.6917582417582417}, 
    # 'kills_per_min': {'raw': 0.1188118811881188, 'pct': 0.3269230769230769}, 'last_hits_per_min': {'raw': 11.168316831683168, 
    # 'pct': 0.8423076923076923}, 'hero_damage_per_min': {'raw': 891.5134370579915, 'pct': 0.5538461538461539}, 
    # 'hero_healing_per_min': {'raw': 0, 'pct': 0.6994505494505494}, 'tower_damage': {'raw': 263, 'pct': 0.5747252747252747}}, 
    # 'ability_upgrades_arr': [5150, 5150, 5152, 5152, 5152, 5153, 5152, 5150, 5150, 650, 1675, 650, 5153, 650, 650, 6152, 5153, 413, 1534, 
    # 1266, 8039, 1267, 7898], 'rank_tier': 61, 'item_0': 96, 'item_1': 277, 'item_2': 108, 'item_3': 610, 'item_4': 604, 'item_5': 202}]
        
    picks_bans = get_picks_bans(matches_df[0]['match_id'], games[0])
    print("Picks and Bans for the first match:", picks_bans)
    
    for game in games:
        match_id = game.get('match_id')
        picks_bans = get_picks_bans(match_id, game)
        # print(f"Picks and Bans for match {match_id}:", picks_bans)
        
    print(len(matches_df), "matches fetched.")
    print(len(games), "games fetched.")
    
    # train_model(df)
