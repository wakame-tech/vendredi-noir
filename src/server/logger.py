import logging
import coloredlogs

logger = logging.getLogger()
logger.setLevel('INFO')
coloredlogs.install(level='INFO', logger=logger,
                    fmt='%(asctime)s : %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
# logging.FileHandler('output.log', 'w', 'utf-8')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    '%(asctime)s : %(levelname)s : %(message)s', datefmt='%Y/%m/%d %H:%M:%S'))
logger.addHandler(handler)
