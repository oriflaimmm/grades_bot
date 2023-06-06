import telebot
import sqlite3
from telebot import types
import pandas as pd

token='6215957485:AAEtzsaaoGxJj7caq7kieFQYe71S-klsm_Q'
bot=telebot.TeleBot(token)

conn = sqlite3.connect('orders.db', check_same_thread=False)
cursor = conn.cursor()

def db_table_val(user_id: str, user_name: str, username: str):
	cursor.execute('INSERT OR IGNORE INTO оценки (user_id, user_name, username) VALUES (?, ?, ?)', (user_id, user_name, username))
	conn.commit()

def moi_nakopi(message):
    user_id = message.from_user.id
    cursor.execute("SELECT * FROM оценки WHERE user_id=?", (user_id,))
    res = cursor.fetchone()
    if res:
        flex_nacop_value = res[8]
        econf_nacop_value = res[12]
        stat_nacop_value = res[17]
        micr_nacop_value = res[22]

    bot.send_message(message.chat.id, f"так так так, вот они, твои накопы на данный момент:\n\nFLEX - {flex_nacop_value}\nЭкономика фирмы - {econf_nacop_value}\nСтатистика - {stat_nacop_value}\nМикроэкономика III - {micr_nacop_value}\n")

def is_number(grade):
    try:
        float(grade)
        return True
    except ValueError:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Выбрать предмет")
    btn2 = types.KeyboardButton("Задать вопрос")
    btn3 = types.KeyboardButton("Все формулы")
    btn4 = types.KeyboardButton("Мои накопы")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Это бот, который поможет тебе посчитать твою итоговую оценку по формуле!".format(message.from_user), reply_markup=markup)



#-------------------------------------------------------------главное меню-----------------------------------------------------------------------



