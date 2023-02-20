import sqlite3
import os
import sys

# QUERIES
# variables 
# INTEGER PRIMARY KEY  ,  TEXT    ,  REAL ,  REAL, REAL, REAL,   REAL,    TEXT, TEXT);"
#                   id , food_name, protein, carb, fat,  gram , calories, date, time
CREATE_intra_Table          = "CREATE TABLE IF NOT EXISTS intra(id INTEGER PRIMARY KEY, food_name TEXT, calories REAL, protein REAL, carb REAL, fat REAL, gram REAL, date TEXT, time TEXT);"

COUNT_FOOD_ENTRIES          = "SELECT COUNT(*) FROM intra;"

INSERT_FOOD_ENTRIES         = "INSERT INTO intra (food_name, calories, protein, carb, fat, gram, date, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"

GET_ALL_FOOD_ENTRIES        = "SELECT * FROM intra;"
GET_ALL_FOOD_ENTRIES_DATE   = "SELECT * FROM intra WHERE date = ?;"
GET_FOOD_ENTRIES_BY_NAME    = "SELECT * FROM intra WHERE food_name = ?;"
GET_FOOD_ENTRIES_BY_ID      = "SELECT * FROM intra i WHERE i.id = ?;"

GET_ALL_FOOD_ENTRIES_30     = "SELECT date, SUM(calories) FROM intra GROUP BY date ORDER BY date LIMIT 30;"
GET_MIN_CALORIES_FOOD_ENTRIES_30 = "SELECT date, total_calories FROM (SELECT date, SUM(calories) AS 'total_calories' FROM intra GROUP BY date ORDER BY date LIMIT 30 ) GROUP BY date ORDER BY total_calories LIMIT 1;"

GET_ALL_FOOD_ENTRIES_TODAY  = "SELECT SUM(calories), strftime ('%H',time) AS 'hour' FROM intra WHERE date =  date('now') GROUP BY hour;"

GET_CURRENT_DATE            = "SELECT date('now');"
GET_CURRENT_TIME            = "SELECT time('now');"
GET_MAX_ID                  = "SELECT MAX(id) FROM intra;"
GET_TOTAL_CALORIES          = "SELECT SUM(calories) FROM intra WHERE date = ?;"
GET_TOTAL_PROTEIN           = "SELECT SUM(protein) FROM intra WHERE date = ?;"
GET_TOTAL_CARB              = "SELECT SUM(carb) FROM intra WHERE date = ?;"
GET_TOTAL_FAT               = "SELECT SUM(fat) FROM intra WHERE date = ?;"

DELTE_ENTRIES_ID            = "DELETE FROM intra WHERE id = ?;"
UPDATE_ENTRIES_ID           = "UPDATE intra SET {} = ? WHERE id = ?;"


CREATE_recipe_Table         = "CREATE TABLE IF NOT EXISTS recipe(id INTEGER PRIMARY KEY, food_name TEXT, calories REAL, protein REAL, carb REAL, fat REAL);"
INSERT_FOOD_ENTRIES_recipe  = "INSERT INTO recipe (food_name, calories, protein, carb, fat) VALUES (?, ?, ?, ?, ?);"
GET_ALL_FOOD_NAME_RECIPE    = "SELECT food_name FROM recipe"


CREATE_info_Table           = "CREATE TABLE IF NOT EXISTS info(id INTEGER PRIMARY KEY, age REAL, gender TEXT, height REAL, weight REAL);"
INSERT_INFO                 = "INSERT INTO info (age, gender, height, weight) VALUES (?, ?, ?, ?);"

def cursor():
    appdir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    con = sqlite3.connect(os.path.join(appdir, 'data.db'))
    return con, con.cursor()

def create_tabels(cursor, con):
    cursor.execute(CREATE_intra_Table)
    cursor.execute(CREATE_info_Table)
    if cursor.execute("SELECT * FROM info;").fetchall() == []: 
        insert_info(con, cursor, 20, 'male', 188, 78);
    

def count_rows(cursor): 
    result = cursor.execute(COUNT_FOOD_ENTRIES)
    for (i,) in result.fetchall():
        return(i)

def add_food(con, cursor, food_name, calories, protein, carb, fat, gram):
    date = get_current_date(cursor)
    time = get_current_time(cursor)
    cursor.execute(INSERT_FOOD_ENTRIES, (food_name, calories, protein, carb, fat, gram, date, time))
    con.commit()

def get_all_food_entries(cursor): 
    return cursor.execute(GET_ALL_FOOD_ENTRIES).fetchall()

