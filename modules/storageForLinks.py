import sqlite3
from sqlite3 import Error

def sql_connection():
 
    try:
 
        con = sqlite3.connect('memoryStorage.db')
 
        return con

    except Error:
 
        print(Error)
 
def sql_table(con):

    cursorObj = con.cursor()

    cursorObj.execute("CREATE TABLE IF NOT EXISTS clips(name text, link text, person text)")

    con.commit()

def sql_insert(con, entities):

    cursorObj = con.cursor()
    
    cursorObj.execute('INSERT INTO clips(name, link, person) VALUES(?, ?, ?)', entities)

    con.commit()

    insert_return = 'запись добавлена'

    return (insert_return)


def read_sqlite_table(con):
    
    cursorObj = con.cursor()
    sqlite_select_query = """SELECT * from clips"""
    cursorObj.execute(sqlite_select_query)
    records = cursorObj.fetchall()
    # print("Всего строк:  ", len(records))
    line = ''
    num = 1
    for row in records:
        line += str(num) + '. ' + row[0] +' '+ row[2] + '\n'
        num += 1

    lines=[]
    lines=line.split('\n')

    cursorObj.close()

    return lines

def read_name_sqlite_table(con):
    
    cursorObj = con.cursor()
    sqlite_select_query = """SELECT * from clips"""
    cursorObj.execute(sqlite_select_query)
    records = cursorObj.fetchall()
    print("Всего строк:  ", len(records))
    line = ''
    for row in records:
        line += row[0] + '\n'

    lines=[]
    lines=line.split('\n')

    cursorObj.close()

    return lines

def delete_sqlite_record(dev_name):
    try:
        sqlite_connection = sqlite3.connect('memoryStorage.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sql_update_query = """DELETE from clips where name = ?"""
        cursor.execute(sql_update_query, (dev_name, ))
        sqlite_connection.commit()
        print("Запись успешно удалена")
        cursor.close() 
        error_del = 'Запись успешно удалена'
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
        error_del = 'Ошибка при удалении записи'
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
        return error_del


def read_single_row(developer_id):
    print(developer_id)
    try:
        sqlite_connection = sqlite3.connect('memoryStorage.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")
        sqlite_select_query = """SELECT * from clips where name = ?"""
        cursor.execute(sqlite_select_query, (developer_id, ))
        print("Чтение одной строки \n")
        record = cursor.fetchone()
        return_read = (record[1])
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
        return_read = ('Ошибка при выборе клипа')

    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

        return return_read