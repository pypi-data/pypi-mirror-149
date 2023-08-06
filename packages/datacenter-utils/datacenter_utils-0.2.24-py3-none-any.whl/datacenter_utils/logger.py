# -*- encoding:utf-8 -*-
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(filename)s[func:%(funcName)s, line:%(lineno)d] - %(levelname)s - %(message)s'
)
logger = logging.getLogger()

def file_logger(file_path):
    logger = logging.getLogger()
    handler = logging.FileHandler(file_path, encoding='UTF-8')
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(filename)s[func:%(funcName)s, line:%(lineno)d] - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    return logger