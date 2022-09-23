# pylint: disable=consider-using-f-string,no-value-for-parameter

from json import dumps
from traceback import format_exc
from pymorphy2 import MorphAnalyzer

from functions import check_word_existence, get_new_word
from player import Player

if __name__ == "__main__":
    morph = MorphAnalyzer(lang='ru')

    print('Бот запущен 🚀')
    player = Player()
    player.cword = get_new_word()
    while True:
        #for event in longpoll.check():
        try:
                
                #if event.t.value == 'message_new':
                    #uid: int = event.message['peer_id']
            text = input("Введите слово: ").lower()
                    #print('📩 {}: получено сообщение «{}»'.format(uid, text))

            if not text:
                continue

            
            # ==== АДМИН-ПАНЕЛЬ ====
            '''
                    if uid == ADMIN:
                        if 'data' in text:
                            msg(ADMIN, str('\n'.join([
                                dumps(i, ensure_ascii=False) for i in list(Player.select().dicts().execute())
                            ])))
                            continue

                        if 'clear' in text:
                            action, act_id = text.split()[1], text.split()[2]
                            if not act_id.isdigit() or action not in ['all', 'stats']:
                                msg(ADMIN, 'Некорректный ввод.')
                                continue

                            act_player = Player.get(Player.id == int(act_id))

                            if action == 'all':
                                res = act_player.delete_instance()
                                msg(ADMIN, 'Удалены данные о {} пользователях.'.format(res))
                            elif action == 'stats':
                                act_player.stats = dumps({i: 0 for i in (1, 2, 3, 4, 5, 6, 'wins', 'total')})
                                act_player.save()
                                msg(ADMIN, 'Статистика пользователя @id{} очищена.'.format(act_id))
                            continue

                        if 'помощь' in text or 'help' in text:
                            msg(uid, '– data — выводит всех пользователей из бд\n'
                                  '– clear {stats|all} <id> — очищает данные о пользователе по id\n'
                                  '⠀stats — только статистику\n⠀all — полностью пользователя')
                            continue
                    # ======================
                    

                    if text.split()[-1].startswith('стат') or text.split()[-1].startswith('stat'):
                        stats = player.get_stats()
                        msg(uid, ('Давай посмотрим, как ты играешь 🎮\n'
                                  + '1: {}\n2: {}\n3: {}\n4: {}\n5: {}\n6: {}\n'.format(
                                      *[stats[str(i)] for i in range(1, 7)]
                                  )
                                  + 'Всего выиграно: {} из {} сыгранн{}.'.format(
                                      stats['wins'], stats['total'],
                                      'ой' if stats['total'] % 10 == 1 and stats['total'] % 100 != 11 else 'ых'
                                  )))
                        continue
                    '''

            if text.split()[-1] in ['помощь', 'help']:
                print('Разберёмся, что к чему:\n' +
                                 '⠀– Напиши любое слово из пяти букв и веселье начнётся!\n' +
                                 #'⠀– Напиши «статистика» или «стата», чтобы узнать статистику своих игр.\n'
                                 '⠀– Напиши «помощь» или «help», чтобы вызвать эту прекрасную справку.\n\n' +
                                 'Да начнётся веселье! 🏃🏻‍♂️'
                            )
                continue

            if not player.story:
                player.story = ''

            player.uword = text.split()[-1]

            if not check_word_existence(player.uword):
                print('{}Нет в словаре\n{}'.format(player.story,
                                                              player.used_letters))
                continue

            mask, lmask = '', ['*', '*', '*', '*', '*', '⠀']
            for i in range(5):
                if player.uword[i] == player.cword[i]:
                    mask += '🟩'
                    lmask = list(lmask)
                    if player.uword[i].upper() in lmask[lmask.index('⠀'):]:
                        lmask.remove(player.uword[i].upper())
                    lmask[i] = player.uword[i].upper()
                    lmask = ''.join(lmask)  # type: ignore
                    lmask += player.uword[i].upper()
                elif (player.uword[i] in player.cword
                              and player.uword[:i].count(player.uword[i])
                              != player.cword.count(player.uword[i])
                              and player.uword[i]
                              != player.cword[player.uword.rfind(player.uword[i])]):
                    mask += '🟨'
                    lmask += player.uword[i].upper()
                else:
                    mask += '⬜'
                    lmask += player.uword[i]

                if player.uword[i].upper() in player.used_letters:
                    a = list(player.used_letters)
                    a.remove(player.uword[i].upper())
                    player.used_letters = ''.join(a)

            print('{}{}/6: {}⠀ ⠀{}\n{}'.format(player.story, player.guesses,
                                                          mask, ''.join(lmask), player.used_letters))

            player.story += '{}/6: {}⠀ ⠀{}\n'.format(player.guesses, mask, ''.join(lmask))

            if player.uword == player.cword:
                num_to_word = {1: 'первой', 2: 'второй', 3: 'третьей',
                                       4: 'четвёртой', 5: 'пятой', 6: 'последней'}
                print('''Это победа! Ты угадал слово {} с {} попытки. Так держать! ✊🏻
Больше об этом слове: https://ru.wiktionary.org/wiki/{}.'''.format(
                            player.cword.upper(), num_to_word[player.guesses], player.cword
                        ))
                break
                        #player.win(player.guesses)
            else:
                player.increase_guesses()

            if player.guesses == 7:
                print('''Ты проиграл 😔 Загаданное слово: {0}.
Больше об этом слове: https://ru.wiktionary.org/wiki/{0}.'''.format(player.cword))
                break
                #player.lose()

                #player.save()
        except Exception:
            print('Поймали ошибку. Смотри трейсбек:\n\n{}'.format('\n'.join(format_exc().split('\n')[1:])))

