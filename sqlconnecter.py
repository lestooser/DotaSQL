import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'DotaStat',
    'user': 'postgres',
    'password': '91B44m9144'
}

def Decorator_connect_db(func):
    def wrapper(*args, **kwargs):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            result = func(cursor, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            print(f"Database error: {e}")
        finally:
            cursor.close()
            conn.close()
    return wrapper

@Decorator_connect_db
def create_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            match_id bigint primary key,
            player_slot int,
            radiant_win boolean,
            duration int,
            game_mode int,
            lobby_type int,
            hero_id int,
            start_time timestamp,
            version int,
            kills int,
            deaths int,
            assists int,
            average_rank int,
            leaver_status int,
            party_size int,
            hero_variant int	
        )
    ''')
    print('Table created successfully.')

@Decorator_connect_db
def INSERT_MATCHES(cursor, matches):
    for match in matches:
        cursor.execute('''
            INSERT INTO matches (
                match_id,
                player_slot,
                radiant_win,
                duration,
                game_mode,
                lobby_type,
                hero_id,
                start_time,
                version,
                kills,
                deaths,
                assists,
                average_rank,
                leaver_status,
                party_size,
                hero_variant	
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
                match.get('match_id'),
                match.get('player_slot'),
                match.get('radiant_win'),
                match.get('duration'),
                match.get('game_mode'),
                match.get('lobby_type'),
                match.get('hero_id'),
                match.get('start_time'),
                match.get('version'),
                match.get('kills'),
                match.get('deaths'),
                match.get('assists'),
                match.get('average_rank'),
                match.get('leaver_status'),
                match.get('party_size'),
                match.get('hero_variant')
        ))
        
    print('Matches inserted successfully.')

