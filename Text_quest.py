# Бучминский Якуб, 31 группа - 1 проект "Текстовый квест"
import time


def otstup():
    print('\n' + 'Ожидание...')
    time.sleep(5)
    print('\n' * 5)


def close(a):
    if a == '0':
        exit()
    else:
        return a


def gg(a):
    if a == 1:
        print('Вы выиграли! 🏆🏆🏆')
    elif a == 2:
        print("Продолжение следует... 🌲🌲🌲🌲🌲🌲🌲")
    else: print('К сожалению, вы проиграли... ☠☠☠')


def gr(a):
    try:
        print(f"последни{chasy(a)}...")
        otstup()
    except TypeError and ValueError:
        print(f"{end}Пожалуйста, введите число - количество часов\n")
        return gr(close(input(f'Сколько часов вы уже находитесь в лесу?\n')))


def check(g, a):
    while str(g) not in a:
        close(g)
        g = input(f"Выбор вариантов по числам: {a}!\n")
    return g


def chasy(a):
    if int(a) % 100 in [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]:
        return 'е ' + a + " часов"
    elif int(a) % 10 == 1:
        return 'й ' + a + " час"
    elif int(a) % 10 in [2, 3, 4]:
        return 'е ' + a + " часа"
    else:
        return 'е ' + a + " часов"



end = "Напишите '0', чтобы завершить программу.\n\n"
print(f"{end}Введите ваш ник: ")
name = close(input())
print(f"""
Добро пожаловать в The Forest, {name}!
-------------------------------{'-' * len(name)}-

""")
otstup()
print(f"{end}Вы бредете по непроглядному ельнику уже последние... \n")
in_form = close(input(f'Сколько часов вы уже находитесь в лесу?\n'))
gr(in_form)
print(f"{end}Перед вами выбор:"
      f"\n"
      f"    1. Дожидаться спасателей\n"
      f"    2. Пытаться найти кров и пропитание в безлюдном лесу\n"
      f"    3. Пинать пни\n")
in_form = check(close(input(f'Ваш выбор(1, 2 или 3): \n')), ('1', '2', '3'))
otstup()
if in_form == '1':
    print(f'{end}Спасатели прибыли, и по выходу их из затонированных машин, вы замечаете, '
          f'что они имели при себе разного рода оружие, и выглядели, как вам показалось, крайне недоброжелательно...\n')
    print(f'Ваши действия:'
          f'\n'
          f'    1. Откликнуться, позвать на помощь\n'
          f'    2. Отсидеться - они не внушают доверия\n'
          f'    3. Пинать пни\n')
    in_form = check(close(input(f'Ваш выбор(1, 2 или 3): \n')), ('1', '2', '3'))
    otstup()
    if in_form == '1':
        print(f"Вы поступили правильно: спасателей сопровождал конвой, так как в лесах засели браконьеры\n")
        gg(1)
    elif in_form == '2':
        print(f'Вы только что пропустили ваш шанс на спасение, вам ничего не остается, как\n'
              f'выбираться своими силами, или же пытаться снова выйти на связь\n')
        gg(2)
    else:
        print('...\n')
        gg(3)
elif in_form == '2':
    print(f'{end}После долгих дней и ночей вы приноравливаетесь к дикой природе:\n'
          f'перед вами палатка, костер и самодельное приспособление для получения питьевой воды,\n'
          f'однако внезапно вы слышите рев позади вас - так как время событий приходятся на начало весны,\n'
          f'то оказывается, что Вы нечаянно будите медведя ото спячки\n')
    print(f'Ваш план действий:\n'
          f'    1. Залезть на дерево\n'
          f'    2. Лечь навзничь и не двигаться 🤫\n'
          f'    3. Пинать пни\n')
    in_form = check(close(input(f'Ваш выбор(1, 2 или 3): \n')), ('1', '2', '3'))
    if in_form == '1':
        print(f'В панике Вы совсем забываете, что для медведя\n'
              f' не составляет труда забраьтся на дерево и добраться до вас\n')
        gg(3)
    elif in_form == '2':
        print(f'Медведь не видит в вас угрозы и обходит вас стороной, но, к несчастью, съедает все ваши припасы\n')
        gg(2)
    else:
        print(f'К удивлению, это приносит пользу: вы находите схрон:\n'
              f' тайник с оружием, боеприпасами и провизией и успешно покидаете «The Forest»!\n')
        gg(1)
else:
    print(f'...\n')
    gg(3)
print('Отличная игра! 👍')
