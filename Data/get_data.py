# Импорт необходимых модулей
import requests  # Для отправки HTTP-запросов
import json      # Для работы с JSON данными
import SQL_connect.sqlconnecter as sqlc  # Модуль для работы с SQL базой данных
from datetime import datetime  # Для работы с датами и временем
from dotenv import load_dotenv
import os
import pandas as pd
import polars as pl


def fetch_match(player_id):
    """
    Функция для получения списка матчей игрока из OpenDota API.

    Аргументы:
    player_id (str): ID игрока в Dota 2.

    Возвращает:
    list: Список словарей с информацией о матчах.

    Исключения:
    Exception: Если запрос к API завершился неудачей (статус код не равен 200).
    """
    # Формируем URL для запроса к API OpenDota
    url = f'https://api.opendota.com/api/players/{player_id}/matches'
    # Устанавливаем заголовки, указывая, что ожидаем ответ в формате JSON
    headers = {"Accept": "application/json"}
    # Отправляем GET-запрос к API
    response = requests.get(url, headers=headers)
    # Проверяем статус ответа: если не 200 (не успех), выбрасываем исключение
    if response.status_code != 200:
        raise Exception(f"API request failed with status code: {response.status_code}")
    # Возвращаем данные ответа в формате JSON
    
    return response.json()

def get_match_inf(matches, between=[0,100], match_id=None):
    """Получает информацию о матчах из OpenDota API"""
    #Из всей информации нужно получить строки: match_id (bigint), 
    # account_id (bigint), 
    # hero_id (int), 
    # picks_bans(list), 
    # benchmarks(list), 
    # ability_upgrades_arr(list) 
    # "item_0": 180,
    #   "item_1": 254,
    #   "item_2": 232,
    #   "item_3": 1802,
    #   "item_4": 108,
    #   "item_5": 1107
    # rank_tier (1 цифра - ранг, 2 - звезды. 
    # 1 - рекрут
    # 2 - страж
    # 3 - рыцарь
    # 4 - герой
    # 5 - легенда 
    # 6 - властелин
    # 7 - божество
    # 8 - титан)
    results = []
    def keep_only_keys(data, keys_to_keep):
        """Рекурсивно оставляет только указанные ключи"""
        if isinstance(data, dict):
            return {k: v for k, v in data.items() if k in keys_to_keep}
        elif isinstance(data, list):
            return [keep_only_keys(item, keys_to_keep) for item in data]
        return data
    
    # Ваш список URL для запросов

    for match in matches[between[0]:between[1]]:
        if 'match_id' in match:
            match_id = match["match_id"]
            # print(f"\nОбрабатываем матч ID: {match_id}")
            url = (f"https://api.opendota.com/api/matches/{match_id}")

    
        headers = {"Accept": "application/json"}
        
        # Обрабатываем каждый URL
        try:
            print(f"Запрашиваем: {url}")
            response = requests.get(url, headers=headers, timeout=10)
                
            if response.status_code != 200:
                print(f"Ошибка {response.status_code} для URL: {url}")
                if response.status_code == 429:
                    print("   Превышен лимит запросов!")
                elif response.status_code == 404:
                    print("   Матч не найден!")
                continue

                
                # Получаем JSON данные
            data = response.json()
                
                # Фильтруем данные
                
            if "players" in data and data["players"]:
                for player in data['players']:
                    # print("ТЕКУЩИЙ ИГРОК --------- " , player.get('account_id'), "\n\n")
                    result = {
                            "match_id": data.get("match_id"),
                            "account_id": player.get("account_id"),
                            "hero_id": player.get("hero_id"), 
                            "picks_bans": data.get("picks_bans"), 
                            "benchmarks": player.get("benchmarks"),
                            "ability_upgrades_arr": player.get ("ability_upgrades_arr"), 
                            "rank_tier": player.get("rank_tier"), 
                            "item_0": player.get("item_0"), 
                            "item_1": player.get("item_1"), 
                            "item_2": player.get("item_2"), 
                            "item_3": player.get("item_3"), 
                            "item_4": player.get("item_4"), 
                            "item_5": player.get("item_5")
                        }
                    results.append(result)
                        # filtered_data = keep_only_keys(data, keys_to_keep)
                
                # Добавляем в результаты
                # all_results.append(filtered_data)
                
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")
        except json.JSONDecodeError as e:
            print(f"Ошибка парсинга JSON: {e}")
    
    return results