@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "Задать вопрос"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Как это работает?")
        btn2 = types.KeyboardButton("Что делать, если у меня допса...")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Готов к любым вопросам!", reply_markup=markup)
    elif(message.text == "Выбрать предмет"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton("Микроэкономика III")
        btn2 = types.KeyboardButton("FLEX")
        btn3 = types.KeyboardButton("Экономика фирмы")
        btn4 = types.KeyboardButton("Статистика")
        btn5 = types.KeyboardButton("Финансы")
        btn6 = types.KeyboardButton("УПЭК")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, back)
        us_id = message.from_user.id
        us_name = message.from_user.first_name
        username = message.from_user.username
        db_table_val(user_id=us_id, user_name=us_name, username=username)
        bot.send_message(message.chat.id, text="Какой предмет интересует?", reply_markup=markup)
    
    elif(message.text == "Как это работает?"):
        bot.send_message(message.chat.id, "Необходимо ввести свои оценки за каждый элемент контроля, а я посчитаю итоговый балл по формуле ;)\nсамое важное - ввести оценку от 0 до 10 и с разделителем в виде точки -  как в смарте, только работает лучше!")
    
    elif message.text == "Что делать, если у меня допса...":
        bot.send_photo(message.chat.id, "https://rg.ru/uploads/images/135/37/51/ponchik-1000.jpg", caption="Главное - не расстраиваться! А вообще можно подать аппеляцию или попробовать уговорить преподавателя чуть-чуть повысить тебе оценочку ;) Вот тебе котик")

    elif message.text == "Мои накопы":
        moi_nakopi(message)
        bot.send_message(message.chat.id, text="Если у тебя появились новые оценки, советую заглянуть в нужный раздел и внести их в формулу :)")
    
    elif (message.text == "Вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Выбрать предмет")
        button2 = types.KeyboardButton("Задать вопрос")
        button3 = types.KeyboardButton("Все формулы")
        button4 = types.KeyboardButton("Мои накопы")
        markup.add(button1, button2, button3, button4)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)

    elif(message.text == "Все формулы"):
        bot.send_message(message.chat.id, "FLEX: 0.4 экзамен + 0.6 накоп, где накоп = 0.4 тест + 0.4 проект + 0.2 аудиторка\nЭкономика фирм: 0.25 аудиторка + 0.25 тест + 0.5 блокирующий экзамен\nСтатистика: 0.3 летучки + 0.3 проект + 0.1 проджект ревью + 0.3 экзамен\nМикроэкономика 3:  0.25 квизы + 0.15 аудиторка и домашки + 0.3 мидтерм + 0.3 экзамен") 

    elif (message.text == "Микроэкономика III"):
        msg = bot.send_message(message.chat.id, text="Для подсчета оценки по микроэкономике сначала введите оценку за квизы:")
        bot.register_next_step_handler(msg, function_micra1)

    elif (message.text == "Экономика фирмы"):
        msg = bot.send_message(message.chat.id, text="Для подсчета оценки по экономике фирмы сначала введите оценку за аудиторку:")
        bot.register_next_step_handler(msg, function_firms1)

    elif (message.text == "Финансы"):
        msg = bot.send_message(message.chat.id, text="Для подсчета оценки по финансам мне сначала самому надо вспомнить формулу...")
        #bot.register_next_step_handler(msg, function_finances1)

    elif (message.text == "FLEX"):
        msg = bot.send_message(message.chat.id, text="Для подсчета оценки по флексу сначала введите оценку за тест:")
        bot.register_next_step_handler(msg, function_flex1)

    elif (message.text == "Статистика"):
        msg = bot.send_message(message.chat.id, text="Для подсчета оценки по статистике сначала введите оценку за летучки:")
        bot.register_next_step_handler(msg, function_stats1)

    elif (message.text == "УПЭК"):
        msg = bot.send_message(message.chat.id, text="Для подсчета оценки по управленческой экономике мне сначала самому надо вспомнить формулу...")
        #bot.register_next_step_handler(msg, function_ypek1)
    
    elif (message.text == "Таблица"):
        bot.send_message(message.chat.id, text="Подождите, проверяю права доступа... Введите пароль!!!!!!")
        bot.register_next_step_handler(message, admin_func)

    elif (message.text == "Получить общую таблицу"):
        msg = bot.send_message(message.chat.id, text="Вы точно этого хотите?")
        bot.register_next_step_handler(msg, download)

    elif (message.text == "Проверить юзера"):
        msg = bot.send_message(message.chat.id, text="Введите юзернейм")
        bot.register_next_step_handler(msg, print_grades)

    else:
       bot.send_message(message.chat.id, text="На такую команду я не запрограммирован..")




#-------------------------------------------------------------функции для микры-----------------------------------------------------------------------





''' 'micra'- > zip([1, 2, 3], ['text1', 'text2', 'text3'], [1, 2, 3])
    for i, t, x in d['micra']:
'''

def function_micra1(message, result=None):

    if is_number(message.text) == True and float(message.text) <= 10 and float(message.text) >=0:
        grade = float(message.text)
        user_id = message.from_user.id

        cursor.execute("SELECT user_id FROM оценки WHERE user_id=?", (user_id,))
        res = cursor.fetchone()
        if res:
            user_id = res[0]
            cursor.execute("UPDATE оценки SET MICR_g1=? WHERE user_id=?", (grade, user_id))
            conn.commit()

        msg = bot.send_message(message.chat.id, "круто, теперь оценку за аудиторку:")
        bot.register_next_step_handler(msg, function_micra2)
    else:
        msg = bot.send_message(message.chat.id, text="пожалуйста, введите оценку цифрами с разделителем в виде точки в диапазоне от 0 до 10")
        bot.register_next_step_handler(msg, function_micra1)

def function_micra2(message):

    if is_number(message.text) == True and float(message.text) <= 10 and float(message.text) >=0:
        grade = float(message.text)
        user_id = message.from_user.id

        cursor.execute("SELECT user_id FROM оценки WHERE user_id=?", (user_id,))
        res = cursor.fetchone()
        if res:
            user_id = res[0]
            cursor.execute("UPDATE оценки SET MICR_g2=? WHERE user_id=?", (grade, user_id))
            conn.commit()

        msg = bot.send_message(message.chat.id, "замечательно, теперь оценку за мидтерм:")
        bot.register_next_step_handler(msg, function_micra3)

    else:
        msg = bot.send_message(message.chat.id, text="пожалуйста, введите оценку цифрами с разделителем в виде точки в диапазоне от 0 до 10")
        bot.register_next_step_handler(msg, function_micra2)

