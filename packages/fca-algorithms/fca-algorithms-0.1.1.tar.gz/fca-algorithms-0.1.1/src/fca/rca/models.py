"""
Propositionalization (P18N) operators
"""

from ..utils.utils import to_subscript


class Propositionalization:
    def __call__(self, object, relation, concept) -> bool:
        return False


class Exists(Propositionalization):
    def __call__(self, obj, relation, concept) -> bool:
        for o in concept.O:
            # with a set structure or bitset, we would know this in
            # O(len(objects)) / 64, considering a 64bit arc
            # other option would be to use a set and then relation[i][j] returns whether j is in the set relation[i],
            # but this latter option is costly in memory, although easier to implement.
            if o in relation[obj]:
                return True
        return False
    
    def __repr__(self):
        return '∃'


class Forall(Propositionalization):
    def __call__(self, obj, relation, concept) -> bool:
        for o in concept.O:
            # with a set structure or bitset, we would know this in
            # O(len(objects)) / 64, considering a 64bit arc
            # other option would be to use a set and then relation[i][j] returns whether j is in the set relation[i],
            # but this latter option is costly in memory, although easier to implement.
            if o not in relation[obj]:
                return False
        return True
    
    def __repr__(self):
        return '∀'


class Relation(list):
    def __init__(self, array, i, j):
        super().__init__(array)
        self.i = i
        self.j = j

    def __repr__(self):
        return f'R{to_subscript(self.i)}₋{to_subscript(self.j)}'

