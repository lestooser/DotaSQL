# Импорт необходимых модулей
import requests  # Для отправки HTTP-запросов
import json      # Для работы с JSON данными
import sqlconnecter as sqlc  # Модуль для работы с SQL базой данных
from datetime import datetime  # Для работы с датами и временем

# Глобальная константа с ID игрока, которую можно изменить для другого игрока
PLAYER_ID = '327729645'

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



# Основной блок, который выполняется только при запуске этого файла напрямую (не при импорте)
if __name__ == "__main__":
    try: 
        sqlc.create_table()
    except Exception as e:
        print(f"Error creating table: {e}")
    
    

    try:
        # Получаем матчи для игрока
        matches = fetch_match(PLAYER_ID)
        # Форматируем данные матчей
        matches_formating(matches)
        try:
            # Вставляем данные матчей в базу данных
            sqlc.INSERT_MATCHES(matches)
        except Exception as e:
            print(f"Error inserting matches: {e}")
        
        # Выводим первые 5 матчей в формате JSON с отступами для читаемости
        print(json.dumps(matches[:5], indent=2))
    except Exception as e:
        # В случае ошибки выводим сообщение об ошибке
        print(f"Error fetching matches: {e}")
