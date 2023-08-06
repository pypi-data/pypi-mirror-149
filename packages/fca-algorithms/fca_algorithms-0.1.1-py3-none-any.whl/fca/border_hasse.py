
def calculate_hasse(ctx, concepts):
    """Calculates the hasse graph and outputs it as:
      List[List[int]], ordered_concepts
      Note that the indexes in the hasse are the indexes in the ordered_concepts.
    """
    if not concepts:
        return []

    number_of_attributes = len(ctx.A)

    ordered_concepts = order(concepts, number_of_attributes)  # creates a new list with the concepts ordered based on the border algorithm
    hasse_lattice = [[] for _ in range(len(concepts))]  # a graph
    border = set([0])
    for i in range(1, len(concepts)):
        ci = ordered_concepts[i]
        intent_ci = frozenset(ci.A)
        intents = []
        concepts_by_intent = {}
        for c_idx in border:
            c = ordered_concepts[c_idx]
            intents_intersected = set(c.A)
            intents_intersected = frozenset(intents_intersected.intersection(intent_ci))
            intents.append(intents_intersected)
            concepts_by_intent[intents_intersected] = c_idx
        cover_intents = maxima(intents, number_of_attributes)
        upper_covers = set()
        for intent in cover_intents:
            idx = find_concept(intent, concepts_by_intent, ordered_concepts, i)
            c = ordered_concepts[idx]
            ci.add_child(c)
            hasse_lattice[i].append(idx)
            upper_covers.add(idx)
        border.difference_update(upper_covers)
        border.add(i)
    return hasse_lattice, ordered_concepts
            



def order(concepts, number_of_attributes):
    """linear time sorting (in |concpets|) of concepts
    """
    bunches = [[] for _ in range(number_of_attributes + 1)]
    for c in concepts:
        bunches[len(c.A)].append(c)
    return [concept for bunch in bunches for concept in bunch]


def maxima(intents, number_of_attributes):
    ordered_intents = order_intents(intents, number_of_attributes)
    maxi = []
    for intent in ordered_intents:
        is_min = True
        for elem in maxi:
            is_min = is_min and not intent.issubset(elem)
        if is_min:
            maxi.append(intent)
    return maxi


def order_intents(intents, number_of_attributes):
    bunches = [[] for _ in range(number_of_attributes + 1)]
    for intent in intents:
        bunches[len(intent)].append(intent)
    
    return [intent for bunch in reversed(bunches) for intent in bunch]


def find_concept(intent, cover_intents, ordered_concepts, idx_so_far):
    i = cover_intents[intent]
    c = ordered_concepts[cover_intents[intent]]
    Y = set(intent)
    while set(c.A) != Y:
        i -= 1
        c_aux = ordered_concepts[i]  # at least it'll have one
        while not Y.issubset(set(c_aux.A)):
            i -= 1
            c_aux = ordered_concepts[i]
        c = c_aux
    return i
        