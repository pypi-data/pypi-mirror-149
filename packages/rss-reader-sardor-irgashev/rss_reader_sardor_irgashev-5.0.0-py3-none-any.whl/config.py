"""The module represents configuration file for logging functionality"""

logging_config = dict(
    version=1,
    formatters={
        'format': {'format': '%(levelname)-8s %(message)s'}
    },
    handlers={
        'handler': {'class': 'logging.StreamHandler',
                    'formatter': 'format',
                    'level': 'DEBUG'}
    },
    root={
        'handlers': ['handler'],
        'level': 'DEBUG',
    },
)