def function_micra3(message):

    if is_number(message.text) == True and float(message.text) <= 10 and float(message.text) >=0:
        grade = float(message.text)

        user_id = message.from_user.id

        cursor.execute("SELECT user_id FROM оценки WHERE user_id=?", (user_id,))
        res = cursor.fetchone()
        if res:
            user_id = res[0]
            cursor.execute("UPDATE оценки SET MICR_g3=? WHERE user_id=?", (grade, user_id))
            conn.commit()

        msg = bot.send_message(message.chat.id, "ваще класс, осталось только ввести оценку за экзамен:")
        bot.register_next_step_handler(msg, function_micra4)
    
    else:
        msg = bot.send_message(message.chat.id, text="пожалуйста, введите оценку цифрами с разделителем в виде точки в диапазоне от 0 до 10")
        bot.register_next_step_handler(msg, function_micra3)

def function_micra4(message):

    if is_number(message.text) == True and float(message.text) <= 10 and float(message.text) >=0:
        grade = float(message.text)
        result = 0

        user_id = message.from_user.id

        cursor.execute("SELECT user_id FROM оценки WHERE user_id=?", (user_id,))
        res = cursor.fetchone()
        if res:
            user_id = res[0]
            cursor.execute("UPDATE оценки SET MICR_g4=? WHERE user_id=?", (grade, user_id))
            conn.commit()

        cursor.execute("SELECT * FROM оценки WHERE user_id=?", (user_id,))
        res = cursor.fetchone()
        if res:
            micr_g1_value = res[18]
            micr_g2_value = res[19]
            micr_g3_value = res[20]
            micr_g4_value = res[21]

        bot.send_message(message.chat.id, "теперь мне осталось только посчитать твой накоп.... надо чуть-чуть подождать....")

        result = str(micr_g1_value*0.25 + micr_g2_value*0.15 + micr_g3_value*0.3 + micr_g4_value*0.3)
        result = round(float(result), 2)

        cursor.execute("SELECT user_id FROM оценки WHERE user_id=?", (user_id,))
        res = cursor.fetchone()
        if res:
            user_id = res[0]
            cursor.execute("UPDATE оценки SET MICR_nacop=? WHERE user_id=?", (result, user_id))
            conn.commit()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) 
        btn1 = types.KeyboardButton("Микроэкономика III")
        btn2 = types.KeyboardButton("FLEX")
        btn3 = types.KeyboardButton("Экономика фирмы")
        btn4 = types.KeyboardButton("Статистика")
        btn5 = types.KeyboardButton("Финансы")
        btn6 = types.KeyboardButton("УПЭК")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, back)
        
        bot.send_message(message.chat.id, f'твоя оценка - {result}, которая состоит из:\n\nквизов (25%) - {round(micr_g1_value*0.25,2)}\nаудиторки - (15%) - {round(micr_g2_value*0.15,2)}\nмидтерма (30%)  - {round(micr_g3_value*0.3,2)}\nэкзамена (30%) - {round(micr_g4_value*0.3,2)}', reply_markup=markup)
    else:
        msg = bot.send_message(message.chat.id, text="пожалуйста, введите оценку цифрами с разделителем в виде точки в диапазоне от 0 до 10")
        bot.register_next_step_handler(msg, function_micra4)



#-------------------------------------------------------------функции для экономики фирмы-----------------------------------------------------------------------



