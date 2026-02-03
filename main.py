# Импорт необходимых модулей
import requests  # Для отправки HTTP-запросов
import json      # Для работы с JSON данными
import sqlconnecter as sqlc  # Модуль для работы с SQL базой данных
from datetime import datetime  # Для работы с датами и временем
from dotenv import load_dotenv
import os
import pandas as pd
import polars as pl

# Глобальная константа с ID игрока, которую можно изменить для другого игрока
load_dotenv()

PLAYER_ID2 = os.getenv("PLAYER_ID")
PLAYER_ID ="327729645"

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

def format_timestamp(timestamp):
    """
    Функция для преобразования UNIX timestamp в читаемую строку даты и времени.

    Аргументы:
    timestamp (int): UNIX timestamp (секунды с 1970-01-01).

    Возвращает:
    str: Строка в формате 'YYYY-MM-DD HH:MM:SS'.
    """
    # Преобразуем timestamp в объект datetime, затем в строку
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def matches_formating(matches):
    """
    Функция для форматирования данных матчей: преобразование duration в минуты и start_time в читаемый формат.

    Аргументы:
    matches (list): Список словарей матчей.

    Возвращает:
    None: Функция изменяет список на месте.
    """
    # Проходим по каждому матчу в списке
    for match in matches:
        # Если в матче есть поле 'duration', преобразуем из секунд в минуты
        if 'duration' in match:
            match['duration'] = match['duration'] // 60  # Целочисленное деление для получения минут
        # Если есть 'start_time', преобразуем timestamp в строку
        if 'start_time' in match:
            match['start_time'] = format_timestamp(match['start_time'])

def del_column(matches):
    for match in matches:
        if 'version' in match:
            del match['version']
        if 'party_size' in match:
            del match['party_size']

def get_match_inf(matches: int):
    import requests

def get_match_inf(matches):
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

    for match in matches[:2]:
        if 'match_id' in match:
            match_id = match["match_id"]
            print(f"\nОбрабатываем матч ID: {match_id}")
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
                    print("ТЕКУЩИЙ ИГРОК --------- " , player.get('account_id'), "\n\n")
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
    


def formating_for_sql(matches):
    """
    Функция преобразовывает колонки из json файла в dict для SQL, по которому строится запрос
    Аргументы:
    matches (list): Список словарей матчей.

    Возвращает:
    types_dict: Словарь, в котором есть все столбцы и их типы.
    """
    if not matches:
        raise (f"Данные для обработки не могут быть пустыми")
        
    first_item = matches[0]
    schema = {}
    
    #Составляем словарь ключ-тип
    for match in first_item:
        types_dict = {key: type(value).__name__ for key,value in match.items()}
    
    #форматируем получившиеся типы
    for key, value in types_dict.items():
        #если элемент является списком
        if isinstance(value, list):
            if value:
                #Определить уровеьн вложенности списков
                def get_list_depth(lst):
                    depth = 0
                    current = lst
                    while (isinstance(current, list) and current):
                        depth += 1
                        current = current[0]
                    return depth
                depth = get_list_depth(value)
                
                if depth == 1:
                    #Простой список
                    elem_type = type(value[0]).__name__
                    match elem_type:
                        case 'str': types_dict[key] == "TEXT[]"
                        case 'int': types_dict[key] == "INTEGER[]"
                        case 'float': types_dict[key] == "FLOAT[]"
                        case _: types_dict[key] = "JSONB"
                else:  types_dict[key] = "JSONB"
                
        elif value == "str": types_dict[key]="TEXT"
        elif value == "dict": types_dict[key] == "JSONB"
        
    return types_dict
# Основной блок, который выполняется только при запуске этого файла напрямую (не при импорте)
if __name__ == "__main__":
    # arr = [1, 4, [45,6,4,2,34], ["ge","few", "fe"], "wer", True]
    # for i in arr: print(type(i))
    
    # print(f"{PLAYER_ID}")
    try:
        matches = fetch_match(PLAYER_ID) 
        matches_formating(matches)
        del_column(matches)
        
        # print(json.dumps(matches[:5], indent=2))
    except Exception as e: 
            print(f"Error fetching matches: {e}")
    try:        
        games = get_match_inf(matches)
    except Exception as e:
        print(f"Error fetch games: {e}")
        
    df = pd.DataFrame(games)
    df.fillna(0, inplace=True)
    print(f"DataFrame создан: {df.shape[0]} строк, {df.shape[1]} колонок")
         
    # df = pd.read_json(games_new, orient='records')    
    # print(df)
    # types_dict = formating_for_sql(matches)

    # try:
    #     sqlc.create_table_with_name(table="onegame", column=types_dict)
    # except Exception as e:
    #     print(f"Error creation table with name: {e}" )
      
      
    # try: 
    #     sqlc.create_table()
    # except Exception as e:
    #     print(f"Error creating table: {e}")

    # try:
    #     # Вставляем данные матчей в базу данных
    #     sqlc.INSERT_MATCHES(matches)
    # except Exception as e:
    #     print(f"Error inserting matches: {e}")

