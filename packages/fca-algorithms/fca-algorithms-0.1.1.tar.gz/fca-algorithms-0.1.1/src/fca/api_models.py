from .base_models import Context as Ctx
from .get_lattice import FCASolver, Inclose
from .utils.utils import to_subscript
from .plot.plot import plot_from_hasse


class Context(Ctx):
    def __init__(self, O, A, I, solver : FCASolver = None):
        super().__init__(O, A, I)
        
        if solver is None:
            solver = Inclose()
        
        self.solver = solver
        self.iteration = 0

        # FIXME: The ideal would be to cache the last_lattice
        #        and also calculate them from the point they were already calculated
        #        * is that possible not to repeat calculations?
        #        * if not, can we bound the amount of calculations that have to be repeated?
        self._last_lattice = None
    
    def get_concepts(self):
        return self.solver.get_concepts(self)
    
    def get_lattice(self):
        hasse, concepts = self.solver.get_lattice(self)
        if self._last_lattice is None:
            self._last_lattice = Lattice(hasse, concepts)
        else:
            from_idx = len(self._last_lattice.concepts)
            self._last_lattice.from_iteration.append(from_idx)
            self._last_lattice = Lattice(hasse, concepts, self._last_lattice.from_iteration)
        return self._last_lattice
    
    def graduate(self, relation, p, lattice, lattice_idx):
        """
        Applies graduation. Extends the formal context with more attributes
        with the relation `relation`, using the p18n operator, against the lattice `lattice`
        """
        q = self.iteration
        for i, concept in lattice.concepts_from(q):
            self.A.append(f'{p}{relation} : C{to_subscript(lattice_idx)}₋{to_subscript(i)}')
        
        for o, relations in enumerate(self.I):
            # this only works considering the relations is a array[array[bool]], if we wanted to make this stream-friendly,
            # we'd have to change it perhaps.
            relations.extend([p(o, relation, c) for _, c in lattice.concepts_from(q)])
        
        self.iteration += 1


class Lattice:
    def __init__(self, hasse, concepts, from_iteration=None):
        self.hasse = hasse
        self.concepts = concepts
        self.ctx = self.concepts[-1].context
        if from_iteration is None:
            # from_iteration[q] gives the idx in `concepts` from where to start iterating the concepts
            # added in iteration q
            self.from_iteration = [0]
        else:
            self.from_iteration = from_iteration
    
    def isomorph(self, other_lattice):
        """
        This method needs the two lattices to have the concepts ordered in the same way, othetwise it'll fail
        - Complexity: O(|self.concepts|), \omega(1)
        """
        if len(self.concepts) != len(other_lattice.concepts):
            return False
        
        for i, concept in enumerate(self.concepts):
            if len(concept.O) != len(other_lattice.concepts[i].O) or \
               len(concept.A) != len(other_lattice.concepts[i].A):
                return False
        return True
    
    def concepts_from(self, q):
        """iterator for all the concepts of iteration q and their indexes: idx, concept
        """
        from_i = self.from_iteration[q]
        to_i = len(self.concepts) if len(self.from_iteration) <= q + 1 else self.from_iteration[q + 1]
        for i in range(from_i, to_i):
            yield i, self.concepts[i]
    
    def plot(self):
        plot_from_hasse(self.hasse, self.concepts)
    
    def __repr__(self):
        return str(self.concepts)





