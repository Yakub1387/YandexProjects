from PIL import Image
import time
from Filters import FILTERS


def approve(a):
    try:
        with Image.open(a) as i:
            i = i.convert('RGB')  # i.load() без надобности
        return i
    except OSError:
        p = stop(input('\nПожалуйста, проверьте верность пути к открываемому файлу и введите его снова! ("0" для остановки)'))
        return approve(p)


def check(a):
    try:
        if int(a) not in FILTERS.keys():
            return True
        else:
            return False
    except TypeError:
        return True


def stop(a):
    if str(a) == '0':
        print("GoodbyeError: До свидания!")
        time.sleep(1)
        exit()
    else:
        return a


def save(a: Image.Image, path):
    try:
        a.save(path)
        print('\nФайл сохранится по закрытии фоторедактора!\n')
    except FileNotFoundError and ValueError:
        path = stop(input('\nПожалуйста, удостоверьтесь в верности введённого пути к изображению\n'
                          'и введите его снова ("0" для выхода) или же напишите "Нет", если сохранять файл не нужно: ')); print()
        if path.lower() != 'нет':
            return save(a, path)


def menu():
    print(f'''Меню фильтров:
    1: {FILTERS[1]["name"]}
    2: {FILTERS[2]["name"]}
    3: {FILTERS[3]["name"]}
    4: {FILTERS[4]["name"]}
    5: {FILTERS[5]["name"]}
    6: {FILTERS[6]["name"]}
    7: {FILTERS[7]["name"]}
    8: {FILTERS[8]["name"]}
    9: {FILTERS[9]["name"]}
    10: {FILTERS[10]["name"]}
    0: Выход
''')
    a: int = stop(input("Выберите фильтр (иначе '0' для выхода): "))
    print()
    return a


def choice():
    ch = menu()
    if check(ch):
        print(f"Пожалуйста, введите номер подходящего фильтра (от {FILTERS.keys()[0]} до {FILTERS.keys()[-1]})\nили завершите программу, введя '0'\n\n")
        return choice()
    else:
        ch = int(ch)
        print(f'{FILTERS[ch]["name"]}:')
        print(f'{FILTERS[ch]["description"]}\n')
        reply = stop(input('Применить фильтр к иозображению (Да/Нет или "0" для выхода)? ')); print()
        while reply.lower() != 'да' and reply.lower() != 'нет':
            reply = stop(input("Введите 'Да' или 'Нет'! ('0' для остановки)")); print()
        if reply.lower() == 'да':
            ans = stop(input("Введите путь к редактируемому изображению ('0' для выхода): "))
            img = approve(ans)
            cl = FILTERS[ch]['class']()
            img = cl.apply_to_image(img)
            print('\nОжидание...')
            img.show()
            print('\nОжидание...')
            time.sleep(3)
            sv = stop(input('\nВведите путь для сохранения файла ("0" для выхода или "нет", если сохранять файл не нужно): '))
            if sv.lower() != 'нет':
                save(img, sv)
                time.sleep(1)
            return choice()
        elif reply.lower() == 'нет':
            return choice()


print('Добро пожаловать в один из лучших фоторедакторов на Python!\n\n')
choice()


