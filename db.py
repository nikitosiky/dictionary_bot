import sqlite3

from matplotlib.pyplot import connect

from viewDB import cursor


class Database:
    def __init__(self, path="bot.db"):
        self.connection= sqlite3.connect(path)
        self.cursor = self.connection.cursor()
        self.create_tables()
    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS setting(
        user_id Integer Primary Key, 
        count_words integer Default 7,
        hour_remind integer Default 12,
        minute_remind integer Default 00
        )''')
        self.cursor.execute('''
        Create Table IF NOT EXISTS dict(
        user_id INTEGER , 
        first_lang TEXT, 
        second_lang TEXT, 
        time_added DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        self.connection.commit()

    def set_dailycount(self, user_i, count ):
        self.cursor.execute('''
        INSERT OR REPLACE INTO setting (user_id, count_words)
        VALUES(?, ?)
        ''', ( user_i, count))
        self.connection.commit()

    def get_dailycount(self, user_i):
        self.cursor.execute('''
        SELECT count_words FROM setting 
        WHERE user_id=?
        ''', (user_i,))
        result=self.cursor.fetchone()
        return result[0]
    def add_word_pair(self, user_i, word1, word2):
        self.cursor.execute('''
        Insert Into dict(user_id, first_lang, second_lang)
        VALUES(?,?, ?)
        ''', (user_i, word1, word2))
        self.connection.commit()

    def get_pair_words(self, user_i ):#   вернуть пару слов
        self.cursor.execute('''
            Select first_lang, second_lang from dict
            WHERE user_id=?
        ''', (user_i,))
        result= self.cursor.fetchall()
        return result
    def set_reminder(self,user_i, h,m):
        self.cursor.execute('''
        INSERT or REPLACE INTO setting
        (user_id, hour_remind, minute_remind)
        VALUES(?,?, ?)
        
        ''',(user_i, h, m))
        self.connection.commit()
    def delete_word(self, user_i, word):
        self.cursor.execute('''
        DELETE FROM dict 
        where user_id=? and (first_lang=? or second_lang=?)
        ''', (user_i, word, word))
        self.connection.commit()