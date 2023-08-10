from abc import ABCMeta, abstractmethod

from django.test import TestCase
from rest_framework.reverse import reverse


class TestReverse(TestCase, metaclass=ABCMeta):

    @property
    @abstractmethod
    def PATH(self) -> str:  # NOQA
        """Path resource """

    @property
    @abstractmethod
    def ENDPOINT(self) -> str:  # NOQA
        """Endpoint"""

    def test_reverse(self):
        self.assertEqual(self.ENDPOINT, reverse(self.PATH))