def function_firms1(message, result=None):

    if is_number(message.text) == True and float(message.text) <= 10 and float(message.text) >=0:

        grade = float(message.text)
        user_id = message.from_user.id

        cursor.execute("SELECT user_id FROM оценки WHERE user_id=?", (user_id,))
        res = cursor.fetchone()
        if res:
            user_id = res[0]
            cursor.execute("UPDATE оценки SET ECONF_g1=? WHERE user_id=?", (grade, user_id))
            conn.commit()

        msg = bot.send_message(message.chat.id, "круто, теперь оценку за тест:")
        bot.register_next_step_handler(msg, function_firms2)

    else:
        msg = bot.send_message(message.chat.id, text="пожалуйста, введите оценку цифрами с разделителем в виде точки в диапазоне от 0 до 10")
        bot.register_next_step_handler(msg, function_firms1)

def function_firms2(message, result=None):

    if is_number(message.text) == True and float(message.text) <= 10 and float(message.text) >=0:

        grade = float(message.text)
        user_id = message.from_user.id

        cursor.execute("SELECT user_id FROM оценки WHERE user_id=?", (user_id,))
        res = cursor.fetchone()
        if res:
            user_id = res[0]
            cursor.execute("UPDATE оценки SET ECONF_g2=? WHERE user_id=?", (grade, user_id))
            conn.commit()

        msg = bot.send_message(message.chat.id, "ваще класс, а теперь оценку за экзамен:")
        bot.register_next_step_handler(msg, function_firms3)
    
    else:
        msg = bot.send_message(message.chat.id, text="пожалуйста, введите оценку цифрами с разделителем в виде точки в диапазоне от 0 до 10")
        bot.register_next_step_handler(msg, function_firms2)

def function_firms3(message):

    if is_number(message.text) == True and float(message.text) <= 10 and float(message.text) >=0:

        grade = float(message.text)
        result = 0

        user_id = message.from_user.id

        cursor.execute("SELECT user_id FROM оценки WHERE user_id=?", (user_id,))
        res = cursor.fetchone()
        if res:
            user_id = res[0]
            cursor.execute("UPDATE оценки SET ECONF_g3=? WHERE user_id=?", (grade, user_id))
            conn.commit()

        cursor.execute("SELECT * FROM оценки WHERE user_id=?", (user_id,))
        res = cursor.fetchone()
        if res:
            econf_g1_value = res[9]
            econf_g2_value = res[10]
            econf_g3_value = res[11]

        bot.send_message(message.chat.id, "теперь мне осталось только посчитать твой накоп.... надо чуть-чуть подождать....")

        result = str(econf_g1_value*0.25 + econf_g2_value*0.25 + econf_g3_value*0.5)
        result = round(float(result), 2)

        cursor.execute("SELECT user_id FROM оценки WHERE user_id=?", (user_id,))
        res = cursor.fetchone()
        if res:
            user_id = res[0]
            cursor.execute("UPDATE оценки SET ECONF_nacop=? WHERE user_id=?", (result, user_id))
            conn.commit()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) 
        btn1 = types.KeyboardButton("Микроэкономика III")
        btn2 = types.KeyboardButton("FLEX")
        btn3 = types.KeyboardButton("Экономика фирмы")
        btn4 = types.KeyboardButton("Статистика")
        btn5 = types.KeyboardButton("Финансы")
        btn6 = types.KeyboardButton("УПЭК")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, back)
        
        if grade >= 4:
            bot.send_message(message.chat.id, f'твоя оценка - {result}, которая состоит из:\n\nаудиторки (25%) - {econf_g1_value*0.25}\nтеста (25%) - {econf_g2_value*0.25}\nблокирующего экзамена (50%) - {econf_g3_value*0.5}', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, f'твоя оценка - {result}, но к сожалению, экзамен по этому предмету блокирующий :(', reply_markup=markup)
    
    else:
        msg = bot.send_message(message.chat.id, text="пожалуйста, введите оценку цифрами с разделителем в виде точки в диапазоне от 0 до 10")
        bot.register_next_step_handler(msg, function_firms3)



#-------------------------------------------------------------функции для флекса-----------------------------------------------------------------------



