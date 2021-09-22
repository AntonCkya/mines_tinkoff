from random import randint
import json


def save(user_field_, field_, bombs_, x_field_, y_field_):
    """
    Сохранение незаконченной игры (сохраняется в json файл)
    Также реализуется шифрование сдвигом всех символов по их коду
    """
    save_data = {
        "user_field": user_field_,
        "field": field_,
        "bombs": bombs_,
        "x_field": x_field_,
        "y_field": y_field_
    }
    s = json.dumps(save_data)
    ss = ''
    for i in range(len(s)):
        ss += chr(ord(s[i]) - 1)
    save_string = {
        0: ss
    }
    with open("save.json", "w") as file:
        json.dump(save_string, file)


def load():
    """
    Загрузка ранее сохранённой игры (загрузка из json файла)
    И расшифровка
    """
    load_string = ['']
    with open("save.json", "r") as file:
        load_string[0] = json.loads(file.readline())
    s = load_string[0]['0']
    ss = ''
    for i in range(len(s)):
        ss += chr(ord(s[i]) + 1)
    load_data = json.loads(ss)
    user_field_ = load_data["user_field"]
    field_ = load_data["field"]
    bombs_ = load_data["bombs"]
    x_field_ = load_data["x_field"]
    y_field_ = load_data["y_field"]
    return user_field_, field_, bombs_, x_field_, y_field_


def new_field_generating(x_field, y_field, min_bombs, max_bombs):
    """
    Функция генерирует поле размера x_field*y_field с min_bombs - max_bombs бомбами

    0 - пустая ячейка без бомб вокруг
    1-8 - пустая ячейка возле бомбы, обозначает количество бомб возле неё
    9 - бомба
    """
    field = [[0 for _ in range(x_field)] for __ in range(y_field)]
    bombs_count = randint(min_bombs, max_bombs)
    bombs = []
    for _ in range(bombs_count):
        x, y = randint(0, x_field - 1), randint(0, y_field - 1)
        while (x, y) in bombs:
            x, y = randint(0, 4), randint(0, 4)
        if (x, y) not in bombs:
            bombs.append((x, y))
            field[x][y] = 9
            if x > 0:
                if field[x - 1][y] < 9:
                    field[x - 1][y] += 1
                if y > 0 and field[x - 1][y - 1] < 9:
                    field[x - 1][y - 1] += 1
                if y < y_field - 1 and field[x - 1][y + 1] < 9:
                    field[x - 1][y + 1] += 1
            if x < x_field - 1:
                if field[x + 1][y] < 9:
                    field[x + 1][y] += 1
                if y > 0 and field[x + 1][y - 1] < 9:
                    field[x + 1][y - 1] += 1
                if y < y_field - 1 and field[x + 1][y + 1] < 9:
                    field[x + 1][y + 1] += 1
            if y > 0 and field[x][y - 1] < 9:
                field[x][y - 1] += 1
            if y < y_field - 1 and field[x][y + 1] < 9:
                field[x][y + 1] += 1

    return field, bombs


def print_field(x_field, y_field, field):
    """
    Функция выводит поле вида:
       1 2 3
       - - -
    1 |0 0 0
    2 |0 0 0
    3 |0 0 0
    """
    print('   ' + ' '.join([str(_) for _ in range(1, x_field + 1)]))
    print('   ' + ' '.join(['-' for _ in range(1, x_field + 1)]))
    for i in range(y_field):
        print(str(i + 1) + '| ' + ' '.join(str(_) for _ in field[i]))


def new_user_field_generating(x_field, y_field):
    """
    Функция генерирует поле x_field*y_field, заполненное символами □
    Такое поле выводится пользователю
    """
    user_field_ = [['□' for _ in range(x_field)] for __ in range(y_field)]
    return user_field_


