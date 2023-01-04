import easygui as gui

import cards, games

TITLE = "Простые Числа"
ICON ='Prime numbers ikona 90x88.png'

#gui.msgbox('Приветствуем вас в карточной игре "Простые Числа", соединяющей в себе карты и математику!', TITLE, image=ICON)
#prav = games.ask_yes_no('Знакомы ли вам нашы правила?', TITLE)
#if not prav:
    #gui.msgbox('Правила, на самом деле, не та уж и сложны. Сначала, каждому из вас раздаётся по 11-ть карт, затем, из колоды берётся верхняя карта, ', TITLE, image=ICON)

class Prime_Card(cards.Card):
    """Карта для игры в Простые Числа."""
    @property
    def value(self):
        v = Prime_Card.RANKS.index(self.rank) + 1
        return v

class Prime_Deck(cards.Deck):
    """Колода для игры в Простые Числа."""
    def populate(self):
        for suit in Prime_Card.SUITS: 
            for rank in Prime_Card.RANKS: 
                self.cards.append(Prime_Card(rank, suit))

class Prime_Hand(cards.Hand):
    """Рука игрока в Простые Числа."""
    def __init__(self, name):
        super(Prime_Hand, self).__init__()
        self.name = name

    def __str__(self):
        rep = self.name + ":\t" + super(Prime_Hand, self).__str__()       
        return rep

class Prime_Game:
    """Игра в Простые Числа"""
    def __init__(self, names):
        self.totalvalue = 0

        self.players = []
        for name in names:
            player = Prime_Hand(name)
            self.players.append(player)
        
        self.firstcard = Prime_Hand('The First Card')

        self.deck = Prime_Deck()
        self.deck.populate()
        self.deck.shuffle()
    
    def checking_the_end(self):
        for player in self.players:
            for card in player.cards:
                if is_prime(self.totalvalue + card.value):
                    return True
        else:
            return False
    
    def __put_card(self, player):
        image = player.card_images()
        response = gui.msgbox(str(player) + 
            "\nКакую карту положите в стопку? Текущая сумма значений карт: " + str(self.totalvalue), TITLE,
            'Пропуск хода', image=player.card_images())
        if response == 'Пропуск хода' or response == None:
            gui.msgbox('У игрока ' + player.name + ' нет соответствующей карты, чтобы положить её в стопку, текущая сумма значений карт: ' + str(self.totalvalue), TITLE, player.name + ', ' + player.name + '...')
        elif not is_prime(int(response[-6:-4]) + self.totalvalue):
            gui.msgbox('Сумма значения этой карты с текущей суммой значений карт, к сожалению, не даёт простого числа. Попробуйте ещё раз.', TITLE, 'Я просто гуманитарий!')
            recurs_player = player
            self.__put_card(recurs_player)
        else:
            self.totalvalue += int(response[-6:-4])
            gui.msgbox('Игрок ' + player.name + ' положил свою карту в стопку, текущая сумма значений карт: ' + str(self.totalvalue), TITLE, 'Кто ходит следующий?', image=response)
            cardindex = image.index(response)
            del player.cards[cardindex]
            
    
    def play(self):
        self.deck.deal(self.players, per_hand=11)
        gui.msgbox('\n'.join(
            (str(player) for player in self.players)
        ), TITLE, 'Далее')
        self.deck.deal([self.firstcard])
        self.totalvalue += self.firstcard.cards[0].value
        gui.msgbox('Первая карта стопки: ' + str(self.firstcard.cards[0]) + '. Текущая сумма значений карт: ' + str(self.totalvalue), TITLE, 'Любопытно...', image=self.firstcard.card_images())
        still_playing = True
        while still_playing:
            for player in self.players:
                self.__put_card(player)
                still_playing = self.checking_the_end()
                if not still_playing:
                    break
        gui.msgbox('Игра окончена.' + '\nТекущая сумма значений карт: ' + str(self.totalvalue) + '. \nКарты на руках у игроков: \n' + '\n'.join((str(player) for player in self.players)), TITLE, 'А я только начал!')
        gui.msgbox('Победил игрок ' + player.name + ', ведь после него никто более не в состоянии сделать ход.', TITLE, 'Поприветствуем же победителя!!!')
        for player in self.players:
            player.clear()
        self.firstcard.clear()
        self.totalvalue = 0

def is_prime(n):
    if n >= 2:
        for i in range(2, int((n ** 0.5)) + 1):
            if n % i == 0:
                return False
        else:
            return True
    else:
        return False

def main():
    gui.msgbox('Приветствуем вас в карточной игре "Простые Числа", соединяющей в себе карты и математику!', TITLE, 'Здрасте', image=ICON)
    prav = games.ask_yes_no('Знакомы ли вам нашы правила?', TITLE)
    if not prav:
        gui.msgbox('Правила, на самом деле, не та уж и сложны. Сначала, каждому из игроков раздаётся по 11-ть карт, затем, из колоды берётся верхняя карта, которая выступает в роли стартовой, нижней карты игральной стопки.', TITLE, 'Далее', image=ICON)
        gui.msgbox('Игрок, который ходит первым, должен положить карту, которая в сумме со стартовой будет образовывать простое число (то есть то натуральное число, большее, чем единица и не имеющее других делителей, кроме самого себя и единицы).', TITLE, 'Далее', image=ICON)
        gui.msgbox('Следующий же игрок должен положить в стопку карту, которая вместе со всеми предыдущими картами из стопки также образует простое число, если же игрок карты, подходящей для данного действия, не имеет, он пропускает ход.', TITLE, 'Далее', image=ICON)
        gui.msgbox('Игра продолжается до тех пор, пока не останется ни одного игрока, способного сделать ход. Победителем считается тот игрок, который походил последним.', TITLE, 'Далее', image=ICON)
        gui.msgbox('Стоимость различных карт: туз - единица, от 2 до 10 включительно соответствуют номиналу карты, валет - 11, дама - 12, король - 13.', TITLE, 'Я не робот.', image=ICON)
    names = []
    number = games.ask_number("Сколько всего игроков? (1 - 4): ", 
        low = 1, high = 4)
    if number is None:
        exit()
    fields = ["Игрок"+str(i + 1) for i in range(number)]
    names = gui.multenterbox('Введите имена игроков', TITLE, fields=fields, values=fields)
    if names is None:
        exit()
    game = Prime_Game(names)
    again = True
    while again:
        game.play()
        again = games.ask_yes_no("Хотите сыграть еще раз?", TITLE)



main()