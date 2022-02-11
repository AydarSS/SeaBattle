import random


class MyException(Exception):
    def __str__(self):
        return "Ошибка"

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return 'Dot(x='+str(self.x)+', y='+str(self.y)+ ')'



class Ship:
    def __init__(self, length, dot_ship_top, ship_direction):
        self.length = length
        self.dot_ship_top = dot_ship_top
        self.ship_direction = ship_direction
        self.life_count = length

    @property
    def dots(self):
        dots_array = [self.dot_ship_top]
        if self.ship_direction == 'vertical' and self.length > 1:
            for d in range(1,self.length):
                ship_body = Dot(self.dot_ship_top.x + d, self.dot_ship_top.y)
                dots_array.append(ship_body)
        if self.ship_direction == 'horizontal' and self.length > 1:
           for d in range(1,self.length):
               ship_body = Dot(self.dot_ship_top.x, self.dot_ship_top.y + d)
               dots_array.append(ship_body)
        return dots_array


class Board:
    def __init__(self, hid = False, size = 6):
        self.hid = hid
        self.size = 6
        self.count = 0

        self.field = [["O"]*size for s in range(size)]
        self.ships = []
        self.busy = []

    def add_ship(self, ship):
        for d1 in ship.dots:
            if self.out(d1) or d1 in self.busy:
                raise MyException()
        for d1 in ship.dots:
            self.field[d1.x][d1.y] = "■"
            self.busy.append(d1)
        self.ships.append(ship)
        self.contour(ship)

    def contour(self, some_ship, verb = False):
        for d in some_ship.dots:
            for conX in range(-1, 2):
                for conY in range(-1, 2):
                    d1 = Dot(d.x+conX, d.y+conY)
                    if d1.x != -1 and d1.x != 6 and d1.x != 7:
                        if d1.y != -1 and d1.y != 6 and d1.y != 7:
                            if d1 not in self.busy and d1 not in some_ship.dots:
                                if verb:
                                    self.field[d1.x][d1.y] = "."
                                self.busy.append(d1)

    def out(self, dot_for_control):
        if dot_for_control.x not in range(0, self.size) or dot_for_control.y not in range(0, self.size):
            return True
        else:
            return False

    def __str__(self):
        res = ''
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"
        if self.hid:
            res = res.replace("■", "O")
        return res

    def shot(self, dot_shot):
       # if dot_shot in self.busy:
        #    raise MyException
        for ship in self.ships:
            if dot_shot in ship.dots:
                ship.life_count -= 1
                self.field[dot_shot.x][dot_shot.y] = 'X'
                if ship.life_count == 0:
                    self.count += 1
                    print("Корабль уничтожен!")
                    self.contour(ship, verb = True)
                    return False
                else:
                    print("Корабль ранен!")
                    return True
        self.field[dot_shot.x][dot_shot.y] = '.'
        print('Мимо')
        return False

class Player:
    def __init__(self, our, enemy):
        self.our = our
        self.enemy = enemy

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except MyException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(random.randint(0, 5), random.randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cordinats  = input("Введите координаты через пробел: ")
            if len(cordinats.split()) != 2:
                print("Введите 2 числа")
                continue
            if not (cordinats.split()[0].isdigit()) or not (cordinats.split()[1].isdigit()):
                print("Введите числа")
                continue
            x = int(cordinats.split()[0])
            y = int(cordinats.split()[1])

            return Dot(x - 1, y - 1)

class Game:
    def __init__(self):
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        direction = ['vertical', 'horizontal']
        board = Board()
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(l, Dot(random.randint(0, 6), random.randint(0, 6)), random.choice(direction))
                try:
                    board.add_ship(ship)
                    break
                except MyException:
                    pass
        board.busy = []
        return board

    def greet(self):
        print("Морской бой")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.our)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.our)
            if num % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.enemy.count == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.our.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()

g = Game()
g.start()




