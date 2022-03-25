# EXAMPLE
# send sms with service 'http://smsc.ru/sys/send.php'

import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class SMS:

    URL = settings.URL_SMSC
    LOGIN = settings.SMS_LOGIN
    PASSWORD = settings.SMS_PASSWORD

    def send(self, mes: str, phones: str):
        # phones has string values separated by ';' or ','
        if not settings.SEND_SMS:
            return None

        assert isinstance(mes, str)
        assert isinstance(phones, str)

        mes = f'Код: {mes}'
        try:
            mes = mes.encode('cp1251')
        except:
            raise Exception('encode error')
        params = {
            'login': self.LOGIN,
            'psw': self.PASSWORD,
            'sender': settings.SMS_SENDER,
            'phones': phones,
            'mes': mes,
        }
        try:
            result = requests.post(url=self.URL, params=params)
        except Exception as e:
            logger.error('SEND-SMS:failed:%s' % str(e))
        else:
            return result
