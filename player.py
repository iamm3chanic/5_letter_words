from functions import get_new_word

class Player():
    cword = None
    guesses = 1
    story = ''
    uword = None
    used_letters = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    '''def __init__(self):
        #id = IntegerField(primary_key=True)
        cword = None
        guesses = 1
        story = ''
        uword = None
        used_letters = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        #stats = TextField(default=dumps({i: 0 for i in (1, 2, 3, 4, 5, 6, 'wins', 'total')}))
        #everyday_word = TextField(default='')
        #everyday_stats = TextField(default=dumps({i: 0 for i in (1, 2, 3, 4, 5, 6, 'wins', 'total')}))'''

    def new_game(self, cword: str = None):
        self.cword = get_new_word() if not cword else cword
        self.uword, self.guesses, self.story = '', 1, ''
        self.used_letters = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        #self.save()

    def increase_guesses(self):
        self.guesses += 1
        #self.save()

    '''def win(self, guess: int, is_everyday: bool = False):
        stats_from_bd = loads(self.stats if is_everyday else self.everyday_stats)
        print(stats_from_bd)
        stats_from_bd[str(guess)] += 1
        stats_from_bd['wins'] += 1
        stats_from_bd['total'] += 1
        if is_everyday:
            self.everyday_stats = dumps(stats_from_bd)
        else:
            self.stats = dumps(stats_from_bd)
        self.new_game()

    def lose(self, is_everyday: bool = False):
        stats_from_bd = loads(self.stats if is_everyday else self.everyday_stats)
        stats_from_bd['total'] += 1
        if is_everyday:
            self.everyday_stats = dumps(stats_from_bd)
        else:
            self.stats = dumps(stats_from_bd)
        self.new_game()

    def get_stats(self):
        return loads(self.stats)

    def get_everyday_stats(self):
        return loads(self.everyday_stats)

    class Meta:
        table_name = 'Data' '''

