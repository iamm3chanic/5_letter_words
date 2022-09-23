from random import choice, randint
from urllib.parse import unquote
from requests import exceptions, get

'''
    Проверяет соединение с русским Викисловарём. 
    Если соединение есть, то возвращает True, иначе — False.
'''
def check_connection() -> bool:
    try:
        response = get('https://ru.wiktionary.org/')
        if not response.ok or response.status_code != 200:
            raise exceptions.ConnectionError
    except exceptions.ConnectionError:
        return False
    return True

    '''
    Проверяет, существует ли слово в введённой форме. Если существует, то возвращает True, иначе — False.
    Параметры
    ---------
    word: str
        слово для проверки
    '''    
def check_word_existence(word: str) -> bool:
    if len(word) != 5:
        return False

    res = get('https://ru.wiktionary.org/w/api.php', {
        'action': 'opensearch',
        'search': word,
        'format': 'json'
    }).json()[1]

    if not res:
        return False
    if word.lower() in [w.lower() for w in res]:
        return True
    return False
    
    '''Получает новое слово из локальной базы пятибуквенных слов.'''
def get_word_from_local() -> str:
    with open('5letters_words.txt', encoding='utf-8') as file:
        return choice(file.readlines())
    
    '''
    Получает новое слово из словаря пятибуквенных слов https://ru.wiktionary.org/wiki/Категория:Слова_из_5_букв/ru.
    При отсутствии доступа к словарю, получает слово из локального словаря.
    '''    
def get_new_word() -> str:
    if not check_connection():
        return get_word_from_local()

    res = get('https://ru.wiktionary.org/wiki/Служебная:RandomInCategory/Слова_из_5_букв/ru')
    word = unquote(res.url).split('/')[-1]
    while (any(case in res.text for case in [
        'имя собственное', 'вульгарное', 'сленговое', ', одушевлённое',
        'разговорное', 'старинное', 'редкое', 'устаревшее'
    ])
            or 'существительное' not in res.text or word == word.title()):
        res = get('https://ru.wiktionary.org/wiki/Служебная:RandomInCategory/Слова_из_5_букв/ru')
        word = unquote(res.url).split('/')[-1]

    return word
        
        
        
        
        
        
            
