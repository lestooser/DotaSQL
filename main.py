# Импорт необходимых модулей
import SQL_connect.sqlconnecter as sqlc  # Модуль для работы с SQL базой данных
import Data.formating_data as formating
import Data.get_data as get_data
import SQL_connect.table_create as table_create

from dotenv import load_dotenv
import os
import pandas as pd
import polars as pl

# Глобальная константа с ID игрока, которую можно изменить для другого игрока
load_dotenv()

PLAYER_ID2 = os.getenv("PLAYER_ID")
# PLAYER_ID ="327729645"

def get_data_from_matches():
    try:
        matches = get_data.fetch_match(PLAYER_ID2)
        # print(f"{matches}")
        # input("Press Enter to continue...")
        
    except Exception as e: 
        print(f"Error fetching matches: {e}")
        return []
    try:
        matches = formating.matches_formating(matches)
        matches = formating.del_column(matches)
        # print(type(matches))
        # print(json.dumps(matches[:5], indent=2))
        return matches
    except Exception as e: 
            print(f"Error formatting matches: {e}")
            return []

def get_data_from_games(matches, between=[0,100], match_id=None):
    try:
        games = get_data.get_match_inf(matches, between=between, match_id=match_id)
        return games
    except Exception as e:
        print(f"Error fetching games: {e}")
        return []

     
# Основной блок, который выполняется только при запуске этого файла напрямую (не при импорте)
if __name__ == "__main__":
    # arr = [1, 4, [45,6,4,2,34], ["ge","few", "fe"], "wer", True]
    # for i in arr: print(type(i))
    
    # print(f"{PLAYER_ID}")
    # matches = get_data_from_matches()
    # last_match_id = sqlc.FETCH_LATEST_MATCHES(limit=1)
    # games = get_data_from_games(matches)
    # df = sqlc.get_matches_at_dataframe(limit=1)
    # print(df)

    table_create.matches_creation(get_data_from_matches(), table_name="matches2")
    table_create.matches_inserting(get_data_from_matches(), table_name="matches2")
                      
