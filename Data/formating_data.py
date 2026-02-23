# Импорт необходимых модулей
import SQL_connect.sqlconnecter as sqlc  # Модуль для работы с SQL базой данных
from datetime import datetime  # Для работы с датами и временем


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
    return matches

def del_column(matches):
    for match in matches:
        if 'version' in match:
            del match['version']
        if 'party_size' in match:
            del match['party_size']
    return matches

def formating_for_sql(matches):
    """
    Функция преобразовывает колонки из json файла в dict для SQL, по которому строится запрос
    
    Аргументы:
    matches (list): Список словарей матчей.

    Возвращает:
    types_dict: Словарь, в котором есть все столбцы и их типы.
    """
    if not matches:
        raise ValueError("Данные для обработки не могут быть пустыми")
    
    # Проверяем тип входных данных
    if not isinstance(matches, list):
        raise TypeError(f"Ожидается список, получен {type(matches)}")
    
    if not matches:
        return {}
    
    # Берем первый элемент для анализа структуры
    first_item = matches[0]
    
    if not isinstance(first_item, dict):
        raise TypeError(f"Элементы списка должны быть словарями, получен {type(first_item)}")
    
    # Функция для определения глубины списка
    def get_list_depth(lst, current_depth=0):
        """Рекурсивно определяет глубину вложенности списка"""
        if not isinstance(lst, list) or not lst:
            return current_depth
        return get_list_depth(lst[0], current_depth + 1)
    
    # Словарь для хранения типов
    types_dict = {}
    
    # Анализируем все элементы, чтобы охватить все возможные ключи
    all_keys = set()
    for match in matches:
        all_keys.update(match.keys())
    
    # Для анализа берем первый элемент
    for key in all_keys:
        # Если ключ есть в первом элементе
        if key in first_item:
            value = first_item[key]
            value_type = type(value).__name__
            
            # Обработка None
            if value is None:
                # Если None, смотрим в других элементах чтобы определить тип
                for match in matches[1:]:
                    if key in match and match[key] is not None:
                        value = match[key]
                        value_type = type(value).__name__
                        break
                else:
                    # Если во всех элементах None, используем TEXT как default
                    types_dict[key] = "TEXT"
                    continue
            
            # Обработка разных типов данных
            if value_type == "list":
                if value:  # если список не пустой
                    depth = get_list_depth(value)
                    
                    if depth == 1:
                        # Простой список - анализируем тип элементов
                        elem_types = set(type(item).__name__ for item in value)
                        
                        if len(elem_types) == 1:
                            elem_type = next(iter(elem_types))
                            if elem_type == "str":
                                types_dict[key] = "TEXT[]"
                            elif elem_type == "int":
                                types_dict[key] = "INTEGER[]"
                            elif elem_type == "float":
                                types_dict[key] = "FLOAT[]"
                            elif elem_type == "bool":
                                types_dict[key] = "BOOLEAN[]"
                            else:
                                types_dict[key] = "JSONB"
                        else:
                            # Смешанные типы
                            types_dict[key] = "JSONB"
                    else:
                        # Вложенные списки
                        types_dict[key] = "JSONB"
                else:
                    # Пустой список
                    types_dict[key] = "JSONB"
            
            elif value_type == "dict":
                types_dict[key] = "JSONB"
            
            elif value_type == "str":
                # Проверяем, может ли быть датой
                if key in ['start_time', 'end_time', 'created_at', 'updated_at']:
                    types_dict[key] = "TIMESTAMP"
                else:
                    # Определяем примерную длину строки
                    max_length = 0
                    for match in matches[:10]:  # проверяем первые 10 элементов
                        if key in match and match[key] is not None:
                            str_len = len(str(match[key]))
                            if str_len > max_length:
                                max_length = str_len
                    
                    if max_length <= 255:
                        types_dict[key] = f"VARCHAR({max_length + 50})"
                    elif max_length <= 1000:
                        types_dict[key] = "TEXT"
                    else:
                        types_dict[key] = "JSONB"  # очень длинные строки как JSON
            
            elif value_type == "int":
                # Проверяем диапазон значений
                min_val = max_val = value
                for match in matches[:10]:
                    if key in match and match[key] is not None:
                        val = match[key]
                        if val < min_val:
                            min_val = val
                        if val > max_val:
                            max_val = val
                
                # Выбираем тип на основе диапазона
                if min_val >= -32768 and max_val <= 32767:
                    types_dict[key] = "SMALLINT"
                elif min_val >= -2147483648 and max_val <= 2147483647:
                    types_dict[key] = "INTEGER"
                else:
                    types_dict[key] = "BIGINT"
            
            elif value_type == "float":
                types_dict[key] = "FLOAT"
            
            elif value_type == "bool":
                types_dict[key] = "BOOLEAN"
            
            elif value_type == "NoneType":
                types_dict[key] = "TEXT"  # default для неизвестных типов
            
            else:
                types_dict[key] = "TEXT"
        
        else:
            # Ключ есть в других элементах, но не в первом
            # Найдем его тип в первом элементе где он есть
            found_value = None
            for match in matches[1:]:
                if key in match:
                    found_value = match[key]
                    break
            
            if found_value is not None:
                value_type = type(found_value).__name__
                if value_type in ["list", "dict"]:
                    types_dict[key] = "JSONB"
                elif value_type == "str":
                    types_dict[key] = "TEXT"
                elif value_type == "int":
                    types_dict[key] = "INTEGER"
                elif value_type == "float":
                    types_dict[key] = "FLOAT"
                elif value_type == "bool":
                    types_dict[key] = "BOOLEAN"
                else:
                    types_dict[key] = "TEXT"
            else:
                # Все значения None
                types_dict[key] = "TEXT"
    
    return types_dict
   