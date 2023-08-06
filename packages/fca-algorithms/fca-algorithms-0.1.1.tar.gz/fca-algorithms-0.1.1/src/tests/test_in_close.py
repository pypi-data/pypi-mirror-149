import pytest
from src.fca.base_models import Context
from src.fca.in_close import inclose_start
from src.fca.get_lattice import Inclose
from src.fca.plot.plot import plot_from_hasse



def test_inclose_returns_all_the_concepts_but_bottom(create_objects_and_attributes):
    O, A, I = create_objects_and_attributes
    c = Context(O, A, I)
    concepts = inclose_start(c)
    res = [x.to_tuple() for x in concepts]
    expected_result = [(['Tg05', 'Tg05FX', 'Flxtra', 'Hxr'], []),
                       (['Tg05FX', 'Hxr'], ['Effect', 'Control']),
                       (['Tg05FX'], ['Effect', 'Control', 'Short']),
                       (['Tg05'], ['Power', 'Short']),
                       (['Tg05FX', 'Flxtra', 'Hxr'], ['Control']),
                       (['Tg05', 'Tg05FX'], ['Short'])]
    assert res == expected_result


def test_inclose_solver_returns_all_the_concepts(create_objects_and_attributes):
    O, A, I = create_objects_and_attributes
    c = Context(O, A, I)
    concepts = Inclose().get_concepts(c)
    res = [x.to_tuple() for x in concepts]
    expected_result = [(['Tg05', 'Tg05FX', 'Flxtra', 'Hxr'], []),
                       (['Tg05FX', 'Hxr'], ['Effect', 'Control']),
                       (['Tg05FX'], ['Effect', 'Control', 'Short']),
                       (['Tg05'], ['Power', 'Short']),
                       (['Tg05FX', 'Flxtra', 'Hxr'], ['Control']),
                       (['Tg05', 'Tg05FX'], ['Short']),
                       ([], ['Effect', 'Power', 'Control', 'Short'])]
    assert res == expected_result


def test_inclose_solver_returns_all_the_concepts_when_there_are_objects_with_all_attributes(create_objects_and_attributes):
    O, A, I = create_objects_and_attributes
    c = Context(O, A, I)
    c.I[1][1] = True
    concepts = Inclose().get_concepts(c)
    res = [x.to_tuple() for x in concepts]
    assert (['Tg05FX'], ['Effect', 'Power', 'Control', 'Short']) in res


def test_inclose_solver_returns_association_rules(create_objects_and_attributes):
    O, A, I = create_objects_and_attributes
    c = Context(O, A, I)
    assoc_rules = [r for r in Inclose().get_association_rules(c, min_support=0.4, min_confidence=1)]
    assert len(assoc_rules) == 1
    first_association_rules = assoc_rules[0]
    x = first_association_rules.ordered_statistics[0]

    assert 0.42 < first_association_rules.support < 0.43

    # Effect -> Control
    assert len(x.items_base) == 1
    assert 0 in x.items_base

    assert len(x.items_add) == 1
    assert 2 in x.items_add

    assert x.confidence == 1


@pytest.mark.skip(reason="UI test")
def test_lattice_construction(create_objects_and_attributes_2):
    O, A, I = create_objects_and_attributes_2
    c = Context(O, A, I)
    hasse_lattice, concepts = Inclose().get_lattice(c)
    plot_from_hasse(hasse_lattice, concepts)
    assert hasse_lattice