def get_all_food_entries_date(cursor, date): 
    return cursor.execute(GET_ALL_FOOD_ENTRIES_DATE, (date, )).fetchall()

def get_food_entries_by_id(cursor, _id):
    return cursor.execute(GET_FOOD_ENTRIES_BY_ID, (_id, )).fetchall()

def get_food_entries_by_name(cursor, food_name):
    return cursor.execute(GET_FOOD_ENTRIES_BY_NAME, (food_name, )).fetchall()

def get_current_date(cursor):
    result = cursor.execute(GET_CURRENT_DATE)
    for (i,) in result.fetchall():
        return(i)

def get_current_time(cursor):
    result = cursor.execute(GET_CURRENT_TIME)
    for (i,) in result.fetchall():
        return(i)

def get_max_id(cursor):
    result = cursor.execute(GET_MAX_ID)
    for (i,) in result.fetchall():
        return i if i != None else 0

def get_total_calories(cursor, date):
    result = cursor.execute(GET_TOTAL_CALORIES, (date, ))
    for (i,) in result.fetchall():
        return i if i != None else 0

def get_total_protein(cursor, date):
    result = cursor.execute(GET_TOTAL_PROTEIN, (date, ))
    for (i,) in result.fetchall():
        return round(i, 1) if i != None else 0

def get_total_carb(cursor, date):
    result = cursor.execute(GET_TOTAL_CARB, (date, ))
    for (i,) in result.fetchall():
        return round(i, 1) if i != None else 0

def get_total_fat(cursor, date):
    result = cursor.execute(GET_TOTAL_FAT, (date, ))
    for (i,) in result.fetchall():
        return round(i, 1) if i != None else 0


def delete_entries_id(con, cursor, _id):
    cursor.execute(DELTE_ENTRIES_ID, (_id, ))
    con.commit()
    

def update_entries_id(con, cursor, _id, num, res):
    list_of_name = ["id", "food_name", "calories", "protein", "carb", "fat", "gram", "date", "time"]
    print([list_of_name[num], res, _id])
    cursor.execute(UPDATE_ENTRIES_ID.format(list_of_name[num]), ( res, _id))
    con.commit()

def get_all_food_entries_30(cur):
    res = []
    for i in  cur.execute(GET_ALL_FOOD_ENTRIES_30).fetchall():
        res.append(list(i))
    return res


def get_min_calories_food_entries_30(cur):
    for i in cur.execute(GET_MIN_CALORIES_FOOD_ENTRIES_30).fetchall():
        res = list(i)
        return res[1]

def get_all_food_entries_today(cur):
    res = []
    for i in  cur.execute(GET_ALL_FOOD_ENTRIES_TODAY).fetchall():
        res.append(list(i))
    return res


def insert_info(con, cursor, age, gender, height, weight):
    cursor.execute(INSERT_INFO, ( age, gender, height, weight))
    con.commit()

def get_info(cur):
    return list(cur.execute("SELECT age, gender, height, weight FROM info ORDER BY id DESC LIMIT 1;").fetchall()[0])

'''
THIS is for recipe database part
'''
def create_tabels_recipe(cur):
    cur.execute(CREATE_recipe_Table)

def add_food_recipe(con, cursor, food_name, calories, protein, carb, fat):
    cursor.execute(INSERT_FOOD_ENTRIES_recipe, (food_name, calories, protein, carb, fat))
    con.commit()

def get_all_food_name_recipe(cursor):
    result = []
    for i in list(cursor.execute(GET_ALL_FOOD_NAME_RECIPE).fetchall()):
        for j in list(i):
            result.append(j)
    return result


    
# con, cur = cursor()

# #print(list(cur.execute("SELECT height, weight FROM info ORDER BY id DESC LIMIT 1;").fetchall()[0]))
# # cur.execute("DROP TABLE IF EXISTS info;")
# print(cur.execute("SELECT * FROM info;").fetchall())
# #print(cur.execute("SELECT name FROM sqlite_master WHERE name='recipev'").fetchall())
# #res = cur.execute("SELECT date, SUM(calories) FROM intra GROUP BY date ORDER BY date LIMIT 30;").fetchall()
# #res = cur.execute("SELECT date, total_calories FROM (SELECT date, SUM(calories) AS 'total_calories' FROM intra GROUP BY date ORDER BY date LIMIT 30 ) GROUP BY date ORDER BY total_calories LIMIT 1;").fetchall()
# #print(get_all_food_entries_30(cur))

# con.close()

print("wrong file, go start the app in app.py")

