from bs4 import BeautifulSoup

def parsing_event(text):
    event_info = {}
    soup = BeautifulSoup(text, "html.parser")
    event_body = soup.find('div', {'class':'formbody'})
    fields = event_body.find_all('div', {'class':'field'})
    for field in fields:
        event_field = field.text.split('\n')[-2].strip()
        if field.find('label',{"for":"name"}):
            key = field.find('label',{"for":"name"}).text.strip()
        if field.find('label',{"for":"Date"}):
            key = field.find('label',{"for":"Date"}).text.strip()
        if field.find('label',{"for":"Type"}):
            key = field.find('label',{"for":"Type"}).text.strip()
        if field.find('label',{"for":"description"}):
            key = field.find('label',{"for":"description"}).text.strip()
        event_field = field.text.split('\n')[-2].strip()
        event_info[key] = event_field
    return event_info #f"{event_info['Дата']} {event_info['Тип']}\n{event_info['Название']}\n{event_info['Описание'][:220]}"