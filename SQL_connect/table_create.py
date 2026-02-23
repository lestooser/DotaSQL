# Импорт необходимых модулей
import requests  # Для отправки HTTP-запросов
import json      # Для работы с JSON данными

import SQL_connect.sqlconnecter as sqlc  # Модуль для работы с SQL базой данных
import Data.formating_data as formating
import Data.get_data as get_data
from main import get_data_from_matches, get_data_from_games

import logging as log


logger = log.getLogger(__name__)
log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


matches = get_data_from_matches()

def games_creation(matches, table_name="oneOngame"):
    """
        Создаем таблицу для хранения информации о матчах, если она еще не существует, при этом определяя тип аргументов.

    Args:
        matches (_type_): _description_
    """
    try:
        logger.info(f"Starting {table_name} table creation.")
        games = get_data_from_games(matches, between=[0,1])
        types_dict = formating.formating_for_sql(games)
        sqlc.create_table_with_name(table=table_name, column=types_dict)
    except Exception as e:
        logger.error(f"Error creation table for {table_name} with name: {e}" )

def games_inserting(matches, table_name="oneOngame"):
    """
        Вставляем данные о каждом матче в базу данных, по одному матчу за раз, с интервалом между ними 1-2 секунды, чтобы не перегружать API и базу данных.

    Args:
        matches (_type_): _description_
    """
    try:
        logger.info(f"Starting to insert {table_name} data into the database.")
        for i in range(0, len(matches), 2):
            games = []
            
            if 'match_id' not in matches[i]:
                logger.warning(f"Match at index {i} is missing 'match_id': {matches[i]}")
                
            games = get_data_from_games(matches, between=[i,i+1])
            types_dict = formating.formating_for_sql(games)
            
            try:
                logger.info(f"Inserting games for matches index range: {i} to {i+1}")
                for game in games:
                     # Подготовка данных для SQL: сериализация JSONB полей
                    game_for_sql = game.copy()
                    for key, value in game_for_sql.items():
                        if key in types_dict and types_dict[key] == "JSONB":
                            game_for_sql[key] = json.dumps(value)
                    sqlc.insert_into_db(table=table_name, data=game_for_sql)
            except Exception as e:
                logger.error(f"Error inserting {table_name}: {e}")
    except Exception as e:
        logger.error(f"Error fetch {table_name}: {e}")

def matches_creation(matches, table_name="matches"):
    """
        Создаем таблицу для хранения информации обо всех играх аккаунта, если она еще не существует, при этом определяя тип аргументов.
    Args:        
        matches (_type_): _description_
        table_name (str, optional): _description_. Defaults to "matches".
    """
    try:
        logger.info(f"Starting {table_name} table creation.")
        types_dict = formating.formating_for_sql(matches)
        sqlc.create_table_with_name(table=table_name, column=types_dict)
        # sqlc.create_table
    except Exception as e:
        logger.error(f"Error creation table with name: {e}" )

def matches_inserting(matches, table_name="matches"):
    """
    Вставляем данные обо всех играх аккаунта в базу данных

    Args:
        matches (_type_): _description_
        table_name (str, optional): _description_. Defaults to "matches".
    """
    try:
        for match in matches:
            sqlc.insert_into_db(table=table_name, data=match)
        logger.info(f"Successfully inserted {len(matches)} matches into {table_name}")
    except Exception as e:
        logger.error(f"Error inserting matches: {e}")


if __name__ == "__main__":
    logger.info("Starting the process of creating tables and inserting data.")
    matches_creation(matches)
    
    logger.info("Finished creating matches table. Starting to insert matches data.")
    matches_inserting(matches)
    
    logger.info("Finished inserting matches data. Starting to create games table and insert games data.")
    games_creation(matches)
    
    logger.info("Finished creating games table and inserting games data.")
    games_inserting(matches)
   
   
# print(json.dumps(matches[:1], indent=2))
# print("\n\n",json.dumps(games[:1], indent=2))



