import os
import logging

log_filename = __name__
log_path = os.path.join(os.getcwd(), log_filename)
log_format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
logging.basicConfig(level=logging.DEBUG,
                    format=log_format,
                    datefmt='%y-%m-%d %H:%M:%S',
                    filename=log_path,
                    filemode='w')
log = logging.getLogger(__name__)
