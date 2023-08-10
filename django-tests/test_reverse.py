from abc import ABCMeta, abstractmethod

from rest_framework.reverse import reverse


class TestReverseMixin(metaclass=ABCMeta):

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
