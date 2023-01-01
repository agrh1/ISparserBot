def message_important_checker(msg):
    if "Информация. Сервисное обслуживание БД" in msg['Тип'][:220]:
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
    elif "Пользователь Калыгин Сергей удалил записи в таблицах: Task" in msg['Название'][:220]:
        print(msg)
        return False
    elif "Пользователь AR удалил записи в таблицах: Task" in msg['Название'][:220]:
        print(msg)
        return False
    elif "Пользователь Администратор удалил записи в таблицах: Task" in msg['Название'][:220]:
        print(msg)
        return False   
    return True

if __name__ == "__main__":
    pass