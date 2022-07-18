import logging
from typing import TYPE_CHECKING

from django.conf import settings
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from extension.functions import get_current_site_url
from extension.integration.client import BaseClient
from extension.redis import cache

if TYPE_CHECKING:
    from payment.models import Transaction

logger = logging.getLogger('atol')


class AtolClient(BaseClient):
    """The class implements client for `Atol-online` service.
     resource: `https://atol.online/files/API_atol_online_v4.pdf` """

    url = settings.ATOL_URL + settings.ATOL_VERSION
    _callback_url = None

    _headers = {'Content-Type': 'application/json'}

    _auth_data = settings.ATOL_AUTH_DATA
    _company_data = settings.ATOL_COMPANY_DATA
    _group_code = settings.ATOL_GROUP_CODE

    _appropriate_codes = [HTTP_200_OK, HTTP_201_CREATED]

    _token_key_cache = 'atol_key_cache'
    _token_activity_time = 23 * 60 * 60  # seconds ( according to the documentation )

    def __init__(self, transaction: 'Transaction'):
        """Dunder method for class initialization"""

        super().__init__()

        self.transaction = transaction

    def register_document(self) -> dict | None:
        """Method for register document"""

        if token := self._get_token():  # NOQA
            self._headers.update(dict(token=token))
            data = self._prepare_data()
            result, status_code = self.do_request(request_method='POST',
                                                  endpoint=f'{self._group_code}/sell',
                                                  data=data,
                                                  headers=self._headers)
            if status_code not in self._appropriate_codes:
                logger.error(f'METHOD. NAME. integration.atol.Atol.register_document')
                logger.error(f'METHOD. DATA. transaction_id {self.transaction.id}')
                logger.error(f'METHOD. STATUS CODE: {status_code} RESULT: {result}')

                if not status_code:
                    return None

            return result

    def _prepare_data(self) -> dict:
        """Prepare data for register"""

        order = self.transaction.order
        user = order.user

        callback_url = get_current_site_url() + reverse('api:payment:cloudpayments-callback')

        items = [
            {
                'name': item.product_name,
                'price': float(item.product_price),
                'quantity': item.quantity,
                'sum': float(item.product_price * item.quantity),
                'measurement_unit': 'шт',
                'payment_method': 'full_prepayment',
                'payment_object': 'commodity',
                'vat': {'type': 'none'}
            }
            for item in order.cart.cart_items.all()
        ]

        delivery_price = float(order.delivery.price)
        items.append({
            'name': 'Доставка',
            'price': delivery_price,
            'quantity': 1,
            'sum': delivery_price,
            'measurement_unit': 'шт',
            'payment_method': 'full_prepayment',
            'payment_object': 'service',
            'vat': {'type': 'none'}
        })

        return {
            'external_id': str(order.code),
            'receipt': {
                'client': {
                    'email': user.email
                },
                'company': self._company_data,
                'items': items,
                'payments': [
                    {
                        'type': 1,
                        'sum': float(order.total_cost)
                    }
                ],
                'total': float(order.total_cost)
            },
            'service': {
                'callback_url': callback_url
            },
            'timestamp': order.created.strftime('%d.%m.%Y %H:%y:%s')
        }

    def _get_token(self) -> str | None:
        """Method for get token"""

        if token := cache.get(self._token_key_cache):  # NOQA
            return token.decode()

        result, status_code = self.do_request(request_method='POST',
                                              endpoint='getToken',
                                              data=self._auth_data,
                                              headers=self._headers)
        token = result.get('token')

        if status_code not in self._appropriate_codes and not token:
            logger.error(f'METHOD. NAME. integration.atol.Atol._get_token')
            logger.error(f'METHOD. STATUS CODE: {status_code} RESULT: {result}')
            return None

        cache.set(name=self._token_key_cache, value=token, ex=self._token_activity_time)

        return token
