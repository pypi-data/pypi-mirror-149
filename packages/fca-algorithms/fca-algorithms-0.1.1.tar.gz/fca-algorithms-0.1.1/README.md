# FCA utils

Module for FCA basics such as retrieving concepts, drawing a hasse diagram, etc

## Getting formal concepts

```python
from fca.api_models import Context

c = Context(O, A, I)
concepts = c.get_concepts(c)
```

## Getting association rules


```python
from fca.api_models import Context

c = Context(O, A, I)
c.solver.get_association_rules(c, min_support=0.4, min_confidence=1)
```


## Drawing hasse diagram


```python
from fca.plot.plot import plot_from_hasse
from fca.api_models import Context


c = Context(O, A, I)
hasse_lattice, concepts = c.get_lattice(c)
plot_from_hasse(hasse_lattice, concepts)
```

# CLI

To plot a hasse diagram from a context

```bash
fca_cli -c input.csv --show_hasse
```

The context is expected to be a `csv` with the following format

name|attr1|attr2
----|:-----:|:-----:
obj1|x|
obj2||x
obj3|x|x
obj4||

# TODO

- Make algorithms to be able to work with streams (big files)

