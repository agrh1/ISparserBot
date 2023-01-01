'''
рабочая версия
создается сессия, генерятся события
'''
#TODO придумать как фиксировать последнее выводимое событие для перезапуска
#TODO придумать как проверять что события в системе вообще есть


import os, time
from bs4 import BeautifulSoup
import requests, logging
import os
from dotenv import load_dotenv
load_dotenv()

TG_BOT_KEY=os.getenv('TG_BOT_KEY')
CHAT_ID = os.getenv('CHAT_ID')
SD_LOGIN = os.getenv('SD_LOGIN')
SD_PASSWORD = os.getenv('SD_PASSWORD')
SD_ADDRESS = os.getenv('SD_ADDRESS')

logging.basicConfig(filename='events_tracker.log', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)

def message_important_checker(msg):
    if "Информация. Сервисное обслуживание БД" in msg['Название'][:220]:
        print(msg)
        return False
    elif "Заявка не создана. Письмо распознано как служебное." in msg['Описание'][:220]:
        print(msg)
        return False
    elif "Заявка не создана. Письмо распознано как автоответ." in msg['Описание'][:220]:
        print(msg)
        return False
    elif "Пользователь Arsentiy Cherkasov удалил записи в таблицах: Task" in msg['Название'][:220]:
        print(msg)
        return False
    elif "Пользователь Черкасов Арсентий Владимирович удалил записи в таблицах: Task" in msg['Название'][:220]:
        print(msg)
        return False   
    elif "Пользователь Сергей Калыгин удалил записи в таблицах: Task" in msg['Название'][:220]:
        print(msg)
        return False
    elif "Пользователь AR удалил записи в таблицах: Task" in msg['Название'][:220]:
        print(msg)
        return False
    elif "Пользователь Администратор удалил записи в таблицах: Task" in msg['Название'][:220]:
        print(msg)
        return False   
        return True

def send_message(msg):
    '''
    бот отправляет событие в группу в телеграме
    '''
    url = f"https://api.telegram.org/bot{TG_BOT_KEY}/sendmessage"
    params = {
        "chat_id": CHAT_ID, # mlsup_group
        "text":msg
    }
    return requests.get(url,params=params).text

def get_item(event_id):
    '''
    поключаемся к странице сообщения, и если такая страница есть - возвращаем ее.
    '''
    with requests.Session() as session:
        payload = {'login' : SD_LOGIN, 'password' : SD_PASSWORD}
        headers={"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
        rs = session.post(f"{SD_ADDRESS}/registertask.ivp", headers=headers, data=payload)
        r = session.get(f"{SD_ADDRESS}/eventlog.ivp/view/{event_id}", cookies=rs.cookies)

        if r.status_code == 200:
            text = r.text
            return text
        else:
            return None

def get_event(text):
    event_info = {}
    soup = BeautifulSoup(text, "html.parser")
    event_body = soup.find('div', {'class':'formbody'})
    fields = event_body.find_all('div', {'class':'field'})
    for field in fields:
        event_field = field.text.split('\n')[-2].strip()
        print(event_field)
        if field.find('label',{"for":"name"}):
            key = field.find('label',{"for":"name"}).text.strip()
        if field.find('label',{"for":"Date"}):
            key = field.find('label',{"for":"Date"}).text.strip()
        if field.find('label',{"for":"Type"}):
            key = field.find('label',{"for":"Type"}).text.strip()
        if field.find('label',{"for":"description"}):
            key = field.find('label',{"for":"description"}).text.strip()
        print(key)
        event_field = field.text.split('\n')[-2].strip()
        event_info[key] = event_field
    return event_info #f"{event_info['Дата']} {event_info['Тип']}\n{event_info['Название']}\n{event_info['Описание'][:220]}"


def mainfunc():
    logging.info("bot restarted")
    send_message("I'm Online")

    timer = 0
    event_id = 58082

    file_with_id="event_id"
    if not os.path.exists(file_with_id):
        with open("event_id",'w') as f:
            f.write(str(event_id))
    f = open("event_id", 'r')
    if len(f.readline()) < 2:
        with open("event_id",'w') as f:
            f.write(str(event_id))

    while True:
        with open("event_id",'r') as o:
            event_id = int(o.readline())
        event_id = event_id + 1
        res = get_item(event_id)
        if res is None:
            msg = f"{event_id} is not found"
            time.sleep(600) #600
            timer = timer + 1
            if timer == 48:
                send_message("I'm work, but no new messages.")
                logging.info(f"timer={timer} event_id={event_id}")
                timer = 0
            continue
        else:
            timer = 0
            message = get_event(res)

            ##проверка содержимого сообщения
            ## если важное - отправляем
            if message_important_checker(message):
                message = f"{message['Дата']} {message['Тип']}\n{message['Название']}\n{message['Описание'][:220]}"
                send_message(message)
            
            with open("event_id",'w') as o:
                o.write(str(event_id))
            logging.info(f"timer={timer} event_id={event_id}")
            time.sleep(1) # убрать
            continue



if __name__ == "__main__":
    mainfunc()