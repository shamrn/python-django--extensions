

def annotate_trigram_similarity(
        self, value: str) -> Union['...QuerySet', models.QuerySet]:

    return self.annotate_author_full_name().annotate(
        trigram_similarity=greatest_trigram_similarity(
            fields=['text', 'description', 'author__username'],
            value=value))
