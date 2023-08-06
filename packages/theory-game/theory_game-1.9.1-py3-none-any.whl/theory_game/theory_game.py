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

    def p3(self, x):
        return any(self.v2(i) for i in self.hod(x))
    
    def gen_output(self):
        yield from ((self.p1, 'Петя первым'), (self.v1, 'Ваня первым'), (self.v1_n, 'Ваня первым (неудачный Пети)'), (self.p2, 'Петя вторым'), (self.v2, 'Ваня вторым или первым'), (self.p3, 'Петя третьим'))
    
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
    def __init__(self, win_value: int, cases: str, first_heap: int):
        super().__init__(win_value, cases)
        self.first_heap = first_heap
        
    def hod(self, x):
        a,b = x
        results = []
        for i in self.cases:
            results += [(a, eval(str(b)+i)), (eval(str(a)+i), b)]
        return results

    def __str__(self):
        results = [f'{tittle}: {[s for s in range(1, self.win_value - self.first_heap) if func((self.first_heap, s))]}' for func, tittle in self.gen_output()]
        return '\n\n'.join(results)

class Game1Ceil(Game1):
    '''
Game1Ceil(\n\tколичество_камней_для_выигрыша: int,\n\tварианты_ходов_через_пробел: str (Пример: '+1 *3' или '+2 *4'),\n\tмаксимальное_количество_камней_для_выигрыша: int\n)
    '''
    def __init__(self, win_value: int, cases: str, max_win_value: int):
        super().__init__(win_value, cases)
        self.max_win_value = max_win_value
        
    def hod(self, x):
        results = []
        if x > self.max_win_value:
            results.append(self.max_win_value-1)
        for i in self.cases:
            results.append(eval(str(x)+i))
        return results
        
    def p1(self, x):
        return any(self.max_win_value >= i >= self.win_value for i in self.hod(x))
    
class Game2Ceil(Game1):
    '''
Game2Ceil(\n\tсумма_камней_для_выигрыша: int,\n\tварианты_ходов_через_пробел: str (Пример: '+1 *3' или '+2 *4'),\n\tколичество_камней_в_первой_куче: int,\n\tмаксимальное_количество_камней_для_выигрыша: int\n)
    '''
    def __init__(self, win_value: int, cases: str, first_heap: int, max_win_value: int):
        super().__init__(win_value, cases, first_heap)
        self.max_win_value = max_win_value
        
    def hod(self, x):
        a,b = x
        results = []
        if sum(x) > self.max_win_value:
            results.append((self.max_win_value-2, 1))
        for i in self.cases:
            results += [(a, eval(str(b)+i)), (eval(str(a)+i), b)]
        return results
    
    def p1(self, x):
        return any(self.max_win_value >= sum(i) >= self.win_value for i in self.hod(x))