def function_flex1(message, result=None):

    if is_number(message.text) == True and float(message.text) <= 10 and float(message.text) >=0:
    
        grade = float(message.text)

        user_id = message.from_user.id

        cursor.execute("SELECT user_id FROM оценки WHERE user_id=?", (user_id,))
        res = cursor.fetchone()
        if res:
            user_id = res[0]
            cursor.execute("UPDATE оценки SET FLEX_g1=? WHERE user_id=?", (grade, user_id))
            conn.commit()

        msg = bot.send_message(message.chat.id, "круто, теперь оценку за проект:")
        bot.register_next_step_handler(msg, function_flex2)
    
    else:
        msg = bot.send_message(message.chat.id, text="пожалуйста, введите оценку цифрами с разделителем в виде точки в диапазоне от 0 до 10")
        bot.register_next_step_handler(msg, function_flex1)

def function_flex2(message, result=None):

    if is_number(message.text) == True and float(message.text) <= 10 and float(message.text) >=0:

        grade = float(message.text)
        user_id = message.from_user.id

        cursor.execute("SELECT user_id FROM оценки WHERE user_id=?", (user_id,))
        res = cursor.fetchone()
        if res:
            user_id = res[0]
            cursor.execute("UPDATE оценки SET FLEX_g2=? WHERE user_id=?", (grade, user_id))
            conn.commit()

        msg = bot.send_message(message.chat.id, "замечательно, а аудиторка у тебя какая?:")
        bot.register_next_step_handler(msg, function_flex3)

    else:
        msg = bot.send_message(message.chat.id, text="пожалуйста, введите оценку цифрами с разделителем в виде точки в диапазоне от 0 до 10")
        bot.register_next_step_handler(msg, function_flex2)

def function_flex3(message, result=None):

    if is_number(message.text) == True and float(message.text) <= 10 and float(message.text) >=0:

        grade = float(message.text)
        user_id = message.from_user.id

        cursor.execute("SELECT user_id FROM оценки WHERE user_id=?", (user_id,))
        res = cursor.fetchone()
        if res:
            user_id = res[0]
            cursor.execute("UPDATE оценки SET FLEX_g3=? WHERE user_id=?", (grade, user_id))
            conn.commit()

        msg = bot.send_message(message.chat.id, "блин ты такой умный класс... а какая оценка за экзамен?")
        bot.register_next_step_handler(msg, function_flex4)

    else:
        msg = bot.send_message(message.chat.id, text="пожалуйста, введите оценку цифрами с разделителем в виде точки в диапазоне от 0 до 10")
        bot.register_next_step_handler(msg, function_flex3)

def function_flex4(message):

    if is_number(message.text) == True and float(message.text) <= 10 and float(message.text) >=0:

        result = 0
        grade = float(message.text)

        user_id = message.from_user.id

        cursor.execute("SELECT user_id FROM оценки WHERE user_id=?", (user_id,))
        res = cursor.fetchone()
        if res:
            user_id = res[0]
            cursor.execute("UPDATE оценки SET FLEX_g4=? WHERE user_id=?", (grade, user_id))
            conn.commit()

        cursor.execute("SELECT * FROM оценки WHERE user_id=?", (user_id,))
        res = cursor.fetchone()
        if res:
            flex_g1_value = res[4]
            flex_g2_value = res[5]
            flex_g3_value = res[6]
            flex_g4_value = res[7]


        bot.send_message(message.chat.id, "теперь мне осталось только посчитать твой накоп.... надо чуть-чуть подождать....")

        result = str((flex_g1_value*0.4 + flex_g2_value*0.4 + flex_g3_value*0.2)*0.6 + flex_g4_value*0.4)
        result = round(float(result), 2)

        cursor.execute("SELECT user_id FROM оценки WHERE user_id=?", (user_id,))
        res = cursor.fetchone()
        if res:
            user_id = res[0]
            cursor.execute("UPDATE оценки SET FLEX_nacop=? WHERE user_id=?", (result, user_id))
            conn.commit()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) 
        btn1 = types.KeyboardButton("Микроэкономика III")
        btn2 = types.KeyboardButton("FLEX")
        btn3 = types.KeyboardButton("Экономика фирмы")
        btn4 = types.KeyboardButton("Статистика")
        btn5 = types.KeyboardButton("Финансы")
        btn6 = types.KeyboardButton("УПЭК")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, back)

        bot.send_message(message.chat.id, f'твоя оценка - {result}, которая состоит из:\n\nэкзамена (40%) - {round(flex_g4_value*0.4,2)}\nнакопа (60%) - {round(flex_g1_value*0.4+flex_g2_value*0.4+flex_g3_value*0.2,2)}\n(который состоит из:\n  теста (40%) - {round(flex_g1_value*0.4,2)}\n  проекта (40%) - {round(flex_g2_value*0.4,2)}\n  аудиторки (20%) - {round(flex_g3_value*0.2,2)})', reply_markup=markup)   

    else:
        msg = bot.send_message(message.chat.id, text="пожалуйста, введите оценку цифрами с разделителем в виде точки в диапазоне от 0 до 10")
        bot.register_next_step_handler(msg, function_flex4)



