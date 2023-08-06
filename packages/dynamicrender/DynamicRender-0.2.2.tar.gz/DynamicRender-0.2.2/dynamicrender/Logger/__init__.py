import configparser
import logging
import os

import colorlog

log_colors_config = {
    'DEBUG': 'white',  # cyan white
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

logger = logging.getLogger('logger_name')

# 输出到控制台
console_handler = logging.StreamHandler()
# 输出到文件
current_path = os.getcwd()
log_path = os.path.join(current_path, "DynamicRender.log")
file_handler = logging.FileHandler(filename=log_path, mode='a', encoding='utf8')

# 日志级别，logger 和 handler以最高级别为准，不同handler之间可以不一样，不相互影响
config_path = os.path.join(current_path, "config.ini")
if os.path.exists(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    file_level_type = config.get("Logger", "file_level")
    log_level_type = config.get("Logger", "log_level")
    try:
        file_level = {"DEBUG": logging.DEBUG, "INFO": logging.INFO, "WARNING": logging.WARNING, "ERROR": logging.ERROR,
                      "CRITICAL": logging.CRITICAL}[file_level_type]
    except:
        file_level = logging.ERROR
    try:
        log_level = {"DEBUG": logging.DEBUG, "INFO": logging.INFO, "WARNING": logging.WARNING, "ERROR": logging.ERROR,
                     "CRITICAL": logging.CRITICAL}[log_level_type]
    except:
        log_level = logging.INFO
else:
    file_level = logging.ERROR
    log_level = logging.INFO

logger.setLevel(log_level)
console_handler.setLevel(logging.DEBUG)
file_handler.setLevel(file_level)

# 日志输出格式
file_formatter = logging.Formatter(
    fmt='[%(asctime)s] %(filename)s ->%(funcName)s [%(levelname)s] : %(message)s',
    datefmt='%Y-%m-%d  %H:%M:%S'
)

console_formatter = colorlog.ColoredFormatter(
    fmt='%(log_color)s[%(asctime)s] %(filename)s -> %(funcName)s [%(levelname)s] : %(message)s',
    datefmt='%Y-%m-%d  %H:%M:%S',
    log_colors=log_colors_config
)

console_handler.setFormatter(console_formatter)
file_handler.setFormatter(file_formatter)

# 重复日志问题：
# 1、防止多次addHandler；
# 2、loggername 保证每次添加的时候不一样；
# 3、显示完log之后调用removeHandler
if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

console_handler.close()
file_handler.close()
