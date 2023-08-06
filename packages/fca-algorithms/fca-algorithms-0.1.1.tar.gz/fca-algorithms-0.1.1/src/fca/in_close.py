from .base_models import Context, Concept
from .utils.utils import inverse_range, is_in, lower_bound, insert_ordered


r_new = 0
concepts = []
graph = []


def inclose_start(context : Context):
    global r_new
    global concepts
    global ctx
    ctx = context
    initial_concept = Concept(ctx, [i for i in range(len(context.O))], [])  # Concepts only uses indexes
    concepts = [initial_concept]
    r_new = 0
    inclose(0, 0)

    # pop the last concept if it hasn't been closed
    if len(concepts[-1].A) == 0:
        concepts.pop()

    return concepts


def inclose(r, y):
    """incrementally close the concept r, beginning with attribute y
    """
    global r_new
    global concepts
    global ctx
    r_new += 1
    for j in range(y, len(ctx.A)):
        if len(concepts) <= r_new:
            concepts.append(Concept(ctx, [], []))
        else:
            concepts[r_new].O = []

        for i in concepts[r].O:  # concepts[r].O \cap {j}'
            if ctx.I[i][j]:
                is_there, _ = is_in(i, concepts[r_new].O)
                if not is_there:
                    insert_ordered(i, concepts[r_new].O)  # append only if it's not in the list
        
        if len(concepts[r_new].O) > 0:
            if len(concepts[r_new].O) == len(concepts[r].O):
                is_there, _ = is_in(j, concepts[r].A)
                if not is_there:
                    insert_ordered(j, concepts[r].A)
            elif is_canonical(r, j - 1):
                new_attributes = concepts[r].A.copy()
                is_there, _ = is_in(j, new_attributes)
                if not is_there:
                    insert_ordered(j, new_attributes)
                concepts[r_new].A = new_attributes  # O(|concepts[r].A|)
                inclose(r_new, j + 1)


def is_canonical(r, y):
    new_y = y
    for k in inverse_range(len(concepts[r].A)):
        for j in range(new_y, concepts[r].A[k], -1):
            h = 0
            while h < len(concepts[r_new].O):
                if not ctx.I[concepts[r_new].O[h]][j]:
                    break
                h += 1
            if h == len(concepts[r_new].O):
                return False
        new_y = concepts[r].A[k] - 1
    
    for j in range(new_y, -1, -1):
        h = 0
        while h < len(concepts[r_new].O):
            if not ctx.I[concepts[r_new].O[h]][j]:
                break
            h += 1
        if h == len(concepts[r_new].O):
            return False
    return True
