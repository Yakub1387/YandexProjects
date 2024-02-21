# Бучминский Якуб | 31 группа
from func import *
import time


def check(a):
    try:
        if int(a) not in [1, 2, 3, 4, 5, 6, 7]:
            return True
        else:
            return False
    except TypeError:
        return True


def stop(a):
    if str(a) == '0':
        print("До свидания!")
        time.sleep(1)
        exit()
    else:
        return a


def menu():
    print(f'''Меню фильтров:
    1: {filters[1]["name"]}
    2: {filters[2]["name"]}
    3: {filters[3]["name"]}
    4: {filters[4]["name"]}
    5: {filters[5]["name"]}
    6: {filters[6]["name"]}
    7: {filters[7]["name"]}
    0: Выход
''')
    a: int = stop(input("Выберите фильтр (или '0' для выхода): "))
    print()
    return a

def choice():
    ch = menu()
    # not(isinstance(ch, int)) or
    if check(ch):
        print("Пожалуйста, введите номер подходящего фильтра (от 1 до 7)\nили завершите программу, введя '0'\n\n")
        return choice()
    else:
        ch = int(ch)
        print(f'{filters[ch]["name"]}:')
        print(f'{filters[ch]["description"]}\n')
        reply = ('Применить фильтр к тексту (Да/Нет или "0" для выхода)? ')
        while reply.lower() != 'да' and reply.lower() != 'нет':
            reply = stop(input("Введите 'Да' или 'Нет'! ('0' для остановки)"))
        if reply.lower() == 'да':
            ans = stop(input("Введите текст для фильтрации: "))
            print(f'\nРезультат: {filters[ch]["function"](ans)}\n\n')
            time.sleep(3)
            return choice()
        elif reply.lower() == 'нет':
            return choice()


print("Добро пожаловать!")
choice()
