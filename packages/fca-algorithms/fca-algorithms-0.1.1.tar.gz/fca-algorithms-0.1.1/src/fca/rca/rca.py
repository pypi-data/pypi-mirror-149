from ..utils.utils import from_subscript


def rca_get_relations(K, R, p):
    """
    :param K: contexts
    :param R: relations
    :param p: p18n operator
    :return: Relational Lattice family
    """
    lattices = []
    calculating_lattices = []
    for k in K:
        lattices.append(k.get_lattice())
        calculating_lattices.append(None)
    
    stable = False
    while not stable:
        # Invariant:
        #   lattices_prev has the last lattices calculated
        for i, k in enumerate(K):
            for r in R:
                if i == r.i:
                    k.graduate(r, p, lattices[r.j], r.j)
        
        for i, k in enumerate(K):
            calculating_lattices[i] = k.get_lattice()
        
        # O(|calculating_lattices| * |concepts|)
        for i, l in enumerate(calculating_lattices):
            stable = stable or l.isomorph(lattices[i])  # O(|concepts|)
            lattices[i] = l  # maintains the invariant
    return lattices


def lattice_and_concept_idx(relational_attribute):
    double_points_idx = relational_attribute.index('C')
    without_C = relational_attribute[double_points_idx + 1:]
    i, j = without_C.split('₋')
    return from_subscript(i), from_subscript(j)
