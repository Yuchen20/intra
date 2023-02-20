import database
import recipe
import eel
import re
import random


eel.init('web')

# might delete this after completion
@eel.expose                        
def say_hello_py(x):
    print('Hello from %s' % x)

# Function: handles result from input field
@eel.expose
def handle_input(x):
    _str = x.strip(' ')
    if _str[: 3].lower() == "ate":
        _str = _str[4:]
        result = ["", "", "", "", "", ""] #food_name, protein, carb, fat, calories,gram
        for i in range(0, 6):
            next_comma = _str.find(',')
            if next_comma == -1: 
                try:
                    i == 0 or float(_str)
                except ValueError:
                    print ("Not a float")
                    break;
                else:
                    if i == 0:  result[i] = _str;
                    else:       result[i] = float(_str)
                    break;
            if i == 0:
                result[i] = _str[:next_comma]
            else:
                if _str[:next_comma] == "" :
                    result[i] = "&nbsp"
                else: 
                    try:
                         float(_str[:next_comma])
                    except: 
                        print("")
                    else:
                        result[i] = float(_str[:next_comma])
            _str = _str[next_comma + 1:].strip(' ')
        database.add_food(con, cur, result[0], result[1], result[2], result[3], result[4], result[5])
        print(result)
        eel.prep_new_div()
    #ate rice, 330, 7.1, 78.9, 1.6, 100
    elif _str[:6].lower() == "delete":
        _str = _str[7:].strip(' ')
        try:
            _str = float(re.sub("id", "", _str))
        except ValueError:
            print("")
        else:
            database.delete_entries_id(con, cur, _str)
            eel.remove_sub_div()
    update_nutrition_chart()
    update_monthly_chart(cur)
    update_daily_chart()
    update_total_rows()
   # eel.total_calories_js(database.get_total_calories(cur, database.get_current_date(cur)))
   #print('%s' % x)

# Function: sending entries to the "create_new_div" in js
@eel.expose
def get_entries_from_py(_id):
    if database.get_max_id(cur) >= _id:
        entries_result = database.get_food_entries_by_id(cur, _id)
        if entries_result == []:
            eel.create_new_empty_div()
        else:
            for (a, b, c, d, e, f, g, h, i) in entries_result:
                entries_result_array = [a, b, c, d, e, f, g, h, i]
            eel.create_new_div(entries_result_array)

# Function: receiving data from js, and update the table intra with the data.
@eel.expose
def update_entries_id_app(_id, num, res):
    database.update_entries_id(con, cur, _id + 1, num, res)
    update_nutrition_chart()
    update_monthly_chart(cur)
    update_daily_chart()
    update_total_rows()

# Function: receiving data from js, and update the table info with the data.
@eel.expose
def add_info(a, g, h, w):
    print(a, g, h, w)
    database.insert_info(con, cur,a, g,  h, w)


# Function: update the monthly chart at the center of overview part
def update_monthly_chart(cursor):
    monthly_chart_data  = database.get_all_food_entries_30(cursor)
    _label              = []
    _calories           = []
    for data_entrie in monthly_chart_data:
        if data_entrie[0][5:10] == "01-01":
            _label.append( str(int(data_entrie[0][0:4])) + "/" + str(int(data_entrie[0][5:7])) + "/" + str(int(data_entrie[0][8:10])) )
        else:
            _label.append( str(int(data_entrie[0][5:7])) + "/" + str(int(data_entrie[0][8:10])) )
        _calories.append(data_entrie[1])
    _min = database.get_min_calories_food_entries_30(cursor)

    hw = database.get_info(cur)
    max_calories = 0
    if hw[1] == 'Male':
        max_calories = 13.9 * hw[3] + 4.2 * hw[2] - 3.4* hw[0] + 54
    else:
        max_calories = 13.9 * hw[3] + 4.2 * hw[2] - 3.3* hw[0] - 58

    max_calories_l = [max_calories] * len(_calories)
    random.seed(max_calories)
    max_calories_l = [i + random.randint(-60, 60) for i in max_calories_l]
    eel.update_monthly_chart(_calories, _label, _min, max_calories_l)

# Function: update the daily chart at the left pane of overview part
def update_daily_chart():
    daily_chart_data  = database.get_all_food_entries_today(cur)
    _label              = list(range(24))
    _calories           = [0] * 24
    for data_entrie in daily_chart_data:
        t = int(data_entrie[1])
        _calories[t] = data_entrie[0]
    eel.update_daily_chart(_calories, _label)

# Function: update the info at left pane of overview part
def update_nutrition_chart():
    hw = database.get_info(cur)
    max_calories = 0
    if hw[1] == 'Male':
        max_calories = 13.9 * hw[3] + 4.2 * hw[2] - 3.4* hw[0] + 54
    else:
        max_calories = 13.9 * hw[3] + 4.2 * hw[2] - 3.3* hw[0] - 58
    today = database.get_current_date(cur)
    eel.total_nutrition_js(
        round(database.get_total_calories(cur, today), 0), 
        round(database.get_total_protein(cur, today), 1),
        round(database.get_total_carb(cur, today), 1), 
        round(database.get_total_fat(cur, today), 1), 
        round(max_calories, 0), round(1.35 * hw[3], 0), round(2.65 * hw[3], 0), round(0.8 * hw[3], 0)
    )

# update the info at the up right coner.
def update_total_rows():
    eel.total_rows_js(database.count_rows(cur))

# update height and weight
def update_hw():
     hw = database.get_info(cur)
     eel.update_hw_js(hw[0], hw[1], hw[2], hw[3])



# connect to the database (data.db) and create it if there's none
con, cur = database.cursor()
database.create_tabels(cur, con)


update_nutrition_chart()
update_monthly_chart(cur)
update_daily_chart()
update_total_rows()
update_hw()

eel.update_suggestion(database.get_all_food_name_recipe(cur))
# start the application
eel.start('main.html', size=(800, 500), position = (350, 200), mode='chrome', cmdline_args=[])  # Start






""" while True:
    #print("I'm a main loop")
    eel.total_rows_js(database.count_rows(cur))
    eel.sleep(1.0)    
 """

# build the app
""" 
source ../test_venv/bin/activate
python -m eel app.py web --onedir --noconsole --noconfirm
 """

 
""" 
ate rice, 330, 7.1, 78.9, 1.6, 100
ate white cheese baton, 636, 24.2, 108.6, 10.6, 200
ate meatball, 600, , , , 450
ate egg, 160, 16.6, 3.2,11.4,150 
ate latte (L), 292, 14.9, 21.7, 16.4, 496
ate Grenade bar(fuged up), 232, 20, 18, 10, 60
 """
 
 