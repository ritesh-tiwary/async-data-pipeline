import logging


class Logger:
    def __init__(self, name):
        self.logger_name = name
        self.stream_handler = logging.StreamHandler()
        self.time_rotating_file_handler = logging.handlers.TimedRotatingFileHandler('app/logs/app.log', when='midnight', interval=1, backupCount=7)

    def get_logger(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                            handlers=[self.stream_handler, self.time_rotating_file_handler])

        logger = logging.getLogger(self.logger_name)
        return logger

    def info(self, message):
        logger = self.get_logger()
        logger.info(message)

    def error(self, message):
        logger = self.get_logger()
        logger.error(message)
