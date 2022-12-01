
def annotate_similarity(self, value: str):
    return self.annotate(
        similarity=greatest_trigram_similarity(
            fields=('title', 'description'),
            value=value
        )
    ).filter(similarity__gt=0.3)
