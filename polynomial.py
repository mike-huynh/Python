class Polynomial:
    def __init__(self, terms):
        self.terms = []
        for term in terms:
            if isinstance(term, Monomial):
                self.terms.append(term)
            else:
                self.terms.append(Monomial(*term))

    def evaluate(self, x):
        newList = []
        for term in self.terms:
            newList.append(Monomial.evaluate(term, x))
        return sum(newList)

        pass

    def __add__(self, other):
        resultList = []
        for i in self.terms:
            resultList.append(i)
        for i in other.terms:
            resultList.append(i)
        
        return Polynomial(resultList).reduce()
        
    
        pass

    def __mul__(self, other):
        resultList = []
        for x in self.terms:
            for y in other.terms:
                resultList.append(Monomial.__mul__(x, y))

        return Polynomial(resultList)

        pass

    # Combine like terms and eliminate zero monomials.
    def reduce(self):
        commonterms = {}
        for term in self.terms:
            if term.exp in commonterms:
                commonterms[term.exp] += term.coeff
            else:
                commonterms[term.exp] = term.coeff
        # Rebuild the list of terms
        self.terms = []
        for e,c in commonterms.items():
            if c != 0:
                self.terms.append(Monomial(c,e))
        self.terms.sort()
        return self

    def __eq__(self, other):
        self.reduce()
        other.reduce()
        return self.terms == other.terms

    def __neg__(self):
        return self * Monomial(-1,0)

    def __sub__(self, other):
        return self + (-other)

    def __call__(self, x):
        return self.evaluate(x)

    def prime(self):
        newPoly = []
        for term in self.terms:
            newPoly.append(Monomial.prime(term))
        return Polynomial(newPoly)

    def root(self, guess = 0, iterations = 50):
        for i in range(iterations):
            
            x = guess
            y = self.evaluate(x)
            z = self.prime().evaluate(x)
            try:               
                guess = x - (y / z)
            except ZeroDivisionError:
                x = 1
            
        return guess    

class Monomial(Polynomial):
    def __init__(self, coeff, exp):
        self.coeff = coeff
        self.exp = exp
        Polynomial.__init__(self, [self])

    def evaluate(self, x):
        try:
            return self.coeff * (x ** self.exp)
        except ZeroDivisionError:
            return 0

    def __eq__(self, other):
        # Make sure other is a Monomial.
        if isinstance(other, Monomial):
            if self.coeff == 0 and other.coeff == 0:
                return True
            else:
                return self.exp == other.exp and self.coeff == other.coeff
        else:
            return NotImplemented

    def __lt__(self, other):
        return (self.exp, self.coeff) < (other.exp, other.coeff)

    def __mul__(self, other):
        # Make sure other is a Monomial.
        if isinstance(other, Monomial):
            return Monomial(self.coeff * other.coeff, self.exp + other.exp)
        else:
            return NotImplemented

    def prime(self):
        x = self.coeff
        y = self.exp
        
        if y == 0:
            x = 0
        else:
            x = x * y
            y = y - 1

        return Monomial(x, y)


