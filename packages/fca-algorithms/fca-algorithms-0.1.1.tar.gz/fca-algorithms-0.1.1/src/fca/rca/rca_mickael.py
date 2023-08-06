def rca_get_relations(K, R, P):
    """
    :param K: relational context family
    :param R: relations
    :param P: array with p18n operators for each R (len(P) == len(R))
    :return: Relational Lattice family
    """
    prev_concepts_len = 0
    curr_concepts_len = None
    lattices = []
    calculating_lattices = []
    for k in K:
        lattices.append(k.get_lattice())
        prev_concepts_len += lattices[-1].concepts_len()
        calculating_lattices.append(None)
    
    while prev_concepts_len != curr_concepts_len:
        # Invariant:
        #   lattices_prev has the last lattices calculated
        prev_concepts_len = curr_concepts_len or prev_concepts_len
        for k in K:
            for j, r in enumerate(R):
                for p in P[j]:
                    k.graduate(r, p, lattices[j])
        
        for i, k in enumerate(K):
            calculating_lattices[i] = k.get_lattice()
        
        # maintains the invariant, compress, and canonize
        curr_concepts_len = 0
        for i, l in calculating_lattices:
            lattices[i] = l.compress().canonize()
            curr_concepts_len += lattices[i].concepts_len()

    return lattices