def open_field(x, y, user_field, field, x_field, y_field, p):
    """
    Функция "открывает" ячейки на поле пользователя
    В координатах открытия открывается ячейка и реккурентно открываются остальные, пока не дойдёт до клеток с цифрами
    включительно
    В случае открытия бомбы, возвращает ['KABOOM', []] - маркер поражения
    """
    if field[x][y] < 9:
        user_field[x][y] = field[x][y]
        if x + 1 < x_field:
            if field[x + 1][y] != 9 and user_field[x + 1][y] == '□' and (p == 0 or field[x + 1][y] == 0):
                user_field = open_field(x + 1, y, user_field, field, x_field, y_field, field[x + 1][y])
        if x - 1 >= 0:
            if field[x - 1][y] != 9 and user_field[x - 1][y] == '□' and (p == 0 or field[x - 1][y] == 0):
                user_field = open_field(x - 1, y, user_field, field, x_field, y_field, field[x - 1][y])
        if y + 1 < y_field:
            if field[x][y + 1] != 9 and user_field[x][y + 1] == '□' and (p == 0 or field[x][y + 1] == 0):
                user_field = open_field(x, y + 1, user_field, field, x_field, y_field, field[x][y + 1])
        if y - 1 >= 0:
            if field[x][y - 1] != 9 and user_field[x][y - 1] == '□' and (p == 0 or field[x][y - 1] == 0):
                user_field = open_field(x, y - 1, user_field, field, x_field, y_field, field[x][y - 1])
        return user_field
    else:
        return ['KABOOM', []]

"""
Начало программы
"""
while True:
    print("Игра \"Сапёр\"")
    print("Введите команду:\n1:Новая игра\n2:Загрузить\n3:Выйти")
    command = input()
    field = [[]]
    user_field = [[]]
    x_field = 0
    y_field = 0
    bombs_count = 0
    bombs = 0
    """
    1: начало новой игры
    2: загрузка игры
    3: выход из игры (прекращение работы программы)
    """
    if command == '3' or command == 'Выйти':
        print('Пока :(')
        break
    if command == '1' or command == 'Новая игра':
        print('Классический режим или Свои установки?\n1: Классический режим\n2: Свои установки')
        command = input()
        """
        Классический режим - работа программы по тз пункта а
        Свои установки - работа программы по тз пункта б
        тз пункта в не реализованно
        """
        if command == '1' or command == 'Классический режим':
            field, bombs = new_field_generating(5, 5, 2, 5)
            x_field = 5
            y_field = 5
            user_field = new_user_field_generating(5, 5)
        elif command == '2' or command == 'Свои установки':
            print('Введите размеры поля:')
            command = list(map(int, input().split()))
            x_field = command[0]
            y_field = command[1]
            print('Введите количество бомб: от скольки до скольки (если хотите видеть точное число бомб, введите 2'+
                  'одинаковых числа)')
            command = list(map(int, input().split()))
            field, bombs = new_field_generating(x_field, y_field, command[0], command[1])
            user_field = new_user_field_generating(x_field, y_field)
    if command == '2' or command == 'Загрузить':
        user_field, field, bombs, x_field, y_field = load()
    while True:
        """
        Игровой процесс
        """
        print_field(x_field, y_field, user_field)
        x, y, action = '', '', ''
        print("Всего бомб: ", len(bombs))
        print("Команды вида: ЧИСЛО ЧИСЛО КОМАНДА\nКоманды: Flag, Open")
        print("Save - схранить игру, Menu - выход в главное меню (игра не сохраняется!)")
        command = input()    # [X,Y,Action]
        if command == 'Save':
            save(user_field, field, bombs, x_field, y_field)
            print("Игра сохранена")
            continue
        elif command == 'Menu':
            break
        else:
            x, y, action = map(str, command.split())
        x = int(x)
        y = int(y)
        if action == 'Flag':
            """
            Игра оканчивается победой только в случае, если все бомбы были отмечены
            """
            user_field[x - 1][y - 1] = '⚑'
            if field[x - 1][y - 1] == 9:
                bombs_count += 1
        if action == 'Open':
            user_field = open_field(x - 1, y - 1, user_field, field, x_field, y_field, field[x - 1][y - 1])
            if user_field == ['KABOOM', []]:
                print('Вы проиграли, игра окончена')
                break
        if len(bombs) == bombs_count:
            print('Победа!')
            break
