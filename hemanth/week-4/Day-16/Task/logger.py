import logging

logging.basicConfig(
    level=logging.INFO,
    filename='ETLlogger.log',
    filemode='w',
    format='%(asctime)s,%(msecs)03d | %(name)s | %(module)s | %(levelname)s | %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("ETL")