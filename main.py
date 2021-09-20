from random import randint
import json


def save(user_field_, field_, bombs_, x_field_, y_field_):
    """
    Сохранение незаконченной игры (сохраняется в json файл)
    """
    save_data = {
        "user_field": user_field_,
        "field": field_,
        "bombs": bombs_,
        "x_field": x_field_,
        "y_field": y_field_
    }
    with open("save.json", "w") as file:
        json.dump(save_data, file)


def load():
    """
    Загрузка ранее сохранённой игры (загрузка из json файла)
    """
    with open("save.json", "r") as file:
        load_data = json.load(file)
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
    user_field_ = [['□' for _ in range(x_field)] for __ in range(y_field)]
    return user_field_


def open_field(x, y, user_field, field, x_field, y_field, p):
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
        return ['KABOOM']

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
    if command == '3' or command == 'Выйти':
        print('Пока :(')
        break
    if command == '1' or command == 'Новая игра':
        print('Классический режим или Свои установки?\n1: Классический режим\n2: Свои установки')
        command = input()
        if command == '1' or command == 'Классический режим':
            field, bombs = new_field_generating(5, 5, 2, 5)
            x_field = 5
            y_field = 5
            user_field = new_user_field_generating(5, 5)
        elif command == '2' or command == 'Свои установки':
            print('Введите размеры поля и число бомб 4 цифрами:')
            command = list(map(int, input().split()))
            x_field = command[0]
            y_field = command[1]
            field, bombs = new_field_generating(command[0], command[1], command[2], command[3])
            user_field = new_user_field_generating(command[0], command[1])
    if command == '2' or command == 'Загрузить':
        user_field, field, bombs, x_field, y_field = load()
    while True:
        print_field(x_field, y_field, user_field)
        print("Всего бомб: ", len(bombs))
        print("Команды вида: ЧИСЛО ЧИСЛО КОМАНДА\nКоманды: Flag, Open")
        x, y, action = map(str, input().split())    # [X,Y,Action]
        x = int(x)
        y = int(y)
        if action == 'Save':
            save(user_field, field, bombs, x_field, y_field)
            print("Игра сохранена")
        if action == 'Flag':
            user_field[x - 1][y - 1] = '⚑'
            if field[x - 1][y - 1] == 9:
                bombs_count += 1
        if action == 'Open':
            user_field = open_field(x - 1, y - 1, user_field, field, x_field, y_field, field[x][y])
            if user_field == ['KABOOM']:
                print('Вы проиграли, игра окончена')
                break
        if len(bombs) == bombs_count:
            print('Победа!')
            break
