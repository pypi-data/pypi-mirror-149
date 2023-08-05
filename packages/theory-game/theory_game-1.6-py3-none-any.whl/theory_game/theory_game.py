from abc import ABC, abstractmethod

class Game(ABC):
    def __init__(self, win_value: int, cases: str):
        self.win_value = win_value
        self.cases = cases.split()
    
    @abstractmethod    
    def hod(self, x):
        pass
    
    def p1(self, x):
        return any((i if isinstance(self, Game1) else sum(i)) >= self.win_value for i in self.hod(x))
    
    def v1(self, x):
        return all(self.p1(i) for i in self.hod(x)) and not self.p1(x)
    
    def v1_n(self, x):
        return any(self.p1(i) for i in self.hod(x)) and not self.p1(x)
    
    def p2(self, x):
        return any(self.v1(i) for i in self.hod(x))
    
    def v2(self, x):
        return all(self.p1(i) or self.p2(i) for i in self.hod(x)) and not (self.p1(x) or self.v1(x))
    
    def gen_output(self):
        yield from ((self.p1, 'Петя первым'), (self.v1, 'Ваня первым'), (self.v1_n, 'Ваня первым (неудачный Пети)'), (self.p2, 'Петя вторым'), (self.v2, 'Ваня вторым или первым'))
    
    @abstractmethod
    def __str__(self):
        pass
             
class Game1(Game):
    '''
Game1(\n\tколичество_камней_для_выигрыша: int,\n\tварианты_ходов_через_пробел: str (Пример: '+1 *3' или '+2 *4')\n)
    '''
    def __init__(self, win_value: int, cases: str):
        super().__init__(win_value, cases)

    def hod(self, x):
        results = []
        for i in self.cases:
            results.append(eval(str(x)+i))
        return results

    def __str__(self):
        results = [f'{tittle}: {[s for s in range(1, self.win_value) if func(s)]}' for func, tittle in self.gen_output()]
        return '\n\n'.join(results)

class Game2(Game):
    '''
Game2(\n\tсумма_камней_для_выигрыша: int,\n\tварианты_ходов_через_пробел: str (Пример: '+1 *3' или '+2 *4'),\n\tколичество_камней_в_первой_куче: int\n)
    '''
    def __init__(self, win_value: int, cases: str, first_bunch: int):
        self.first_bunch = first_bunch
        super().__init__(win_value, cases)
        
    def hod(self, x):
        a,b = x
        results = []
        for i in self.cases:
            results += [(a, eval(str(b)+i)), (eval(str(a)+i), b)]
        return results

    def __str__(self):
        results = [f'{tittle}: {[s for s in range(1, self.win_value - self.first_bunch) if func((self.first_bunch, s))]}' for func, tittle in self.gen_output()]
        return '\n\n'.join(results)

if __name__ == '__main__':
    testObj1 = Game1(30, '+1 *2')
    print(testObj1.__doc__)
    print(testObj1)
    
    testObj2 = Game2(247, '+1 *2', 17)
    print(testObj2.__doc__)
    print(testObj2)