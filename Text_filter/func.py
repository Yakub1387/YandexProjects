import re


def camel_filter(a):
    up = True
    result = ''
    for i in a:
        if i == ' ':
            up = True
        elif up:
            up = False
            result += i.upper()
        else:
            result += i
    return result


def snake_filter(a):
    return a.replace(' ', '_')


def shouting_filter(a):
    return a.upper()


def whispering_filter(a):
    return a.lower()


def spacing_filter(a):
    delim = '.,;!?'
    for i in range(len(a)):
        if i != len(a) and a[i] in delim and a[i + 1] != ' ':
            a = a[:i + 1] + ' ' + a[i + 1:]
    return a


def such_a_nice_filter(a):
    for i in ',;-_!&~:()? ':
        a = '👍'.join(a.split(i))
    return a


def funny_filter(a):
    abc = 'абвгдеёжзийклмнопрстуфхцчшщуьыъэюяabcdefghijklmnopqrstuvwxyz'
    f = True
    res = ''
    for i in a:
        if i.lower() in abc:
            if f:
                res += i.upper()
                f = False
            else:
                res += i.lower()
                f = True
        else:
            res += i
    return res


filters = {
    1: {
        'name': 'CamelFilter',
        'description': 'Фильтр возвращает строку в формате CamelCase '
                       '(без пробелов, а каждое слово начинается с большой буквы), \n'
                       'пр.: "Длинный код" -- > "ДлинныйКод"',
        'function': camel_filter
    },
    2: {
        'name': 'Snake_filter',
        'description': 'Фильтр преобразует пробелы в строке в "_", \n'
                       'пр.: "Черный питон на дереве" --> "Черный_питон_на_дереве"',
        'function': snake_filter
    },
    3: {
        'name': 'SHOUTING filter',
        'description': 'Фильтр преобразует все буквы в строке в большие,\n'
                       'пр.: "На Руси жить хорошо" --> "НА РУСИ ЖИТЬ ХОРОШО"',
        'function': shouting_filter
    },
    4: {
        'name': 'whispering filter',
        'description': 'Фильтр преобразует все буквы в строке в строчные, \n'
                       'пр.: "Башмачкин Акакий Акакиевич" --> "башмачкин акакий акакиевич"',
        'function': whispering_filter
    },
    5: {
        'name': '«S p a c i n g» filter',
        'description': 'Фильтр проверяет наличие пробелов после знаков препинания (",", ";", ".", "...", "!", "?") '
                       'и при их отсутсвтии соответсвенно добавляет их, \n'
                       'пр.: "Мороз и солнце;день чудесный!" --> "Мороз и солнце; день чудесный! "',
        'function': spacing_filter
    },
    6: {
        'name': 'FuNnY filter',
        'description': 'Возвращает строку с чередующимися прописными и строчными буквами '
                       '(при условии, что символы принадлежат русскому или английскому алфавиту), \n'
                       'пр.: "Большие города" --> "БоЛьШиЕ гОрОдА"',
        'function': funny_filter
    },
    7: {
        'name': 'Such👍a👍nice👍filter',
        'description': 'Фильтр возвращает вводимую строку, заменяя все разделители (знаки препинания) смайликом "👍"\n'
                       'если они входят в данный список: ".", ",", ";", "-", "_", "!", "&", "~", "(", ")", "?", ":", \n'
                       'пр.: "Спорт - залог здоровья!" --> "Спорт👍залог👍здоровья👍"',
        'function': such_a_nice_filter
    }
}