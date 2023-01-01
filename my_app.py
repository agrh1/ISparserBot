'''
рабочая версия v1.1
'''

import os, time, logging
from dotenv import load_dotenv
from msgFilter import message_important_checker
from get_event import parsing_event
from get_next_item import get_item
from tg_bot import send_message

load_dotenv()
# подключение переменных окружения
TG_BOT_KEY=os.getenv('TG_BOT_KEY')
CHAT_ID = os.getenv('CHAT_ID')
SD_LOGIN = os.getenv('SD_LOGIN')
SD_PASSWORD = os.getenv('SD_PASSWORD')
SD_ADDRESS = os.getenv('SD_ADDRESS')

logging.basicConfig(filename='events_tracker.log', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)

def mainfunc():
    '''модуль логики'''
    logging.info("bot restarted")
    # отправка сообщения в группу, если бот запущен или перезагружен
    send_message("I'm Online", TG_BOT_KEY, CHAT_ID)
    # начальное значение таймера, при наполнении которого бот пишет, что он жив
    timer = 0
    # если в отдельном файле (обычно при первом запуске) не указан id последнего существующего сообщения, то используется это
    event_id = 58083
    # файл с номером эвента, с которого начинать прогон.
    file_with_id="event_id"
    # если файла с номером нет (или файл пустой), создать его и положить в него значение evend_id
    if not os.path.exists(file_with_id):
        with open("event_id",'w') as f:
            f.write(str(event_id))
    f = open("event_id", 'r')
    if len(f.readline()) < 2:
        with open("event_id",'w') as f:
            f.write(str(event_id))

    # бесконечный цикл поиска следующего сообщения, его парсинкга и отправки в группу
    while True:
        # читаем номер последнего существуюшего на момент анализа, сообщения
        with open("event_id",'r') as o:
            event_id = int(o.readline())
        # берем id эвента, следующий за последним обработанным
        event_id = event_id + 1
        # проверяем существует ли и если да, вытаскиваем содержимое
        res = get_item(event_id, SD_LOGIN, SD_PASSWORD, SD_ADDRESS)
        # если следующего сообщения нет, то делаем паузу и проверяем еще раз до тех пор пока таймер не накопит пороговое значение
        # после чего в группу отправляется сообщение что бот жив, но нет новых сообщений
        if res is None:
            msg = f"{event_id} is not found"
            time.sleep(600) #600
            timer = timer + 1
            if timer == 48:
                send_message("I'm work, but no new messages.", TG_BOT_KEY, CHAT_ID)
                logging.info(f"timer={timer} event_id={event_id}")
                timer = 0
            continue
        # если сообщение есть, парсим с его страницы данные
        else:
            timer = 0
            message = parsing_event(res)
            ##проверка содержимого сообщения
            ## если важное - отправляем, если не важное - пропускаем
            if message_important_checker(message):
                message = f"{message['Дата']} {message['Тип']}\n{message['Название']}\n{message['Описание'][:220]}"
                send_message(message, TG_BOT_KEY, CHAT_ID)
            # записываем в файл id обработанного сообщения
            with open("event_id",'w') as o:
                o.write(str(event_id))
            logging.info(f"timer={timer} event_id={event_id}")
            time.sleep(1) # убрать
            continue

if __name__ == "__main__":
    mainfunc()