"""Package Loggers"""
import logging.config

CONSOLE_LOGGER_NAME = 'console'
FILE_LOGGER_NAME = 'file'

def setup_logging():
    """Initialize logging for pygypsy package"""
    log_conf = {
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
                'filename': './pygypsy.log',
                'mode': 'w',
            },
        },
        'loggers': {
            'pygypsy.forward_simulation': {
                'handlers':['file'],
                'level':'INFO',
                'propagate': True,
            },
            'pygypsy.data_prep': {
                'handlers':['file'],
                'level':'DEBUG',
                'propagate': True,
            },
            'pygypsy.utils': {
                'handlers':['file'],
                'level':'DEBUG',
                'propagate': True,
            },
            'pygypsy.basal_area_simulate': {
                'handlers':['file'],
                'level':'DEBUG',
                'propagate': True,
            },
            'pygypsy.basal_area_factor': {
                'handlers':['file'],
                'level':'DEBUG',
                'propagate': True,
            },
            'pygypsy.density': {
                'handlers':['file'],
                'level':'DEBUG',
                'propagate': True,
            },
            'pygypsy.plot': {
                'handlers':['file'],
                'level':'DEBUG',
                'propagate': True,
            },
            'pygypsy.stand_density_factor': {
                'handlers':['file'],
                'level':'DEBUG',
                'propagate': True,
            },
            'pygypsy.volume': {
                'handlers':['file'],
                'level':'DEBUG',
                'propagate': True,
            },
            'pygypsy.GYPSYNonSpatial': {
                'handlers':['file'],
                'level':'INFO',
                'propagate': True,
            },
            'pygypsy.site_index': {
                'handlers':['file'],
                'level':'DEBUG',
                'propagate': True,
            },
            CONSOLE_LOGGER_NAME: {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': True,
            },
        }
    }

    logging.config.dictConfig(log_conf)
