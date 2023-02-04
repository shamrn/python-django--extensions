import os

ROOT_DIR_LOG = 'logs'


def get_path_to_dir(secondary_dir: str) -> str:
    """The method returns the path to the directory log, if dir is not exists - creates dirs"""

    if not os.path.exists(ROOT_DIR_LOG):
        os.mkdir(ROOT_DIR_LOG)

    full_path = os.path.join(ROOT_DIR_LOG, secondary_dir)
    if not os.path.exists(full_path):
        os.mkdir(full_path)

    return full_path


LOGGING = {
    'version': 1,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'file': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
        'py.warnings': {
            'handlers': ['console'],
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
