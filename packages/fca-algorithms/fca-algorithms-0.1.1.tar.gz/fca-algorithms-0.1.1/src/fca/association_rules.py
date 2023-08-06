from typing import List


from apyori import apriori
from .base_models import Concept

def get_association_rules(concepts : List[Concept], min_support=0.5, min_confidence=1):
    """Given a list of concepts, it returns a generator of its association rules
    """
    transactions = [c.A for c in concepts]
    return apriori(transactions, min_support=min_support, min_confidence=min_confidence)
