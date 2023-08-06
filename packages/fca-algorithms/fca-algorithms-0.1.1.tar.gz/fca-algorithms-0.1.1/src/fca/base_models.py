from typing import List


class Context:
    def __init__(self, O, A, I):
        """
        :param O: a list of objects (strings for the moment) len(O) = n
        :param A: a list of attributes (strings for the moment) len(A) = m
        :param I: a nm incidence matrix, beign I[i][j] = 1 if object i has the attribute j, 0 <= i <= n, 0 <= j <= m
        """
        self.O : List = O
        self.A : List = A
        self.I : List = I
    
    def derivative(self, Y, is_attr : bool = True):
        """
        :param Y: A subset of A
        """
        return self._derivative_attr(Y) if is_attr else self._derivative_obj(Y)

    def _derivative_attr(self, Y):
        res = set()
        for attr in Y:
            attr_idx = self.A.index(attr)
            for obj in self.O:
                obj_idx = self.O.index(obj) 
                if I[obj_idx][attr_idx]:
                    res.add(obj)
        return list(res)
    
    def _derivative_obj(self, Objs):
        res = set()
        for obj in Objs:
            obj_idx = self.O.index(obj) 
            for attr in self.A:
                attr_idx = self.A.index(attr)
                if I[obj_idx][attr_idx]:
                    res.add(attr)
        return list(res)

    def __repr__(self):
        return f'O: {self.O},\n' \
               f'A: {self.A},\n' \
               f'I: {self.I}'


class Concept:
    def __init__(self, context : Context, O, A, parents=None, children=None):
        if children is None:
            children = []
        
        if parents is None:
            parents = []

        self.context = context
        self.O = O
        self.A = A
        self._set_O = frozenset(O)  # this is not supposed to change, so it's a frozenset
        self.parents = parents
        self.children = children
    
    def in_extent(o) -> bool:
        return o in self._set_O  # O(1) amortised
    
    def add_child(self, concept):
        self.children.append(concept)
        concept.parents.append(self)
    
    def __repr__(self):
        return f'({[self.context.O[i] for i in self.O]}, {[self.context.A[i] for i in self.A]})'
    
    def to_tuple(self):
        return [self.context.O[i] for i in self.O], [self.context.A[i] for i in self.A]
