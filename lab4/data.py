from datetime import datetime, timedelta

#TASK1

def subtract_five_days():
    current_date = datetime.now()
    new_date = current_date - timedelta(days=5)
    print("Сегодняшний день", current_date.strftime("%Y-%m-%d"))
    print("5 дней назад", new_date.strftime("%Y-%m-%d"))

#TASK2

def TYT():
    today = datetime.now()
    tomorrow = today + timedelta(day=1)
    yesterday = today - timedelta(day=1)
    print("Вчера было: ", yesterday.strftime("%Y-%m-%d"))
    print("Сегодня: ", today.strftime("%Y-%m-%d"))
    print("Завтра будет: ", tomorrow.strftime("%Y-%m-%d"))

#TASK3
def Micro():
    now = datetime.now().replace(microsecond=0)
    print("Дата и время без микросекунд", now)


#Task4
def Date_deff(date1, date2):
    diff = abs((date2 - date1).total_second())
    print("Разница в секундах", diff)