#-------------------------------------------------------------функции для статы-----------------------------------------------------------------------



def function_stats1(message, result=None):

    if is_number(message.text) == True and float(message.text) <= 10 and float(message.text) >=0:

        grade = float(message.text)
        user_id = message.from_user.id

        cursor.execute("SELECT user_id FROM оценки WHERE user_id=?", (user_id,))
        res = cursor.fetchone()
        if res:
            user_id = res[0]
            cursor.execute("UPDATE оценки SET STAT_g1=? WHERE user_id=?", (grade, user_id))
            conn.commit()

        msg = bot.send_message(message.chat.id, "круто, теперь оценку за проект:")
        bot.register_next_step_handler(msg, function_stats2)

    else:
        msg = bot.send_message(message.chat.id, text="пожалуйста, введите оценку цифрами с разделителем в виде точки в диапазоне от 0 до 10")
        bot.register_next_step_handler(msg, function_stats1)

def function_stats2(message, result=None):

    if is_number(message.text) == True and float(message.text) <= 10 and float(message.text) >=0:

        grade = float(message.text)

        user_id = message.from_user.id

        cursor.execute("SELECT user_id FROM оценки WHERE user_id=?", (user_id,))
        res = cursor.fetchone()
        if res:
            user_id = res[0]
            cursor.execute("UPDATE оценки SET STAT_g2=? WHERE user_id=?", (grade, user_id))
            conn.commit()

        msg = bot.send_message(message.chat.id, "ваще класс, а теперь оценку за проджект ревью:")
        bot.register_next_step_handler(msg, function_stats3)
    
    else:
        msg = bot.send_message(message.chat.id, text="пожалуйста, введите оценку цифрами с разделителем в виде точки в диапазоне от 0 до 10")
        bot.register_next_step_handler(msg, function_stats2)

def function_stats3(message, result=None):

    if is_number(message.text) == True and float(message.text) <= 10 and float(message.text) >=0:

        grade = float(message.text)

        user_id = message.from_user.id

        cursor.execute("SELECT user_id FROM оценки WHERE user_id=?", (user_id,))
        res = cursor.fetchone()
        if res:
            user_id = res[0]
            cursor.execute("UPDATE оценки SET STAT_g3=? WHERE user_id=?", (grade, user_id))
            conn.commit()

        msg = bot.send_message(message.chat.id, "блин ты такой умный класс... а какая оценка за экзамен?")
        bot.register_next_step_handler(msg, function_stats4)

    else:
        msg = bot.send_message(message.chat.id, text="пожалуйста, введите оценку цифрами с разделителем в виде точки в диапазоне от 0 до 10")
        bot.register_next_step_handler(msg, function_stats3)

