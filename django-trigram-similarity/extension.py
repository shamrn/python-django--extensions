from django.db.models.functions import Greatest
from django.contrib.postgres.search import TrigramSimilarity


def greatest_trigram_similarity(fields: list, value: str) -> Greatest:
    """
    It takes as input a list of fields to search for "['name', 'title', ....]",
    and the search "value", and returns the result for the most relevant field.
    """

    return Greatest(*[TrigramSimilarity(field, value) for field in fields])
