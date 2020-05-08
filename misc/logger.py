"""Create a logger with file and stream handler"""
import logging

level = "debug"

# Create logger
logger = logging.getLogger()
if logger.hasHandlers():
    logger.handlers.clear()

if level == 'debug':
    logger.setLevel(logging.DEBUG)
elif level == 'info':
    logger.setLevel(logging.INFO)

# Create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Create file handler and set level to debug
fh = logging.FileHandler('tjj-bot.log', mode='a')
fh.setLevel(logging.DEBUG)

# Create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add formatter
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

return logger
