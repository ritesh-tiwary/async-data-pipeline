import logging


class Logger:
    def __init__(self, logger_name):
        stream_formatter = logging.Formatter('%(levelname)s - %(name)s - %(message)s')
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        stream_handler = logging.StreamHandler()
        file_handler = logging.handlers.TimedRotatingFileHandler('app/logs/app.log', when='midnight', interval=1, backupCount=7, delay=True)

        stream_handler.setFormatter(stream_formatter)
        file_handler.setFormatter(file_formatter)
        logging.basicConfig(handlers=[stream_handler, file_handler], level=logging.INFO, encoding='utf-8')
        self.logger = logging.getLogger(logger_name)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)
