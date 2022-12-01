from base64 import b64encode
from collections import OrderedDict
from urllib import parse

from rest_framework.pagination import (
    CursorPagination as BaseCursorPagination,
    PageNumberPagination as BasePageNumberPagination)
from rest_framework.response import Response


class CursorPagination(BaseCursorPagination):

    page_size_query_param = 'page_size'
    page_size = 50
    max_page_size = 100

    def encode_cursor(self, cursor):
        """Given a Cursor instance, return an url with encoded cursor."""
        tokens = {}
        if cursor.offset != 0:
            tokens['o'] = str(cursor.offset)
        if cursor.reverse:
            tokens['r'] = '1'
        if cursor.position is not None:
            tokens['p'] = cursor.position

        querystring = parse.urlencode(tokens, doseq=True)
        encoded = b64encode(querystring.encode('ascii')).decode('ascii')
        return encoded


class PageNumberPagination(BasePageNumberPagination):

    page_size = 15

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('next', self.get_next_page_number()),
            ('previous', self.get_previous_page_number()),
            ('results', data)
        ]))

    def get_next_page_number(self):
        if not self.page.has_next():
            return None
        return self.page.next_page_number()

    def get_previous_page_number(self):
        if not self.page.has_previous():
            return None
        return self.page.previous_page_number()