def function_stats4(message):

    if is_number(message.text) == True and float(message.text) <= 10 and float(message.text) >=0:

        result = 0
        grade = float(message.text)

        user_id = message.from_user.id

        cursor.execute("SELECT user_id FROM оценки WHERE user_id=?", (user_id,))
        res = cursor.fetchone()
        if res:
            user_id = res[0]
            cursor.execute("UPDATE оценки SET STAT_g4=? WHERE user_id=?", (grade, user_id))
            conn.commit()

        cursor.execute("SELECT * FROM оценки WHERE user_id=?", (user_id,))
        res = cursor.fetchone()
        if res:
            stat_g1_value = res[13]
            stat_g2_value = res[14]
            stat_g3_value = res[15]
            stat_g4_value = res[16]

        bot.send_message(message.chat.id, "теперь мне осталось только посчитать твой накоп.... надо чуть-чуть подождать....")

        result = str(stat_g1_value*0.3 + stat_g2_value*0.3 + stat_g3_value*0.1 + stat_g4_value*0.3)
        result = round(float(result), 2)

        cursor.execute("SELECT user_id FROM оценки WHERE user_id=?", (user_id,))
        res = cursor.fetchone()
        if res:
            user_id = res[0]
            cursor.execute("UPDATE оценки SET STAT_nacop=? WHERE user_id=?", (result, user_id))
            conn.commit()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) 
        btn1 = types.KeyboardButton("Микроэкономика III")
        btn2 = types.KeyboardButton("FLEX")
        btn3 = types.KeyboardButton("Экономика фирмы")
        btn4 = types.KeyboardButton("Статистика")
        btn5 = types.KeyboardButton("Финансы")
        btn6 = types.KeyboardButton("УПЭК")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, back)
        
        bot.send_message(message.chat.id, f'твоя оценка - {result}, которая состоит из\n\nлетучек (30%) - {round(stat_g1_value*0.3,2)}\nпроекта (30%) - {round(stat_g2_value*0.3,2)}\nпроджект ревью (10%) - {round(stat_g3_value*0.1,2)}\nэкзамена (30%) - {round(stat_g4_value*0.3,2)}', reply_markup=markup)

    else:
        msg = bot.send_message(message.chat.id, text="пожалуйста, введите оценку цифрами с разделителем в виде точки в диапазоне от 0 до 10")
        bot.register_next_step_handler(msg, function_stats3)



#-------------------------------------------------------------функции для упэка-----------------------------------------------------------------------



#-------------------------------------------------------------функции для финансов-----------------------------------------------------------------------



#-------------------------------------------------------------функции для админки-----------------------------------------------------------------------



def admin_func(message):
    id_usera = message.from_user.username
    if id_usera == "scheissdreckk":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) 
        btn1 = types.KeyboardButton("Получить общую таблицу")
        btn2 = types.KeyboardButton("Проверить юзера")
        btn3 = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, "Здравствуйте {0.first_name}! Что вы хотели бы сделать?".format(message.from_user), reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "К сожалению, у вас недостаточно прав для выполнения данной операции :(")

def download(message):

    conn = sqlite3.connect('orders.db', check_same_thread=False)
    filename = 'статистика_оценок.xlsx'
    df = pd.read_sql('select * from оценки', conn)
    df.to_excel(filename, index=False)
    bot.send_document(message.chat.id,document=open("статистика_оценок.xlsx", 'rb'))

def print_grades(message):

    username = message.text

    cursor.execute("SELECT * FROM оценки WHERE username=?", (username,))
    res = cursor.fetchone()
    bot.send_message(message.chat.id, f"Вот все оценки юзера @{username}:\n\nФЛЕКС:\n\nТест - {res[4]}\nПроект - {res[5]}\nАудиторка - {res[6]}\nЭкзамен - {res[7]}\nИтоговый накоп - {res[8]}\n\nЭкономика фирмы:\n\nАудиторка - {res[9]}\nТест - {res[10]}\nЭкзамен - {res[11]}\nИтоговый накоп - {res[12]}\n\nСтатистика:\n\nЛетучки - {res[13]}\nПроект - {res[14]}\nПроджект ревью - {res[15]}\nЭкзамен - {res[16]}\nИтоговый накоп - {res[17]}\n\n")
    


bot.infinity_polling()

