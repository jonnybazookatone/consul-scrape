# encoding: utf-8
"""
Configuration file
"""

ENVIRONMENT = 'staging'

S3_BUCKET = 'etc-consul-scrape'

CS_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)s\t%(process)d '
                      '[%(asctime)s]:\t%(message)s',
            'datefmt': '%m/%d/%Y %H:%M:%S',
        }
    },
    'handlers': {
        'console': {
            'formatter': 'default',
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        'consul-scrape': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}