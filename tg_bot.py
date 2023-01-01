'''
модуль взаимодействия с Телеграм
'''
import requests

def send_message(msg, TG_BOT_KEY, CHAT_ID):
    '''
    бот отправляет событие в группу в телеграме
    '''
    url = f"https://api.telegram.org/bot{TG_BOT_KEY}/sendmessage"
    params = {
        "chat_id": CHAT_ID, # mlsup_group
        "text":msg
    }
    return requests.get(url,params=params).text