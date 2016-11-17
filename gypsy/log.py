import logging.config

CONSOLE_LOGGER_NAME = 'console'
FILE_LOGGER_NAME = 'file'

def setup_logging():
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(process)d %(thread)d %(message)s'
            },
            'standard': {
                'format': '%(levelname)s %(asctime)s %(message)s'
            },
            'colored': {
                '()': 'colorlog.ColoredFormatter',
                'format': "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s"
            },
        },
        'handlers': {
            'console':{
                'level':'INFO',
                'class':'logging.StreamHandler',
                'formatter': 'colored'
            },
            'file': {
                'level': 'DEBUG',
                'formatter': 'standard',
                'class': 'logging.FileHandler',
                'filename': './gypsy.log',
                'mode': 'w',
            },
        },
        'loggers': {
            'gypsy.forward_simulation': {
                'handlers':['file'],
                'level':'INFO',
                'propagate': True,
            },
            'gypsy.data_prep': {
                'handlers':['file'],
                'level':'DEBUG',
                'propagate': True,
            },
            'gypsy.utils': {
                'handlers':['file'],
                'level':'DEBUG',
                'propagate': True,
            },
            'gypsy.basal_area_simulate': {
                'handlers':['file'],
                'level':'DEBUG',
                'propagate': True,
            },
            'gypsy.density': {
                'handlers':['file'],
                'level':'DEBUG',
                'propagate': True,
            },
            'gypsy.plot': {
                'handlers':['file'],
                'level':'DEBUG',
                'propagate': True,
            },
            'gypsy.stand_density_factor': {
                'handlers':['file'],
                'level':'DEBUG',
                'propagate': True,
            },
            'gypsy.volume': {
                'handlers':['file'],
                'level':'DEBUG',
                'propagate': True,
            },
            'gypsy.GYPSYNonSpatial': {
                'handlers':['file'],
                'level':'INFO',
                'propagate': True,
            },
            'gypsy.site_index': {
                'handlers':['file'],
                'level':'DEBUG',
                'propagate': True,
            },
            CONSOLE_LOGGER_NAME: {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': True,
            },
        }
    }

    logging.config.dictConfig(LOGGING)
