import logging
import time

logging.basicConfig(level = logging.INFO,filename='example.log',filemode='w',
                    format='%(asctime)s | %(name)s | %(module)s | %(levelname)s | %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)

logging.info("Pipeline started")
time.sleep(2)

logging.info("Extraction completed")
time.sleep(1)

logging.info("Transformation completed")
time.sleep(1)

logging.info("Loading completed")

logging.info("Pipeline finished")