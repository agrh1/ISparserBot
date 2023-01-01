
import requests



def get_item(event_id, SD_LOGIN, SD_PASSWORD, SD_ADDRESS):
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