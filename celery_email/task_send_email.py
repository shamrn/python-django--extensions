import logging
from smtplib import SMTPAuthenticationError, SMTPException
from typing import Optional

from celery import shared_task
from django.core.mail import send_mail

logger = logging.getLogger('schedule_task')


@shared_task
def task_send_email(
        subject: str,
        from_email: str,
        recipient_list: list[str],
        message: str = '_',
        html_message: Optional[str] = None,
):
    """Task for send email"""

    logger.info('METHOD. NAME: common.tasks.task_send_email')
    logger.info(f'METHOD. DATA:\n'
                f'subject: {subject}\n'
                f'from_email: {from_email}\n'
                f'recipient_list: {recipient_list}\n'
                f'is html_message: {bool(html_message)}\n'
                f'message: {message}\n')

    try:
        result_code = send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message
        )
        if result_code:
            logger.info(f'METHOD. RESULT: Success')
        else:
            logger.info(f'METHOD. RESULT: Error')

    except SMTPAuthenticationError as exc:
        logger.exception(f'METHOD. EXCEPTION: {exc}')
        logger.exception(f'METHOD. MESSAGE: Authentication error.')
    except SMTPException as exc:
        logger.exception(f'METHOD. EXCEPTION: {exc}')
        logger.exception(f'METHOD. MESSAGE: Base Smtp exception.')
    except Exception as exc:
        logger.exception(f'METHOD. EXCEPTION: {exc}')
        logger.exception(f'METHOD. MESSAGE: Base exception.')
