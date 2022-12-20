"""The file contains exceptions"""


class BaseClientException(Exception):
    """Base client class that implements exception"""


class BaseClientConfigurationException(BaseClientException):
    """Base client class that implements configuration exception"""
