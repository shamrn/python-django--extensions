from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class StrReprModel(models.Model):
    """Abstract model for instance representation"""

    class Meta:
        """Meta class"""

        abstract = True

    def __str__(self):
        """Implement `str` dunder."""

        if hasattr(self, 'id') and hasattr(self, 'name'):
            return f'{self.id}: {self.name}'
        return super(StrReprModel, self).__str__()


class ReprDunderModel(StrReprModel, models.Model):
    """Dunder abstract model"""

    class Meta:
        """Meta class"""

        abstract = True

    def __repr__(self):
        """Implement `repr` dunder."""

        return f'{self.id}: {self.__class__.__name__}'


class BaseModel(ReprDunderModel, models.Model):
    """Base abstract model"""

    created = models.DateTimeField(default=timezone.now, editable=False,
                                   verbose_name=_('Date created'))
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name=_('Date updated'))

    class Meta:
        abstract = True


class ActiveModel(models.Model):
    """Active abstract model"""

    is_active = models.BooleanField(default=True, verbose_name=_('Active'))

    class Meta:
        abstract = True


class SortableModel(models.Model):
    """Sortable abstract model"""

    # Sorting with library sortable2
    sort = models.PositiveSmallIntegerField(default=0, blank=False, null=False,
                                            verbose_name=_('Sort'))

    class Meta:
        abstract = True
